---
title: Security Boundary
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - safety
  - security
  - architecture
status: learning
aliases:
  - Security
  - Trust Boundary
---

# Security Boundary

> The hard line the **LLM is never allowed to cross**: secrets, credentials,
> auth, and raw execution. The model is treated as an *untrusted* component;
> the orchestrator holds the keys and mediates every privileged action.

## What it is

Agents handle real credentials, private data, and code execution. The security
boundary is the architectural rule that the model **proposes** but the
orchestrator **holds power** — secrets, permissions, and execution stay outside
the model's reach. Treat LLM output like untrusted user input.

## Why it's the orchestrator's job

The model can be manipulated ([[Prompt Injection]]) and will faithfully relay
anything in its context. If it can see a secret or run arbitrary code, an
attacker who controls its input controls your system. The orchestrator enforces
least privilege so a compromised prompt can't escalate.

## How it works

Core controls:
- **Secrets stay out of context** — the orchestrator injects API keys at
  execution time; the model sees a tool, never the credential.
- **Least-privilege tools** — narrow, specific tools (`get_order(id)`) not broad
  ones (`run_sql(query)`).
- **Sandboxing** — untrusted/generated code runs isolated ([[Sandboxed Execution]]).
- **Auth & scoping** — actions run with the *user's* permissions, not god-mode.
- **Input/output filtering** — strip [[PII Filtering|PII]], detect injection ([[Guardrails]]).

```
# WRONG: secret in the prompt
ctx += f"Use API key {SECRET}"          # model can leak it
# RIGHT: orchestrator holds it
result = api.call(args, key=SECRET)     # injected at execution only
```

## Likely issues
- **Secrets in the prompt/context** → exfiltrated via injection.
- **Over-powerful tools** (raw shell/SQL) → arbitrary actions.
- **Confused-deputy** — the agent does, on behalf of an attacker, what the user
  is allowed to do (over-broad scope).
- **Unsandboxed code execution** → full host compromise.

## Tradeoffs
- **Capability vs containment** — broader tools/permissions make a more powerful
  agent but a larger blast radius; default to least privilege.

## Example

A coding agent runs generated code in a sandboxed container with no network and
no host secrets; its git tool authenticates via a scoped token the model never
sees — so even a malicious prompt can't steal credentials or escape the sandbox.

## Q&A insights

_(To be filled as we go deeper.)_

## Related
- Part of [[Orchestrator]]'s responsibilities · [[07 Safety Guardrails and Reliability]] · [[AI Agents MOC]]
- [[Sandboxed Execution]] — isolating tool/code execution
- [[Guardrails]] — the policy layer (softer enforcement)
- [[Prompt Injection]] — the primary threat
- [[PII Filtering]] — keeping sensitive data out of the model
