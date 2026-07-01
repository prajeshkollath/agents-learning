---
title: Tool Calling
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - tools
  - architecture
status: learning
aliases:
  - Function Calling
  - Tool Use
  - Tool Dispatch
---


# Tool Calling

> How an agent **acts on the world** — the LLM proposes a tool + arguments, the
> orchestrator validates and executes it, then feeds the result back. Headline of
> domain [[04 Tool Use and Function Calling]]; here, the orchestrator's "act" step.

## What it is

Tools are functions the agent can invoke: search, query a DB, call an API, run
code. "Tool calling" (a.k.a. function calling) is the mechanism where the model,
given tool [[Schemas]], emits a structured request like
`refund(order=123, amount=50)` and the orchestrator runs it.

> **Selection vs execution** — the LLM *selects* the tool and args ([[Tool Selection]]);
> the orchestrator *executes* it. The model never runs code directly.

## Why it's the orchestrator's job

Execution is where reliability and safety live: validating arguments, checking
permissions ([[Guardrails]]), handling failures ([[Error Handling]]), and never
exposing secrets to the model ([[Security Boundary]]). The model only proposes.

## How it works

```
call = llm_response.tool_call            # model: which tool + args
assert schema.valid(call)                # [[Output Validation]] / [[Schemas]]
assert policy.allows(call)               # [[Guardrails]]
result = registry[call.name](**call.args)  # execute (with timeout/retry)
state.append(result)                     # feed back → [[Agent Loop]]
```

The **tool registry** maps names → functions + schemas. Good tool design
(clear names, tight schemas, helpful errors) directly improves how well the
model selects and uses them.

## The tool schema

Each tool is exposed to the model via a **schema** — `name` + `description` +
typed arguments — which is what lets the model decide *when* and *how* to call it,
and lets the orchestrator validate the call. The full anatomy (annotated example,
what it helps with, the "prompt engineering disguised as types" insight) lives in
[[Schemas]].

## Tool search — loading only relevant schemas

Every exposed tool's schema is billed on **every** call ([[Token Cost Optimization]]),
and a huge tool menu also makes [[Tool Selection]] harder. **Tool search** fixes both:
instead of putting all N schemas in context upfront, the model **searches your tool
library and loads only the relevant few** per request.

```
1. Mark most tools defer_loading: true   → their schemas are NOT in context
2. Add a tool-search tool                → this IS in context (small)
3. Model gets a request → calls search   → "find tools for booking flights"
4. Server returns matching schemas       → APPENDED to context (not swapped)
5. Model calls the real tool with a now-loaded schema
```

Matched schemas are **appended, not swapped in** — so the existing cached prefix
stays valid ([[Caching Strategies]]). You pay for ~1 search tool + only the handful
of schemas surfaced, not all 200.

On the Claude API it's a **server-side tool**, two variants —
`tool_search_tool_regex_20251119` (regex) and `tool_search_tool_bm25_20251119`
(BM25 keyword ranking):

```python
tools=[
    {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
    {"name": "book_flight", "description": "...", "input_schema": {...}, "defer_loading": True},
    # ... 200 more, all defer_loading: True
]
```

Rules (both 400 if broken): the **search tool itself must not** be deferred, and
**at least one tool must be non-deferred**. Use it only at *large* tool counts —
with ~5 tools, just load them all; the search step is pure overhead.

### Tool search ≠ tool registry

Different layers, complementary:

| | **Tool registry** | **Tool search** |
|---|---|---|
| **What** | *your* catalog: `name → schema + implementation` | mechanism selecting *which schemas enter the model's context* |
| **Lives** | your app (a data structure you build) | server-side at the API (or your own retrieval) |
| **Job** | hold + dispatch tools; run `X` when the model calls `X` | context management; surface only relevant schemas |
| **Concern** | execution + organization | token cost + selection difficulty |

The registry is your *whole toolbox* (always present — it's how you execute a call);
tool search decides *which tools to lay on the table* this request. You have both: a
registry of all 200, and search choosing the 5 to expose. You can even roll your own
search — filter the registry in code (by user role, by intent) and pass only the
subset in `tools`; the API's tool-search tool is just a managed, cache-preserving
version of that idea.

## Likely issues
- **Hallucinated tool/args** → caught by schema validation, not execution.
- **No timeout/retry** → a hung tool stalls the whole agent ([[Retries and Idempotency]]).
- **Over-broad tools** (e.g. raw SQL) → security and correctness risk ([[Sandboxed Execution]]).
- **Poor schemas/descriptions** → the model picks the wrong tool.

## Tradeoffs
- **Few coarse tools vs many fine tools** — fewer is simpler for the model but
  less precise; many is precise but raises selection difficulty.

## Example

A support agent's `issue_refund` tool: the LLM proposes the call, the
orchestrator validates the schema, checks the >$100 approval policy, executes
with an idempotency key, and returns the confirmation into the loop.

## Q&A insights

**Q: What does a tool schema look like / what does it help with?**
Captured in [[Schemas]] (the dedicated note) — `name` + `description` +
`input_schema`, driving selection, arguments, validation, and constrained
decoding; "a tool schema is prompt engineering disguised as a type definition."

## Related
- Part of [[Orchestrator]]'s responsibilities · headline of [[04 Tool Use and Function Calling]] · [[AI Agents MOC]]
- [[Tool Selection]] — the model's choice of tool (vs execution)
- [[Schemas]] — the tool's input/output contract
- [[Output Validation]] — checking the call before running it
- [[Sandboxed Execution]] — running tools safely
- [[Token Cost Optimization]] — why tool schemas are billed on every call
- [[Caching Strategies]] — caching the tool block; why changing it invalidates the cache
- [[Agent Loop]] — tool calling is the "act" phase
