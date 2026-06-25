---
title: Guardrails
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - safety
  - architecture
status: learning
aliases:
  - Policy Engine
  - Agent Guardrails
---

# Guardrails

> The **enforcement layer** between the LLM's proposal and execution: policy,
> permissions, and safety checks that decide what the agent is *allowed* to do.
> Headline of domain [[07 Safety Guardrails and Reliability]]; here, the
> orchestrator's enforcement responsibility.

## What it is

Guardrails are deterministic rules the orchestrator applies around the model:
- **Input guardrails** — filter/blocklist prompts, strip [[PII Filtering|PII]], detect injection.
- **Action guardrails** — permission checks before a tool runs (allowed? needs approval? within limits?).
- **Output guardrails** — block disallowed or unsafe responses before they reach the user.

## Why it's the orchestrator's job

The model is non-deterministic and can be manipulated ([[Prompt Injection]]); it
cannot be trusted to police itself. Guardrails live in code, as a **separate
layer from the LLM**, so enforcement is reliable, auditable, and independent of
what the model "decides".

## How it works

```
call = llm_response.tool_call
if not policy.allows(call):              # rule check
    if policy.needs_approval(call):
        return await human_approval(call)  # human-in-the-loop
    return deny(call)                      # blocked, fed back to model
result = execute(call)
```

A core principle is **fail-safe defaults**: every limit/timeout/ambiguous case
defaults to the *safe* option (deny, escalate), never the permissive one. Rules
can be hand-coded or run in a policy engine (e.g. OPA).

## Likely issues
- **Guardrails as prompt instructions only** → the model can be talked out of them;
  enforce in code, not just the system prompt.
- **Fail-open defaults** → on error it allows instead of denying.
- **Over-blocking** → legitimate actions denied, agent becomes useless.
- **No audit trail** → can't prove what was blocked and why ([[Observability]]).

## Tradeoffs
- **Safety vs capability** — stricter guardrails are safer but more limiting;
  tune to the domain (a finance agent ≫ a note-taking agent).

## Example

The live example from this vault's own creation: the coding agent proposed
`git push origin main`; a guardrail blocked it ("pushing to main bypasses
review") — enforcement in the orchestrator, independent of the model's intent.

## Q&A insights

_(To be filled as we go deeper.)_

## Related
- Part of [[Orchestrator]]'s responsibilities · headline of [[07 Safety Guardrails and Reliability]] · [[AI Agents MOC]]
- [[Security Boundary]] — secrets/auth/sandbox (the harder boundary)
- [[Output Validation]] — shape/safety checks on responses
- [[Prompt Injection]] — a threat guardrails defend against
- [[Fallback Strategies]] — human-handoff as a guardrail path
