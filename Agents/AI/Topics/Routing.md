---
title: Routing
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - architecture
  - orchestration
status: learning
aliases:
  - Agent Routing
  - Step Routing
---

# Routing

> Deciding **what happens next** — which step, branch, tool-set, model, or
> sub-agent handles the current input. Routing is the orchestrator's
> "switchboard".

## What it is

Within the [[Agent Loop]], routing is the choice of *path*. Examples: send a
billing question to the billing tools but a coding question to the code tools;
escalate to a bigger model for hard inputs; hand off to a specialist sub-agent.

## Why it's the orchestrator's job

Routing is control flow, and control flow should be **predictable**. Who makes
the routing decision is itself a design choice (see
[[Orchestrator vs LLM Responsibilities]]):
- **Code-driven routing** — rules/classifiers in the orchestrator. Deterministic, testable, cheap.
- **LLM-driven routing** — the model picks the path. Flexible, handles ambiguity, less predictable.
- **Hybrid** — LLM classifies intent, code maps intent → path.

## How it works

A common pattern is an explicit **router node**: classify the input (by rules,
embeddings, or a cheap LLM call), then dispatch to the matching handler.

```
intent = classify(input)        # rules / embedding / small LLM
handler = ROUTES[intent]        # deterministic mapping
return handler(input)
```

Routing also covers **model routing** (cheap model for easy steps, strong model
for hard ones) and **sub-agent routing** in [[Multi-Agent Systems]] (a supervisor
routing work to workers).

## Tradeoffs
- **Code routing** is reliable but brittle to inputs you didn't anticipate.
- **LLM routing** adapts but can mis-route, and costs a call.
- **More routes** = more flexibility but more paths to test and observe.

## Likely issues
- Mis-routing sends an input down the wrong path silently → wrong answer.
- An unhandled intent with no default route → dead end.
- LLM router used where a cheap classifier would be more reliable.

## Example

A support agent routes "where's my refund?" to billing tools, "app keeps
crashing" to diagnostics, and anything ambiguous to a clarifying question —
the router decides before any expensive work happens.

## Q&A insights

_(To be filled as we go deeper.)_

## Related
- Part of [[Orchestrator]]'s responsibilities · [[02 Agent Architecture and Orchestration]] · [[AI Agents MOC]]
- [[Agent Loop]] — routing happens inside the loop
- [[Orchestrator vs LLM Responsibilities]] — code vs LLM routing
- [[Multi-Agent Systems]] — routing work to sub-agents
- [[Model Selection Tradeoffs]] — routing between models by difficulty
