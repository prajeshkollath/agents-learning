---
title: Cost Control
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - cost
  - architecture
  - orchestration
status: learning
aliases:
  - Cost
  - Token Budgeting
  - Cost Management
---

# Cost Control

> Tracking and **capping spend** per run — tokens, calls, and dollars — so an
> agent can't quietly run up a huge bill. The orchestrator accounts for every
> call; optimisation techniques live in [[Token Cost Optimization]].

## What it is

Every LLM call costs tokens, and agents make many calls in loops — cost
compounds fast. Cost control is the orchestrator's accounting and enforcement:
measure token usage per step, enforce a per-run budget, and stop or degrade when
it's exceeded.

> **Control vs optimisation.** *Cost control* = measure + cap + stop (this note,
> an orchestrator runtime job). *Cost optimisation* = make each call cheaper
> (caching, smaller models, fewer steps) → [[Token Cost Optimization]].

## Why it's the orchestrator's job

The model doesn't know or care what it costs. The orchestrator reads the usage
field on each response, sums it against a budget, and acts — it's the only place
spend can actually be enforced ([[Termination Conditions]]).

## How it works

```
budget = TokenBudget(max_tokens=50_000, max_usd=2.0)
...
budget.add(resp.usage)                 # accumulate per call
if budget.exceeded():
    raise Terminate("budget exhausted") # stop or degrade ([[Fallback Strategies]])
```

Levers the orchestrator pulls:
- **Per-run budgets** + hard stop.
- **Model routing** — cheap model for easy steps, strong only when needed ([[Model Selection Tradeoffs]]).
- **Step caps** — fewer loops = fewer calls ([[Termination Conditions]]).
- **Prompt caching** + context trimming to shrink input tokens ([[Context Building]]).
- **Cost metrics** per run for monitoring ([[Observability]]).

## Likely issues
- **No per-run cap** → one pathological loop bills hundreds of dollars.
- **Ignoring input tokens** → bloated context is often the real cost driver, not output.
- **Per-call view only** → miss that cost compounds across the loop and across users.
- **No alerting** → you discover the spend on the invoice.

## Tradeoffs
- **Cost vs capability/quality** — cheaper models and tighter budgets save money
  but can lower answer quality or truncate work; set budgets to the task's value.

## Example

The refund agent caps each run at 50k tokens / $2; a stuck run hits the cap,
terminates with the reason logged, and alerts ops — instead of looping unnoticed
and racking up cost across thousands of sessions.

## Q&A insights

_(To be filled as we go deeper.)_

## Related
- Part of [[Orchestrator]]'s responsibilities · [[12 Production and Cost Engineering]] · [[AI Agents MOC]]
- [[Token Cost Optimization]] — making each call cheaper (vs capping)
- [[Caching Strategies]] — prompt/semantic caching to cut cost
- [[Termination Conditions]] — budgets as a stop condition
- [[Observability]] — where cost metrics are captured
- [[Model Selection Tradeoffs]] — routing by cost/capability
