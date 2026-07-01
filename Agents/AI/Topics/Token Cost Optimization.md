---
title: Token Cost Optimization
created: 2026-07-01
updated: 2026-07-01
tags:
  - ai-agents
  - cost
  - architecture
status: learning
aliases:
  - Cost Optimization
  - Token Optimization
  - Token Cost Anatomy
---

# Token Cost Optimization

> Making **each call cheaper** — shrinking what you send, what the model generates,
> and what you pay per token — as opposed to [[Cost Control]], which *caps and stops*
> spend. Control = "don't exceed the budget"; optimisation = "do the same work for
> fewer tokens/dollars".

## What it is

Before you can cut cost you have to know **what you're paying for**. "Token cost"
feels like one number but it's a **sum over many components**, split across two
meters — **input** (context you send *in*) and **output** (what the model generates
*out*) — priced at different rates (output is typically ~4–5× input). Optimisation
is attacking each component in turn.

> **Control vs optimisation.** *Cost control* = measure + cap + stop (the runtime
> guard, [[Cost Control]]). *Cost optimisation* = make each call cheaper (this note).
> They compose: optimise so each call is lean, cap so no run runs away.

## What's in the token bill — every component

### INPUT — everything in the context window when you hit "send"

The API is **stateless**: you resend the whole conversation every turn, so a turn's
input is the *entire payload on the wire*.

| Component | What it is | Note |
|-----------|-----------|------|
| **System prompt** | your instructions / persona | rendered first; freeze it → cacheable |
| **Tool definitions** | `name` + `description` + `input_schema` of **every** tool exposed | paid on **every** call, even for unused tools — big tool sets are a fixed tax |
| **Conversation history** | all prior `user` + `assistant` turns | the compounding driver; grows every turn |
| ↳ **tool_use blocks** | the model's past tool calls (name + args) | inside assistant messages |
| ↳ **tool_result blocks** | data you fed back | inside user messages — tool outputs can be *huge* |
| **New user message** | the only genuinely new text | usually the smallest piece |
| **RAG / retrieved context** | docs/chunks injected into the prompt | often the **largest** single component ([[RAG and Knowledge Grounding]]) |
| **Few-shot examples** | in-context examples | fixed cost per call |
| **Attached files / documents** | PDFs, text placed in a message | billed as input tokens by length |
| **Images (vision)** | tokenised by resolution | a high-res image = thousands of tokens |
| **Prior thinking blocks** | reasoning echoed back on multi-turn | when continuing on the same model |

#### Tool schemas: **every exposed tool is billed on every call**

Worth calling out because it surprises people: **every tool you expose to the agent
counts in input tokens on every request — used or not.** Tool definitions are part
of the payload, rendered first (`tools → system → messages`), and each contributes
its full schema:

- **`name`**
- **`description`** — usually the biggest part; often a few sentences
- **`input_schema`** — every parameter's name, type, `description`, `enum` values, `required` list

So 20 richly-described tools can be several thousand input tokens — paid on **every**
call, because the model needs the whole menu to choose. An *unused* tool costs the
same as a used one; using a tool only adds *output* tokens (generating the call).
And because history is resent every turn, that schema block is re-sent on all 12
turns of a 12-step run — a **fixed tax × conversation length**.

Two consequences: (1) the tool block sits at position 0, so it's **cacheable** — but
adding/removing/reordering a tool mid-conversation invalidates the whole cache
([[Caching Strategies]]); (2) at large tool counts, loading every schema is wasteful,
which is what **tool search** solves — load only the relevant schemas on demand
([[Tool Calling]]). Lean tool sets are a *cost* concern, not just a
least-privilege ([[Security Boundary]]) one — don't expose 30 tools "just in case".

### OUTPUT — everything the model generates

| Component | What it is | Note |
|-----------|-----------|------|
| **Visible response text** | the answer the user sees | |
| **Thinking / reasoning tokens** | extended/adaptive thinking | **billed as output even when hidden** — `display:"omitted"` hides the text, not the charge |
| **tool_use generation** | the model *producing* a tool call | output now; becomes input history next turn |

### Cross-cutting: caching sub-divides input, server tools add fees

- **Caching** splits every input component into `input_tokens` (uncached, 1×),
  `cache_read_input_tokens` (~0.1×), `cache_creation_input_tokens` (1.25×/2×) — it
  changes the *price* of a component, not whether it counts ([[Cost Control]]).
- **Server-side tools** (web search, code execution) carry their own per-use fee
  **and** inject their results back as **more input tokens** on the continuation.

```
turn cost =  Σ input components   (÷ uncached / cache-read / cache-write, per-model rate)
          +  Σ output components  (visible text + thinking + tool-call generation)
          +  any server-tool fees
```

## The optimisation levers (component → fix)

Each thing you pay for is a lever to pull:

| Cost component | Lever |
|----------------|-------|
| Repeated system prompt / tools / history | **Prompt caching** — ~0.1× on the cached prefix ([[Caching Strategies]]) |
| Growing history | **Context trimming / compaction** — summarise or drop old turns ([[Context Building]]) |
| Big tool schemas paid every call | **Fewer/leaner tools**, or tool-search to load schemas on demand |
| Bloated RAG context | **Retrieve less, rank better** — top-k tuning, smaller chunks |
| Every step on the strong model | **Model routing** — cheap model for easy steps, strong only when needed ([[Model Selection Tradeoffs]]) |
| Too many loop steps | **Fewer steps** — better planning, step caps ([[Termination Conditions]]) |
| Verbose / over-thinking output | **Effort / max_tokens tuning**, terser prompts |
| High-res images | **Downsample** to the smallest resolution that still works |

## Likely issues
- **Optimising output, ignoring input** — input (context, RAG, history, tool
  schemas) is usually the bigger bill; output is a fraction.
- **Forgetting thinking is billed** — hidden reasoning still costs output tokens.
- **Paying for unused tools** — every exposed tool's schema is on every call.
- **Cache silently missing** — a timestamp/UUID in the prefix invalidates it; verify
  `cache_read_input_tokens > 0` ([[Caching Strategies]]).

## Tradeoffs
- **Cost vs quality** — a cheaper model, trimmed context, or fewer few-shot examples
  save tokens but can lower accuracy; optimise to the task's value, not to zero.
- **Cache write premium** — writing the cache costs *more* (1.25×/2×) than a normal
  token; caching only pays off when the prefix is read again enough times.

## Example

A support agent's cost audit: the 40k-token knowledge-base dump per call dwarfs the
200-token question. Fix isn't shorter answers — it's caching the system prompt +
tool schemas (paid once, ~0.1× thereafter), retrieving top-3 chunks instead of
top-10, and routing FAQ turns to a cheaper model — cutting cost ~5× with no quality
loss.

## Q&A insights

- **"What all is included in the token cost?"** — Two meters. **Input** = system
  prompt + *all* tool definitions + full history (every user/assistant turn,
  including `tool_use` and `tool_result` blocks) + new message + RAG context +
  few-shot examples + attached files + images + echoed thinking blocks. **Output** =
  visible text + thinking/reasoning tokens (billed even when hidden) + the model
  generating tool calls. Plus server-tool fees, and caching sub-divides input into
  uncached / cache-read / cache-write buckets. Three surprises: you pay for tool
  schemas on **every** call, thinking is output you pay for even when it's hidden,
  and tool-results/RAG are usually the biggest line items — and it all **compounds
  per turn** because history is resent.

## Related
- [[Cost Control]] — capping/stopping spend (this note is the *make-it-cheaper* half)
- [[Caching Strategies]] — the biggest input-side lever
- [[Context Building]] — trimming/compaction to shrink history
- [[Model Selection Tradeoffs]] — routing cheap vs strong per step
- [[RAG and Knowledge Grounding]] — retrieved context is often the largest component
- [[Tool Calling]] — tool schemas are paid on every call
- Part of [[Orchestrator]]'s concerns · [[12 Production and Cost Engineering]] · [[AI Agents MOC]]
