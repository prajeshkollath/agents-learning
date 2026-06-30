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

## Spans and traces (the unit of a trace)

A **trace** is one entire run (everything from "user asked X"); a **span** is one
timed step *within* it — a single LLM call, tool execution, or retrieval. A trace
is *made of* spans, and spans **nest** into a tree that mirrors what the agent did:

```
TRACE  run_id=abc123  "summarize unpaid invoices"        [2.4s]
├─ SPAN  llm_call #1     decide what to do                [0.6s]
├─ SPAN  tool: search_invoices(status="unpaid")           [0.3s]
│   └─ SPAN  db_query    SELECT ... WHERE status='unpaid' [0.12s]   ← child of the tool span
├─ SPAN  llm_call #2     summarize results                [0.9s]
└─ SPAN  tool: send_email(...)                            [0.4s]
```

The parent/child nesting is what shows **causality** (the `db_query` happened
*inside* `search_invoices`), not just a flat list. Each span carries:

| Field | Example | Used to find |
|-------|---------|--------------|
| **name** | `tool: search_invoices` | what the step was |
| **start/end → duration** | 0.3s | the *slow* step (latency) |
| **parent span id** | — | which step it ran inside of |
| **status** | ok / error | the *failed* step |
| **attributes** | prompt, output, tokens, args, result | *why* it went wrong |

The `with span(...)` block *is* the span's lifetime (enter = start, exit = end +
save); the shared trace id stitches them into one tree. "Span" is **OpenTelemetry**
vocabulary; some agent tools call it a "step" or "observation" — same concept.

## Instrumenting: how spans get captured

Capture depends on the **integration level**, and real agents mix all three:

- **Auto-instrumentation** — attach a **wrapped LLM client** or a framework
  **callback handler**, and every LLM/tool/retrieval call emits a span *for you*,
  with prompts, outputs, and token counts already filled in.
- **Decorator/wrapper** — tag any function (`@observe()`) to make it a span.
- **Manual** — open spans yourself with `with span(...)`.

The key nuance: **"automatic" only works where the tool can see your calls.** It
hooks into things it recognizes (the LLM SDK, a framework like LangChain). Your own
custom glue code (a `rank_results()` fn, a raw DB query) is invisible to it — those
spans you add manually. So: **LLM + tool spans come free; your business-logic spans
you add.**

### Connecting the tool — 3 steps

```bash
# 1. install the SDK
pip install langfuse            # or langsmith, or opentelemetry-sdk

# 2. credentials via env vars (keys never in code → Security Boundary)
export LANGFUSE_PUBLIC_KEY=pk-...
export LANGFUSE_SECRET_KEY=sk-...
export LANGFUSE_HOST=https://cloud.langfuse.com
```

```python
# 3. hook into code — one of:
from langfuse.openai import openai        # (a) wrapped client → every LLM call auto-traced
from langfuse.decorators import observe   # (b) decorator → any fn becomes a span

@observe()
def search_invoices(status): ...

# (c) framework callback handler, passed once:
#     agent.run(query, config={"callbacks": [CallbackHandler()]})
# (d) OpenTelemetry exporter to any backend (Grafana/Datadog/Phoenix):
#     export OTEL_EXPORTER_OTLP_ENDPOINT=https://your-collector:4318
```

### What connecting does under the hood

The SDK doesn't ship each span the instant it closes (that would add latency to
every step). It **buffers spans in memory → a background thread batches them →
sends async over HTTPS** to the backend. So tracing is **fire-and-forget and
non-blocking** — the agent never waits on the network. **Caveat:** in a
short-lived script you must call `flush()` / `shutdown()` before exit or the last
buffered spans are lost; long-running servers flush continuously, so it's a
non-issue there.

## Q&A insights

- **"What's a span?"** — One timed unit of work inside a trace: *this operation
  started here, ended there, here's what happened*. Trace = whole run, span = one
  nested step. It's the unit that matters for agents because debugging a 12-step
  run means inspecting the 12 spans — which was slow (duration), which failed
  (status), and why (attributes).

- **"Do spans get captured automatically?"** — Only where the tool can *see* your
  calls. A wrapped client / framework callback auto-emits spans for LLM, tool, and
  retrieval calls; but your custom glue code is invisible and needs a decorator or
  manual `with span(...)`. LLM + tool spans come free; business-logic spans you add.

- **"How do we connect the observability tool?"** — Install SDK → set credential
  env vars → hook in via a wrapped client, `@observe()` decorator, framework
  callback handler, or an OpenTelemetry exporter pointed at any backend.

- **"What does connecting do under the hood?"** — Spans are buffered and sent
  async/batched over HTTPS, so tracing never blocks the agent. A short-lived script
  must `flush()` before exit or it loses the last spans.

## Related
- Part of [[Orchestrator]]'s responsibilities · headline of [[09 Observability and Debugging]] · [[AI Agents MOC]]
- [[Agent Evaluation]] — traces become eval data
- [[Cost Control]] — token/cost metrics come from here
- [[Error Handling]] — failures are recorded as spans
- [[Root Cause Analysis]] — using traces to debug
