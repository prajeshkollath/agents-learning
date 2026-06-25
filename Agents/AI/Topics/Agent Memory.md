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

## How it works

- **Write path** — after a run (or step), persist salient facts/events to the
  store (episodic → logs/DB; semantic → embeddings in a vector DB).
- **Read path** — on each step, retrieve the most relevant memories (recency,
  similarity, importance) and inject them into the prompt.

```
relevant = memory.retrieve(query=current_goal, k=5)   # similarity/recency
ctx = build_context(state, memories=relevant)         # → [[Context Building]]
```

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

_(To be filled as we go deeper.)_

## Related
- Part of [[Orchestrator]]'s responsibilities · headline of [[03 Memory Systems]] · [[AI Agents MOC]]
- [[State Management]] — run-scoped state (contrast)
- [[Context Building]] — where retrieved memory is injected
- [[RAG for Agents]] — semantic memory via retrieval
- [[Context Window Management]] — the working-memory constraint
