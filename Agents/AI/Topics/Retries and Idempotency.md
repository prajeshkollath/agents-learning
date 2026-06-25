---
title: Retries and Idempotency
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - architecture
  - orchestration
  - reliability
status: learning
aliases:
  - Retries
  - Idempotency
  - Retry and Idempotency
---

# Retries and Idempotency

> **Retry** transient failures so flaky calls still succeed — and make actions
> **idempotent** so a retry (or an LLM repeat) can't do the same thing twice.
> These two belong together: retries without idempotency cause double-actions.

## What it is

- **Retry** — re-attempt a failed call, usually with **exponential backoff** and
  jitter, up to a max attempts.
- **Idempotency** — designing an action so performing it twice has the same
  effect as once. Achieved with an **idempotency key**: a unique id the
  downstream system uses to dedupe repeats.

## Why it's the orchestrator's job

Networks and model APIs fail intermittently; retries turn that into reliability.
But agents are doubly risky: a retry *and* a non-deterministic LLM can both cause
a repeat. The orchestrator must guarantee that "do it again" never means "charge
the customer again."

## How it works

```
key = idempotency_key(run_id, step)        # stable per logical action
for attempt in range(MAX):
    try:
        return charge(amount, idem_key=key) # downstream dedupes on key
    except Transient:
        sleep(backoff(attempt) + jitter)    # 1s, 2s, 4s ...
raise GiveUp
```

The downstream service stores seen keys; a repeat with the same key returns the
original result instead of acting again.

## Likely issues
- **Retries without idempotency** → duplicate refunds, double emails, double rows.
- **Retrying non-idempotent or permanent errors** → compounding damage.
- **No backoff/jitter** → thundering-herd hammering a struggling service.
- **Idempotency key not stable** (e.g. includes a timestamp) → dedup fails.

## Tradeoffs
- **More retries** = higher success under flakiness but higher latency and cost;
  tune attempts/backoff to the failure profile.
- Idempotency adds design effort (keys, dedup store) but is mandatory for any
  action with side effects.

## Example

The refund agent generates an idempotency key per refund step; a network blip
triggers a retry, the payment API sees the same key and returns the original
confirmation — the customer is refunded exactly once.

## Q&A insights

_(To be filled as we go deeper.)_

## Related
- Part of [[Orchestrator]]'s responsibilities · [[02 Agent Architecture and Orchestration]] · [[AI Agents MOC]]
- [[Error Handling]] — retries are one response to failures
- [[Fallback Strategies]] — what to do when retries are exhausted
- [[Tool Calling]] — the calls being retried
- [[Durable Execution]] — checkpointing complements idempotency
