---
title: Agent Memory
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - memory
  - architecture
status: learning
aliases:
  - Memory
  - Agent Memory Systems
---

# Agent Memory

> How an agent **recalls information across time** — within a run and across
> runs. Four kinds: working, episodic, semantic, procedural. The headline topic
> of domain [[03 Memory Systems]]; here, the orchestrator's responsibility for it.

## What it is

Memory is everything the agent "knows" beyond the current prompt. Unlike
[[State Management]] (this run's live working set), memory spans runs and is
selectively retrieved into context when relevant.

The four types:
- **Working memory** — the current context window; what the model can see *right now*.
- **Episodic memory** — logs of past interactions/events ("last week the user asked X").
- **Semantic memory** — a knowledge store of facts, usually a vector DB ([[RAG for Agents]]).
- **Procedural memory** — learned how-to patterns (effective tool-use sequences, skills).

## Why it's the orchestrator's job

The LLM has no memory between calls. The orchestrator decides **what to store,
where, and what to retrieve back into [[Context Building]]** each step — without
overflowing the window or polluting context with irrelevant recall.

## How it works — write & read paths

- **Write path** — after a step/run, persist salient facts/events (episodic → a
  log table; semantic → embeddings in a vector store).
- **Read path** — each step, retrieve the most relevant memories (recency,
  similarity) and inject them into the prompt.

```python
# WRITE (after a turn)
log_episode(user_id, turn)                     # episodic: usually always
facts = extract_facts(turn)                    # optional LLM "memory manager"
if facts: vectordb.upsert(embed(facts))        # semantic

# READ (building the next prompt)
recent   = episodic.recent(user_id, n=5)       # by recency (SQL)
relevant = vectordb.search(embed(query), k=5)  # by similarity
ctx = build_context(state, recent, relevant)   # → [[Context Building]] = working memory
```

## Provisioning each memory type

| Type | Set up / provision | What goes in | Write decision |
|---|---|---|---|
| **Working** | nothing separate — it's the context window, built from [[State Management\|state]] | system prompt + recent turns + retrieved memories + input | automatic each turn ([[Context Building]]) |
| **Episodic** | a DB table (Postgres/Mongo), keyed by `user_id` + time | past conversations/events, time-stamped | usually automatic — log every interaction |
| **Semantic** | a vector store (Qdrant, pgvector, Pinecone) | facts, docs, KB — chunked + embedded | batch ingest OR LLM fact-extraction |
| **Procedural** | prompt/skill registry, files, or tools | reusable how-to sequences / skills | mostly manual today; auto via [[Reflection]] |

## Is "what goes where" decided manually each time?

Three layers — separate them and it clears up:

1. **Type → store mapping is decided ONCE, at design time** (working = context,
   episodic = log table, semantic = vector store, procedural = skill registry).
   Not re-decided per message — it's architecture.
2. **Per-item write ("remember *this*, and where?"):**
   - **Rule-based / automatic** (common) — always log turns; always embed uploaded docs.
   - **LLM memory-manager** (smarter) — the model decides "durable fact → semantic"
     / "useful procedure → procedural" (MemGPT/Letta, Mem0, ChatGPT memory).
   - **Manual** — user/engineer curates ("remember I prefer X").
3. **Read ("what to pull back") is always automated** each turn via
   [[Context Building]] (episodic by recency, semantic by similarity).

> **Design is one-time & manual; per-item writes are usually automated; reads are always automated.**

## Working memory ↔ state

Working memory is **not stored separately** — it's **assembled from the loaded
[[State Management|state]]** (plus retrieved memories) right before each call, then
discarded.

```
Redis/Postgres ──load──▶ build (trim/summarise/retrieve) ──▶ context window
    STATE                                                     WORKING MEMORY
 (persisted,                                                 (transient, rebuilt
  full history)                                               every call)
```

Per call: **load state → retrieve memories → build context (= working memory) →
call LLM → update state → save.** In a simple agent with no trimming/retrieval,
working memory ≈ the loaded state; they diverge once you trim/summarise or add
retrieval (which injects facts that weren't in this run's state at all).

## State vs episodic memory (both can live in Postgres!)

Same database, different *role* — **now** vs **the past**:

|           | **State**                            | **Episodic memory**                 |
| --------- | ------------------------------------ | ----------------------------------- |
| Time      | NOW — current run                    | PAST — previous runs                |
| Scope     | one conversation (`conversation_id`) | all of a user's history (`user_id`) |
| Access    | load the whole blob each turn        | query/search relevant episodes      |
| Lifecycle | active, then done                    | persists & accumulates              |
| Role      | *is* the conversation                | *brought into* a conversation       |

**The handoff:** when a conversation ends, its state (or a summary) is written into
episodic memory for future recall — so **episodic memory is largely "yesterday's
states, archived and made searchable."** Two tables: `sessions` (state, by
`conversation_id`, load-whole) vs `episodes` (episodic, by `user_id`, query-relevant).

## Searching episodic memory — do you need a vector DB?

You retrieve *relevant* episodes, never load all. But **"search" ≠ "vector DB"** —
there are three kinds, and only the last needs vectors:

| Search | Finds | Needs |
|---|---|---|
| **Recency / structured** | last N for a user, by date/status | plain Postgres SQL |
| **Keyword / full-text** | episodes containing a *word* | Postgres `tsvector` |
| **Semantic / similarity** | episodes *about* a topic, any wording | embeddings |

Only **semantic** needs vectors — and even then **pgvector** adds similarity search
*to Postgres itself*:

| Setup | Gives you |
|---|---|
| Plain Postgres | recency, filters, keyword |
| Postgres + **pgvector** | + semantic similarity |
| Dedicated vector DB (Qdrant/Pinecone) | semantic at large scale / high throughput |

**So a vector DB isn't *required* for episodic memory** — recency/keyword run in
plain Postgres; semantic recall can use pgvector; a dedicated vector DB (e.g.
Qdrant) is a **scale** choice. In practice episodic retrieval is often **hybrid**:
SQL filters by user + time, then vector similarity ranks by relevance.

## Semantic memory — setup, write, retrieve

**Setup (the RAG pipeline):** a vector store (Qdrant, pgvector, Pinecone) + an
embedding model + a collection (vector dim + cosine) + an ingestion job:
`source → chunk → embed → upsert(vector + text + metadata)`.

**How to decide a fact belongs in semantic memory** — it must pass all four tests:

| Test | Question | If "no" → |
|---|---|---|
| **Durable** | true beyond this conversation? | transient → [[State Management\|state]] |
| **Declarative** | a *fact*, not an *event* or *skill*? | event → episodic; skill → prompt |
| **Selective** | only relevant *sometimes* (so retrieve it)? | always + small → **system prompt** |
| **Voluminous** | too much to always keep in context? | tiny → **system prompt** |

> **The test people miss — semantic vs system prompt.** Both hold durable facts.
> A *handful, always-relevant, small* fact → **system prompt** ("refund policy = 30
> days"). A *large body where only a slice matters per query* → **semantic memory**
> (10k-item catalog → retrieve the 3 relevant). Semantic earns its complexity only
> when there's too much to always include.

Worked examples: order status → state; "asked about shipping last week" → episodic;
"refund policy 30 days" → system prompt; product catalog/docs → semantic; a few
per-user attributes → a **profile field** is simpler than vectors.

**Who decides eligibility — LLM or hardcoded?** Mostly *not* a runtime LLM check —
you rarely evaluate the 4 tests per fact at runtime:
- **Curated corpus** (docs/KB) → no per-fact decision; a **hardcoded ingestion
  pipeline** embeds the whole corpus. You applied the 4 tests *once*, at design time.
- **Facts extracted from conversations** → the only per-item decision, and it's a choice:

| Approach | How | Trade-off |
|---|---|---|
| **Hardcoded / schema** | fixed fields via rules/NER | cheap, deterministic, rigid |
| **LLM memory-manager** | "extract durable facts worth keeping" → store | flexible, costs a call (Mem0/Letta) |
| **Hybrid** | LLM extracts → code dedupes/validates/stores | flexibility + a deterministic gate |

The 4 criteria live in your **architecture** (curated), the **schema/rules**
(hardcoded), or the **extraction prompt** (LLM) — not a per-fact classifier.
Default: hardcode a schema for known attributes; add an LLM extractor only when
facts are open-ended. **Write rule:** store only durable & salient facts, and
**dedupe/update** rather than append (avoid contradictory duplicates).

**How to retrieve (the RAG knobs):** embed query → similarity top-k → inject.
Knobs: **k** (recall vs bloat), **similarity threshold**, **metadata filter**
(user/source/recency), **re-ranking**, **hybrid** dense+sparse. This is the
[[05 RAG and Knowledge Grounding]] domain — semantic memory *is* RAG applied to recall.

## Procedural memory — skills / how-to

Forms by sophistication: **system-prompt instructions → few-shot example store →
skill library → promoted tools**. **Write decision:** verified-success + reusable
+ general; mostly **manual** today (engineers encode procedures), with automatic
skill-learning via [[Reflection]] emerging. **Retrieve:** task→skill lookup, or
similar few-shot examples; inject as instructions / examples / callable tools.

> **This vault's approach (for now): procedural = manual, coded as instructions in
> the system prompt.** That collapses procedural memory into "good prompt
> instructions" — where most production agents actually sit. Revisit automatic
> skill acquisition later.

## Tools landscape
- **Semantic:** Qdrant, pgvector, Pinecone, Weaviate, Chroma.
- **Episodic:** Postgres/Mongo (recency/keyword) + vectors for semantic recall.
- **All-in-one memory layers:** Mem0, Zep, Letta (MemGPT) — handle extract/store/retrieve for you.
- **Framework:** LangGraph / LangChain memory modules.

## Likely issues
- **Context stuffing** — dumping all memory into the prompt → cost, latency, and
  the model loses the signal.
- **Relevance decay** — stale memories surface and mislead.
- **Polluted long-term memory** — writing junk in makes future retrieval worse.
- **Privacy** — storing user data as memory has compliance implications ([[PII Filtering]]).

## Tradeoffs
- **Stuff context vs retrieve** — more in-context = simpler but pricier and
  noisier; retrieval = scalable but adds latency and a relevance-quality problem.

## Example

A coding assistant remembers (semantic) your project conventions, recalls
(episodic) that you prefer pytest, and reuses (procedural) a known
"run tests → read failure → fix" sequence — all retrieved into context as needed.

## Q&A insights

**Q: How do we provision each memory type, and is "what goes where" manual each time?**
Provisioning differs per type (see table): working = no separate store (built from
state), episodic = a log table, semantic = a vector store, procedural = a skill
registry. The **type→store mapping is decided once at design time**; **per-item
writes** are usually automated (rules, or an LLM "memory manager" like Mem0/Letta),
optionally manual; **reads are always automated** at query time.

**Q: For working memory, do we fetch state from Redis/Postgres and populate it before each call?**
Yes — you load the persisted **state**, then **build working memory (the prompt)
from it** each call. Working memory isn't stored separately; it's the transient,
curated subset of state (+ retrieved memories) that fits the context window,
rebuilt every call and discarded.

**Q: State vs episodic memory — both can be in Postgres, so what's the difference?**
Role, not technology. **State** = the *current* conversation (`conversation_id`,
loaded whole each turn, active then done). **Episodic** = the *archive of past*
conversations (`user_id`, queried by relevance, persists forever). Today's state
becomes tomorrow's episodic memory when the run ends.

**Q: We search episodic memory, not load it all — but can't search in Postgres / do we need a vector DB?**
You can search in Postgres. Recency/structured search = plain SQL; keyword =
full-text (`tsvector`); only **semantic** (meaning-based) search needs embeddings —
and **pgvector** adds that to Postgres itself. A dedicated vector DB (Qdrant) is a
**scale** choice, not a requirement. Episodic retrieval is often hybrid: SQL filter
by user+time, then vector rank by relevance.

**Q: How do I decide if a fact belongs in semantic memory?**
It must pass four tests — **durable** (true beyond this run), **declarative** (a
fact, not an event or skill), **selective** (only sometimes relevant, so you
retrieve it), and **voluminous** (too much to always include). The test people
miss is **semantic vs system prompt**: a small, always-relevant fact ("refund
policy = 30 days") goes in the **system prompt**; a large body where only a slice
matters per query (a product catalog) goes in **semantic memory**. A few per-user
attributes are simpler as a **profile field** than as vectors.

**Q: Do we need an LLM to decide eligibility, or do people hardcode it?**
Mostly *not* a runtime LLM check. For a **curated corpus** there's no per-fact
decision at all — a **hardcoded pipeline** embeds the whole corpus (you applied the
4 tests once, at design time). Only **extracting facts from conversations** is a
per-item decision, and it's a choice: **hardcoded schema/rules** (cheap, rigid) vs
an **LLM memory-manager** (flexible, costs a call) vs **hybrid**. The criteria live
in your architecture, schema, or extraction prompt — not a per-fact classifier.
Default to a hardcoded schema; add an LLM extractor only when facts are open-ended.

## Related
- Part of [[Orchestrator]]'s responsibilities · headline of [[03 Memory Systems]] · [[AI Agents MOC]]
- [[State Management]] — run-scoped state (contrast)
- [[Context Building]] — where retrieved memory is injected
- [[RAG for Agents]] — semantic memory via retrieval
- [[Context Window Management]] — the working-memory constraint
