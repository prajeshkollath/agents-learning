---
title: Observability
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - observability
  - architecture
status: learning
aliases:
  - Logs and Tracing
  - Tracing
  - Agent Observability
---

# Observability

> Seeing **inside a multi-step run** — traces, logs, and metrics for every step,
> tool call, and model response — so you can debug, audit, and improve a
> non-deterministic agent. Headline of domain [[09 Observability and Debugging]].

## What it is

When an agent does something wrong across 12 steps and 4 tool calls, you need to
replay exactly what happened. Observability is the instrumentation that records
the full **trajectory**: each prompt, each model output, each tool input/result,
timings, token counts, and the final outcome — tied together by a trace id.

The three pillars:
- **Traces** — the step-by-step path of a single run (the most important for agents).
- **Logs** — structured event records.
- **Metrics** — aggregates: latency, cost, error rate, tool-success rate.

## Why it's the orchestrator's job

Only the orchestrator sits at every step, so only it can emit the spans that
stitch a run together. Without this you're blind: you can't reproduce a failure,
explain a decision, or measure quality.

## How it works

Wrap each step in a span; propagate one trace id through the whole run.

```
with trace(run_id):
    with span("llm_call"): resp = llm(ctx)      # record prompt, output, tokens
    with span("tool", name=call.name): result = execute(call)  # record I/O, timing
```

Tooling: **LangSmith, Langfuse, Arize Phoenix** (agent-native), or
**OpenTelemetry → Grafana/Datadog** (general). Feeds directly into
[[Agent Evaluation]] (traces become eval datasets) and [[Cost Control]] (token
metrics).

## Likely issues
- **Logging only inputs/outputs, not the middle** → can't see *why* it went wrong.
- **No trace id** → steps scattered, can't reconstruct one run.
- **No token/cost capture** → blind to spend.
- **Logging secrets/PII** into traces → a compliance leak ([[Security Boundary]]).

## Tradeoffs
- **Detail vs overhead/cost** — full tracing aids debugging but adds latency,
  storage, and a PII-handling burden; sample or redact in high volume.

## Example

A user reports a wrong answer; the engineer opens the trace, sees step 7 selected
the wrong tool with bad args fed by a stale memory, and fixes the retrieval — a
diagnosis impossible without the recorded trajectory.

## Q&A insights

_(To be filled as we go deeper.)_

## Related
- Part of [[Orchestrator]]'s responsibilities · headline of [[09 Observability and Debugging]] · [[AI Agents MOC]]
- [[Agent Evaluation]] — traces become eval data
- [[Cost Control]] — token/cost metrics come from here
- [[Error Handling]] — failures are recorded as spans
- [[Root Cause Analysis]] — using traces to debug
