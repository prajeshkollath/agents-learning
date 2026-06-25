---
title: State Management
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - architecture
  - orchestration
status: learning
aliases:
  - State
  - Agent State
  - Execution State
---

# State Management

> Holding the agent's **live execution state** — where it is in the task right
> now — and persisting it so runs survive restarts and scale across machines.
> The LLM is stateless; the orchestrator remembers.

## What it is

State is the running record of a single agent run: the goal, the message/step
history, the scratchpad, intermediate tool results, the current step number,
and any flags. It is *not* the same as [[Agent Memory]] — see below.

> **State vs Memory.** **State** = the live, run-scoped working set (this run's
> steps so far). **Memory** = longer-term recall reused *across* runs (past
> conversations, learned facts). State is "where am I in this task"; memory is
> "what do I know from before."

## Why it's the orchestrator's job

Each LLM call is independent and forgets everything. For the agent to take step
2 informed by step 1, the orchestrator must carry that history and feed it back
in via [[Context Building]]. Persisting state externally is also what makes the
orchestrator **stateless and scalable** ([[Stateless Orchestrator Design]]).

## How it works

The core operation is **load → mutate → save** on every loop iteration; the only
question is *what the store is*.

```
state = store.load(run_id) or init(goal)   # load this conversation's state
state = run_agent_step(state, input)       # append step, call LLM, run tools
store.save(run_id, state)                  # persist after each step → crash-safe
```

### What "state" actually looks like

For one conversation it's a single serializable blob:

```json
{
  "conversation_id": "conv_8a3f",
  "user_id": "user_42",
  "messages": [
    {"role": "user", "content": "Where's my refund for order 1234?"},
    {"role": "tool", "name": "get_order", "result": {"id": 1234, "refund": "pending"}},
    {"role": "assistant", "content": "Your refund is pending, issued in 2 days."}
  ],
  "scratchpad": {"order_id": 1234, "refund_status": "pending"},
  "step": 4,
  "status": "running"
}
```

### Storage options

| Option | Where the blob lives | Tools | When |
|---|---|---|---|
| **In-memory** | a `dict` keyed by `run_id` | plain Python | prototype, single process |
| **Redis** (hot cache) | `session:conv_8a3f → "{json}"`, with TTL | Redis; Upstash, ElastiCache, Memorystore | fast per-step reads, multi-instance, expirable sessions |
| **Postgres** (durable) | `sessions(conversation_id, state JSONB, ...)` row | Postgres + SQLAlchemy; Supabase, Neon, RDS | production, durable, queryable, auditable |
| **Checkpointed / durable engine** | the run's recorded history | LangGraph checkpointer, Temporal | long runs, crash-resume ([[Durable Execution]]) |

### Real example — Postgres vs Redis (what gets stored)

**Postgres:** one table, one row per conversation, the blob in a `JSONB` column:

```sql
CREATE TABLE sessions (
  conversation_id TEXT PRIMARY KEY,
  user_id TEXT, state JSONB, status TEXT, updated_at TIMESTAMPTZ DEFAULT now()
);
-- load:  SELECT state FROM sessions WHERE conversation_id=$1
-- save:  INSERT ... ON CONFLICT (conversation_id) DO UPDATE SET state=$2, ...
```

**Redis:** the same blob as a string value under a keyed name, auto-expiring:

```
SET session:conv_8a3f '{...json...}' EX 86400      # 24h TTL
GET session:conv_8a3f                              # sub-ms read each step
```

**Two-tier (real production):** Redis is the *hot* copy (fast reads each step),
Postgres is the *durable* source of truth; on a Redis miss, rehydrate from Postgres.

```python
state = redis.get(key) or db.load(cid)   # hot first, fall back to durable
state = run_agent_step(state, msg)
redis.set(key, state, ex=86400); db.save(cid, state)   # write both
```

Use two-tier only when per-step latency actually hurts — for most agents, plain
**Postgres-JSONB is enough**.

### Does state include the message history? (and keeping it small)

Yes — the `messages` array lives *inside* the blob, so the `state` column holds
the **whole conversation history**, and it's **rewritten and grows every turn**:

```
turn 1: messages = [u1, a1]                 → save
turn 2: messages = [u1, a1, u2, a2]         → save
turn 3: messages = [u1, a1, u2, a2, u3, a3] → save
```

Why store it all? The LLM is **stateless** — to answer turn 5 it must be re-shown
turns 1–4, so the orchestrator keeps them and replays them via [[Context Building]].

**Storage vs context — what actually needs to stay small:**
- **Storage** (the blob in Postgres) is *cheap* — keeping full history is fine and
  useful for audit/replay.
- **Context** (what you send the LLM each call) is what costs **tokens**, and the
  whole history is re-sent *every* call. **This** is what must be minimised.

So you don't necessarily stop *storing* messages — you stop *sending all of them*.
The context window is the **constraint**; the techniques that meet it (all
[[Context Window Management]] / [[Context Building]]):
- **Trim / sliding window** — send only the last N turns.
- **Summarise** — compress old turns into a short recap.
- **Retrieve (RAG)** — send only the relevant past turns, not all.

Optionally also **compact the stored state** (write the summary back) so the blob
itself stops growing unbounded — do this when loading/saving the blob gets heavy,
not just to save tokens.

**Data-modelling choice:**

| Approach | How | Trade-off |
|---|---|---|
| **Single blob** | whole state incl. `messages[]` in one JSONB column, rewritten each turn | simplest; rewrites everything each turn; grows large |
| **Normalized** | a `messages` table, one row per message (append-only) + a `sessions` row | append not rewrite; scales to long chats; queryable; more code |

## Likely issues
- **State in process memory** → a restart wipes the run; can't scale horizontally.
- **Unbounded state** → history grows past the context window ([[Context Window Management]]).
- **Shared/leaky state** → two runs' contexts bleed together (key by run_id).
- **No checkpointing** → a crash at step 9 restarts from step 0.

## Cost: storage vs token cost

Two costs — the second is the one people miss:

- **Storage cost (small).** State is text. Millions of sessions in Postgres = GBs
  = cents-to-dollars. Redis is pricier (it's RAM, ~$15–50/mo managed for small
  workloads); Postgres on disk is cheaper (Neon/Supabase have free tiers).
- **Token cost (the real driver).** State feeds [[Context Building]], so every
  byte of state becomes **input tokens on every LLM call**. A bloated history
  inflates the cost *and* latency of every step, across the whole loop. So **state
  *size* is a token-cost problem** — trim/summarise old turns rather than carry
  everything ([[Cost Control]]).

## Tradeoffs & how to choose

| Concern | In-memory | Redis | Postgres | Durable engine |
|---|---|---|---|---|
| Survives crash/restart | ❌ | ⚠️ configurable | ✅ | ✅ |
| Horizontal scale | ❌ | ✅ | ✅ | ✅ |
| Speed | fastest | very fast | fast | varies |
| Queryable / auditable | ❌ | ❌ | ✅ | ✅ |
| Setup complexity | none | low | low–med | med–high |

**Default:** start with **Postgres-JSONB** for anything real — cheap, durable,
queryable, won't outgrow it for a long time. Add **Redis** only when per-step read
latency hurts. Go to a **durable engine** only for long-running / must-resume
agents ([[Durable Execution]]). The central tension is **simplicity vs
durability/scale** — in-memory is zero-effort but can't survive a restart or run
two instances (the [[Stateless Orchestrator Design]] point).

## Q&A insights

**Q: How do I actually maintain state with Redis or Postgres — what gets stored?**
You store one serializable blob per conversation (messages + scratchpad + step +
status). **Postgres:** one row per conversation with the blob in a `JSONB` column,
keyed by `conversation_id`; load/save each step. **Redis:** the same blob as a
string value under `session:{id}` with a TTL; sub-ms reads. **Two-tier:** Redis
hot + Postgres durable, rehydrate from Postgres on a cache miss. Default to plain
Postgres-JSONB unless per-step latency hurts. See the worked example above.

**Q: When do I need a durable engine instead?**
When runs are long, must survive crashes/redeploys, or **wait hours for a human**
— there you stop hand-writing load/save/resume and let an engine checkpoint every
step automatically. That's [[Durable Execution]] (Level 6 on the
[[Orchestrator Maturity Ladder]]), overkill for short agents.

**Q: Does the blob contain the message history, and does it grow each turn?**
Yes — `messages[]` is inside the blob, so `state` holds the whole conversation,
rewritten and growing every turn (the LLM is stateless and must be re-shown the
history each call). **Refinement:** storage is cheap, but **context** isn't — the
full history is re-sent to the model every call, so minimise what you *send* (trim
/ summarise / retrieve) to stay under the [[Context Window Management|context window]]
and control [[Cost Control|cost]], even while keeping full history in storage for
audit. Optionally compact the stored state too. Single blob vs a normalized
`messages` table is a modelling choice (simplicity vs scale).

## Related
- Part of [[Orchestrator]]'s responsibilities · [[02 Agent Architecture and Orchestration]] · [[AI Agents MOC]]
- [[Agent Memory]] — longer-term recall (contrast with state)
- [[Context Building]] — state is fed back into the prompt from here
- [[Stateless Orchestrator Design]] — externalize state to scale
- [[Durable Execution]] — checkpoint state to resume
