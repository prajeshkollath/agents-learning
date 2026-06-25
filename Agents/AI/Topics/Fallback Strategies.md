---
title: Fallback Strategies
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - architecture
  - orchestration
  - reliability
status: learning
aliases:
  - Fallbacks
  - Fallback Calls
  - Graceful Degradation
---

# Fallback Strategies

> When the primary path fails, **switch to an alternative** — another model,
> tool, or simpler behavior — instead of failing the whole run. Graceful
> degradation for non-deterministic systems.

## What it is

A fallback is a pre-planned plan B. Where [[Retries and Idempotency]] re-attempts
the *same* call, a fallback **changes the call**: different model, different
provider, different tool, cached/default answer, or human handoff.

Common fallback axes:
- **Model fallback** — primary model overloaded/down → secondary or cheaper model.
- **Provider fallback** — one vendor's API fails → another's.
- **Tool fallback** — preferred data source down → alternate source.
- **Degraded answer** — can't fully solve → return a partial/cached result or a safe default.
- **Human fallback** — escalate to a person ([[Guardrails]] approval path).

## Why it's the orchestrator's job

Only the orchestrator sees the failure and controls routing, so only it can pivot
to plan B. Fallbacks pair with **fail-safe defaults**: when unsure, degrade to the
*safe* option, never the risky one.

## How it works

```
try:
    return strong_model(ctx)
except (Overloaded, Timeout):
    try:    return cheaper_model(ctx)     # model fallback
    except: return cached_or_default()    # degraded answer
```

Often combined with a **circuit breaker**: after repeated primary failures, skip
straight to the fallback for a cooldown period instead of retrying each time.

## Likely issues
- **No fallback** → one dependency's outage takes down the whole agent.
- **Silent quality drop** → falling back to a weaker model without flagging it.
- **Fallback to a *less safe* option** → violates fail-safe-defaults.
- **Cascading fallbacks** with no final floor → still ends in an unhandled error.

## Tradeoffs
- **Coverage vs complexity** — more fallback paths = more resilience but more code
  and more states to test/observe.
- **Quality vs availability** — a degraded answer keeps the agent up but may be
  worse; decide which matters per use case.

## Example

A production assistant calls Opus; on a `529 overloaded` it falls back to a
smaller model, and if that also fails, returns a cached FAQ answer with a "live
help" link — the user always gets *something*, and the downgrade is logged.

## Q&A insights

_(To be filled as we go deeper.)_

## Related
- Part of [[Orchestrator]]'s responsibilities · [[02 Agent Architecture and Orchestration]] · [[AI Agents MOC]]
- [[Error Handling]] — fallbacks trigger after errors
- [[Retries and Idempotency]] — retry the same call first, then fall back
- [[Model Selection Tradeoffs]] — choosing primary vs fallback models
- [[Guardrails]] — fail-safe defaults and human handoff
