---
title: Context Building
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - architecture
  - orchestration
  - prompting
status: learning
aliases:
  - Context Engineering
  - Prompt Assembly
  - Context Assembly
---

# Context Building

> Assembling the **exact prompt** the LLM sees each step — from system
> instructions, state, retrieved memory, and tool specs — within the context
> window. Often called *context engineering*; it's where most agent quality
> (and cost) is won or lost.

## What it is

Every LLM call is a fresh prompt the orchestrator constructs. Context building
is the act of choosing what goes in and in what order: the system prompt, the
running [[State Management]] history, relevant [[Agent Memory]], available
[[Tool Calling]] schemas, and the current input — then fitting it into the
[[Context Window Management|context window]].

## Why it's the orchestrator's job

The model can only reason over what's in its context. Garbage or bloat in →
bad or expensive out. The orchestrator curates context deterministically so the
model gets exactly the right information, no more.

## How it works

A typical assembly, in priority order:

```
prompt = [
  system_prompt,                       # role, rules, output format
  retrieved_memories,                  # [[Agent Memory]] (top-k relevant)
  tool_specs,                          # [[Schemas]] of available tools
  compacted_history(state),            # [[State Management]], trimmed/summarised
  current_input,
]
assert tokens(prompt) < WINDOW         # fit the budget
```

Key techniques when it won't fit: **truncation**, **summarisation/compaction**
of old turns, **retrieval** instead of inclusion, and **prioritisation** (keep
the system prompt and recent steps; drop or compress the middle).

## Likely issues
- **Overflow** — too much context → truncation errors or silent dropping.
- **Lost-in-the-middle** — models attend worse to mid-context info; order matters.
- **Stale/irrelevant context** — pulling in the wrong memories degrades answers.
- **Cost blow-up** — stuffing context is the #1 driver of token spend ([[Cost Control]]).

## Tradeoffs
- **Include vs retrieve vs summarise** — more raw context is simpler but costlier
  and noisier; retrieval/summarisation save tokens but add latency and a
  quality-of-selection problem.

## Example

A long support chat: the orchestrator keeps the system prompt + last 6 turns
verbatim, summarises the earlier 40 turns into 3 lines, and retrieves the 2
most relevant KB articles — keeping the prompt sharp and under budget.

## Q&A insights

_(To be filled as we go deeper.)_

## Related
- Part of [[Orchestrator]]'s responsibilities · [[02 Agent Architecture and Orchestration]] · [[AI Agents MOC]]
- [[State Management]] / [[Agent Memory]] — sources fed into context
- [[Context Window Management]] — the hard size constraint
- [[Schemas]] — tool specs included in context
- [[Caching Strategies]] — prompt caching to cut context cost
