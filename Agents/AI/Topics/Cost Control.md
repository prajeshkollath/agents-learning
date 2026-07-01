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

## Reading a turn's usage — what the API actually reports

Every response carries a **`usage`** object. The critical subtlety: input is split
across **three** fields, not one — because of [[Caching Strategies|prompt caching]]:

| Field | What it is | Price multiplier (× base input rate) |
|-------|-----------|--------------------------------------|
| `input_tokens` | uncached input, processed fresh | **1×** |
| `cache_read_input_tokens` | input served from cache | **~0.1×** (≈90% cheaper) |
| `cache_creation_input_tokens` | input *written* to cache this turn | **1.25×** (5-min) / **2×** (1-hr) |
| `output_tokens` | the model's generated response | separate **output** rate |

**The true input for a turn = the sum of all three input fields.** `input_tokens`
*alone is only the uncached remainder* — if the run's prefix is cached, it can read
tiny (e.g. 4k) while the real prompt was 50k, with the other 46k hiding in
`cache_read_input_tokens`. Summing only `input_tokens` for a budget silently
**undercounts**. (Anthropic's exact field names; other providers expose the same
concepts.)

### What counts as "input" on any given turn

The LLM API is **stateless** — it remembers nothing between calls; *you* resend the
whole conversation every turn. So a turn's input is the entire payload on the wire:

- **system prompt** + **tool definitions** (rendered first, `tools → system → messages`),
- **all prior turns** — every `user` *and* `assistant` message, including the
  `tool_use` blocks (the model's calls) and `tool_result` blocks (your results),
- the **new user message** (the only genuinely new text).

This is *why tokens build up*: turn 7's input ≈ (turns 1–6 in full) + system + tools
+ your new question. It grows ~linearly with conversation length — the real driver
behind "bloated context is the cost, not output."

## Cost is per-bucket **and** per-model

You can't price input with one number. Each bucket has its own multiplier, and rates
are **per model** (route a cheap turn to Haiku, a hard one to Opus → each turn's
`usage` is multiplied by *that turn's* model rates, see [[Model Selection Tradeoffs]]).

```
cost = input_tokens                 × in_rate
     + cache_read_input_tokens      × in_rate × 0.1
     + cache_creation_input_tokens  × in_rate × 1.25     # × 2 for 1-hour cache
     + output_tokens                × out_rate
```

A cache **read** is cheap (~0.1×); a cache **write** costs *more* than a normal token
(1.25×/2×) — you pay a one-time premium to write, to save ~90% on every later read.
Worked turn (Opus-tier $5/1M in, $25/1M out; 50k input split 4.2k fresh / 44.8k
cache-read / 1k cache-write, 1k output): ≈ **$0.075** — vs ≈$0.25 if you'd naively
priced all 50k input at the full rate (a ~4× overstatement). This per-bucket,
per-model accounting **is** the "accumulate usage across the loop" logic — the
stateless model holds no running total, so the orchestrator must.

## Q&A insights

- **"When I send turn 7, does Claude tell me the input — history, tools, system,
  user?"** — Yes: `usage` reports it, and **all** of those count. Because the API is
  stateless you resend system + tools + every prior user/assistant turn (including
  `tool_use`/`tool_result` blocks) + the new message — that whole payload is the
  turn's input, which is exactly why tokens build up turn over turn.

- **"Is the input one number?"** — No. It's split across `input_tokens` (uncached),
  `cache_read_input_tokens`, and `cache_creation_input_tokens`. **`input_tokens`
  alone is only the uncached remainder** — sum all three for the true input, or you
  undercount (often badly) on a cached conversation.

- **"Is the price different across the three buckets?"** — Yes. Uncached input = 1×,
  cache-read ≈ 0.1×, cache-write = 1.25× (5-min TTL) or 2× (1-hr TTL), output on its
  own rate. So a cache *read* is cheap but a cache *write* costs **more** than a
  normal token — a one-time premium that pays off across later reads. Cost logic must
  apply **per-bucket** multipliers **per-model**, not one flat input price.

## Related
- Part of [[Orchestrator]]'s responsibilities · [[12 Production and Cost Engineering]] · [[AI Agents MOC]]
- [[Token Cost Optimization]] — making each call cheaper (vs capping)
- [[Caching Strategies]] — prompt/semantic caching to cut cost
- [[Termination Conditions]] — budgets as a stop condition
- [[Observability]] — where cost metrics are captured
- [[Model Selection Tradeoffs]] — routing by cost/capability
