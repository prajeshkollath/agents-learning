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

## What a tool schema looks like (and what it helps)

The raw form sent to the model — name, description, and typed args (JSON Schema):

```json
{
  "name": "issue_refund",
  "description": "Refund a customer's order. Use only when the customer explicitly requests a refund and the order exists.",
  "input_schema": {
    "type": "object",
    "properties": {
      "order_id": { "type": "integer", "description": "The order to refund" },
      "amount":   { "type": "number",  "description": "Refund amount in USD", "exclusiveMinimum": 0 },
      "reason":   { "type": "string",  "enum": ["defective", "late", "wrong_item", "other"] }
    },
    "required": ["order_id", "amount", "reason"]
  }
}
```

Three parts, and which does the work:

| Part | Purpose |
|---|---|
| **`name`** | the identifier the model emits to call it |
| **`description`** | natural-language "when to use this" — *the most important field*; it drives [[Tool Selection]] |
| **`input_schema`** (`parameters` in OpenAI) | JSON Schema of args — `type`, per-field `description`, `enum`, `required` |

> Naming: **Anthropic** uses `input_schema`, **OpenAI** uses `parameters` — same
> JSON Schema underneath.

**What the model emits** (it runs nothing — it returns a structured call):

```json
{ "type": "tool_use", "name": "issue_refund",
  "input": { "order_id": 1234, "amount": 50, "reason": "defective" } }
```

**What the schema helps with:**
1. **Tool selection** — `description` + clear names tell the model *when* the tool applies (→ [[Tool Selection]]).
2. **Correct arguments** — types/`enum`/`required` tell it *how* to call it.
3. **Validation** — the orchestrator checks the call against the schema before executing (→ [[Output Validation]]).
4. **Constrained decoding** — providers can *enforce* the schema during generation, so invalid JSON or out-of-`enum` values can't be emitted.
5. **A contract / docs** — one source of truth shared by the LLM and your code.

> **Key insight: a tool schema is prompt engineering disguised as a type
> definition.** Every `description` and field name is text the model reads. It
> serves two audiences at once — the **model** ("when/how do I call this?") and the
> **orchestrator** ("is this call valid and safe?"). Vague schema → the model
> guesses and mis-calls; tight schema (clear description, `enum`, `required`) →
> reliable tool use.

## Output schemas (structured output)

A tool schema constrains a *tool call*; an **output schema** constrains the
model's **final answer** to a fixed shape — so you get typed data, not prose.
Same JSON Schema underneath, different role:

| | **Tool input schema** | **Output schema** |
|---|---|---|
| Constrains | the *arguments* of a tool call | the model's *final answer* |
| Used | mid-loop, to **act** (call a function) | to get **usable data out** |
| Answers | "how do I call this tool?" | "what shape must my answer be?" |
| Example | `issue_refund(order_id, amount)` | `{vendor, total, due_date}` from an invoice |

So: tool schema = "here's a function you *can* call"; output schema = "your answer
*must* look like this."

```python
class Invoice(BaseModel):           # Pydantic → JSON Schema
    vendor: str
    total: float
    due_date: date | None
    line_items: list[LineItem]

invoice = llm(prompt, response_format=Invoice)   # returns a validated Invoice
```

**How it's enforced:**
- **OpenAI** — `response_format: { type: "json_schema", strict: true }` (Structured Outputs).
- **Anthropic** — typically a **forced single tool call** whose `input_schema` is your output shape (or JSON-instruction + validation).
- **Mechanism — constrained decoding:** the model is restricted token-by-token to
  only emit tokens valid under the schema, so the JSON is *always* well-formed and
  `enum` values can't be violated. More reliable than "please return JSON" in the prompt.

**Where you use it** — any step whose output feeds *code, not a human*:
extraction (doc → fields), classification (`{label, confidence}`), routing
(`{intent}` → [[Routing]]), LLM-as-judge (`{score, reasoning}` → [[08 Evaluation]]),
structured generation (forms, configs, API payloads).

> **Pitfall — strict schemas can hurt reasoning.** If you force the model to emit
> *only* the answer JSON, it can't "think out loud" first, which lowers accuracy on
> hard tasks. Fixes: (1) put a **`reasoning` field first** in the schema so it
> thinks before the answer; (2) a **two-step** call (reason, then structure);
> (3) the provider's **thinking mode** alongside structured output. Strict output
> is great for extraction/classification (little reasoning); for *judgment* tasks,
> give it a reasoning step first.

Note: a schema checks *shape*, not *correctness* — an extracted total can be
well-formed but wrong, so business validation still applies ([[Output Validation]]).

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

**Q: What does a tool schema look like, and what does it help with?**
A JSON-Schema description of a function — `name`, `description`, and `input_schema`
(typed args with `enum`/`required`). The model reads it to decide *when* to use the
tool (description) and *how* to call it (args), then emits a structured `tool_use`
call; the orchestrator validates that call against the schema before executing. It
helps with tool **selection**, correct **arguments**, **validation**, **constrained
decoding** (providers enforce the schema), and acts as the **contract** between LLM
and code. Key insight: a tool schema is *prompt engineering disguised as a type
definition* — every description/field name is text the model reads, so tight
schemas (clear descriptions, `enum`, `required`) produce reliable tool use.

**Q: What about output schemas — how are they different from tool schemas?**
A **tool input schema** constrains a tool *call's arguments* (used mid-loop to
act); an **output schema** constrains the model's *final answer* to a fixed shape
(used to get typed data out). Same JSON Schema, different role. Enforced via
provider "structured output" / forced-tool-call + constrained decoding (guaranteed
valid JSON). Used for extraction, classification, routing, LLM-as-judge. **Key
pitfall:** a strict output schema stops the model reasoning first and can lower
accuracy on hard tasks — add a `reasoning` field first, or reason then structure.

## Related
- Part of [[Orchestrator]]'s responsibilities · [[04 Tool Use and Function Calling]] · [[AI Agents MOC]]
- [[Tool Calling]] — schemas define the callable tools
- [[Output Validation]] — runtime checking against the schema
- [[Structured Output Prompting]] — prompting for schema-shaped output
- [[Guardrails]] — business rules beyond shape
