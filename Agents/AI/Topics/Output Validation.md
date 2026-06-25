---
title: Output Validation
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - architecture
  - orchestration
  - reliability
status: learning
aliases:
  - Output Parsing
  - Response Validation
---

# Output Validation

> The **runtime check** on a single LLM response *before the orchestrator acts on
> it*: is it well-formed, schema-valid, and safe? Distinct from evaluation — this
> is per-call, in the hot path.

## What it is

When the model returns a tool call or structured answer, the orchestrator parses
and validates it against the expected [[Schemas]] (and any safety rules) before
using it. If it fails, the orchestrator retries, repairs, or rejects — it does
**not** act on malformed output.

> **Output validation ≠ evals.** [[Output Validation]] is a *runtime* gate on
> *this one response* ("can I act on this now?"). [[Agent Evaluation]] is
> *offline/aggregate quality measurement* across many runs (domain [[08 Evaluation]]).
> Don't conflate them — see also the note in [[Orchestrator]].

## Why it's the orchestrator's job

LLM output is non-deterministic and can be malformed, hallucinated, or unsafe.
Acting on it blindly is how agents corrupt data or trigger bad side effects.
Validation is the guard between "the model said" and "the system did".

## How it works

```
resp = llm(ctx)
try:
    data = parse_and_validate(resp, schema)   # shape/type check ([[Schemas]])
    assert safe(data)                         # content/safety check
except Invalid as e:
    resp = llm(ctx + repair_hint(e))          # ask the model to fix → retry
```

Layers of validation:
- **Syntactic** — is it valid JSON / does it match the schema?
- **Semantic** — are values sane (dates real, refs exist)?
- **Safety** — no injected commands, no disallowed content ([[Prompt Injection]]).

## Likely issues
- **No validation** → malformed output crashes downstream or executes wrongly.
- **Validate-but-don't-repair** → unnecessary hard failures the model could fix.
- **Infinite repair loops** → cap repair retries ([[Termination Conditions]]).
- **Trusting schema-valid-but-wrong data** → shape is right, meaning is wrong.

## Tradeoffs
- **Strict reject vs auto-repair** — rejecting is safe but brittle; repairing is
  resilient but costs extra calls and can mask real prompt problems.

## Example

A data-extraction agent must return `{name, email, amount}`. If the model emits
prose or a bad email, validation fails and the orchestrator re-asks with a repair
hint — only schema-valid data reaches the database.

## Q&A insights

_(To be filled as we go deeper.)_

## Related
- Part of [[Orchestrator]]'s responsibilities · [[02 Agent Architecture and Orchestration]] · [[AI Agents MOC]]
- [[Schemas]] — what output is validated against
- [[Agent Evaluation]] — the offline counterpart (don't conflate)
- [[Error Handling]] — what happens when validation fails
- [[Prompt Injection]] — the safety dimension of validation
