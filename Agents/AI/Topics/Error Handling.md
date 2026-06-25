---
title: Error Handling
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - architecture
  - orchestration
  - reliability
status: learning
aliases:
  - Agent Error Handling
  - Failure Handling
---

# Error Handling

> Catching and responding to failures — tool errors, model errors, timeouts,
> bad output — **without crashing the run**. The difference between a demo and a
> production agent.

## What it is

Things fail constantly in agents: a tool throws or times out, an API returns
500, the model returns garbage or refuses, a rate limit hits. Error handling is
the orchestrator's strategy for each failure class: recover, retry, fall back,
ask the model to adjust, or stop cleanly.

## Why it's the orchestrator's job

The LLM can't catch a network exception. The orchestrator wraps every external
call, decides what each failure means, and keeps the loop alive or ends it
gracefully — turning a crash into a handled event the agent can reason about.

## How it works

A key pattern: **feed the error back to the model as an observation**, so it can
adapt — but cap how often.

```
try:
    result = execute(call, timeout=T)
except ToolError as e:
    state.append(error_observation(e))   # let the LLM see + react
    if fail_count[call.name] > N:         # repeated failure → stop
        raise Terminate("tool keeps failing")
```

Failure classes and typical responses:
- **Transient** (timeout, 5xx, rate limit) → retry with backoff ([[Retries and Idempotency]]).
- **Permanent** (bad input, 4xx) → don't retry; surface to the model or user.
- **Model errors** (malformed output, refusal) → repair/re-prompt ([[Output Validation]]).
- **Unrecoverable** → terminate cleanly and report ([[Termination Conditions]]).

## Likely issues
- **Swallowing errors silently** → the agent "succeeds" with wrong/empty data.
- **Retrying permanent errors** → wasted calls and loops.
- **Not surfacing errors to the model** → it can't self-correct.
- **No cap on error loops** → spins on the same failure.

## Tradeoffs
- **Fail fast vs recover** — failing fast is debuggable but brittle; aggressive
  recovery is resilient but can hide real problems and burn cost.

## Example

A research agent's search tool times out: the orchestrator retries twice with
backoff, then appends "search unavailable" to context so the model tries a
different source — instead of the whole run dying.

## Q&A insights

_(To be filled as we go deeper.)_

## Related
- Part of [[Orchestrator]]'s responsibilities · [[02 Agent Architecture and Orchestration]] · [[AI Agents MOC]]
- [[Retries and Idempotency]] — handling transient failures safely
- [[Fallback Strategies]] — switching path when recovery fails
- [[Output Validation]] — handling malformed model output
- [[Termination Conditions]] — stopping on unrecoverable failure
