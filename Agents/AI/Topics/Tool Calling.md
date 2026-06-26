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
- [[Agent Loop]] — tool calling is the "act" phase
