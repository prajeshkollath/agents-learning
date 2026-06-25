---
title: Schemas
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - tools
  - architecture
status: learning
aliases:
  - Tool Schemas
  - JSON Schema
  - Structured Output Schema
---

# Schemas

> The **typed contracts** for structured data crossing the LLM boundary: what a
> tool accepts, and what shape a response must take. Schemas are how fuzzy model
> output becomes safe, machine-usable data.

## What it is

A schema (usually JSON Schema, often authored via Pydantic) declares fields,
types, required-ness, and constraints. Two uses in agents:
- **Tool input schemas** — define each tool's parameters so the model knows how
  to call it ([[Tool Calling]]) and the orchestrator can validate the call.
- **Output schemas** — force the model to return data in a fixed shape
  (structured output), so downstream code can rely on it.

## Why it's the orchestrator's job

The model emits text/tokens; the orchestrator needs *typed data*. Schemas are
the contract that bridges them — they tell the model the required shape and give
the orchestrator something concrete to validate against ([[Output Validation]]).
They also double as documentation the model reads to select tools well.

## How it works

```python
class RefundArgs(BaseModel):          # Pydantic → JSON Schema
    order_id: int
    amount: float = Field(gt=0)
    reason: str

# schema is sent to the model AND used to validate its output
call = validate(llm_response, RefundArgs)   # raises on mismatch → retry
```

Many providers enforce schemas server-side (structured output / tool-use mode),
making malformed output much rarer — but the orchestrator should still validate.

## Likely issues
- **Loose schemas** (everything optional/string) → the model fills them sloppily.
- **Over-strict schemas** → frequent validation failures and retries.
- **Schema ≠ business rules** — a schema checks *shape*, not *validity*
  (amount > 0 is schema; "refund ≤ order total" is [[Guardrails]]).
- **Drift** — code changes but the schema the model sees doesn't.

## Tradeoffs
- **Tight vs permissive** — tight schemas give reliable data but more retries;
  permissive schemas are forgiving but push validation work downstream.

## Example

The `issue_refund` tool exposes a `RefundArgs` schema; the model must produce
`{order_id, amount, reason}` with `amount > 0`, or the call is rejected before
it ever touches the payment API.

## Q&A insights

_(To be filled as we go deeper.)_

## Related
- Part of [[Orchestrator]]'s responsibilities · [[04 Tool Use and Function Calling]] · [[AI Agents MOC]]
- [[Tool Calling]] — schemas define the callable tools
- [[Output Validation]] — runtime checking against the schema
- [[Structured Output Prompting]] — prompting for schema-shaped output
- [[Guardrails]] — business rules beyond shape
