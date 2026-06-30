---
title: Guardrails
created: 2026-06-22
updated: 2026-06-30
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

## Tool-check policy (worked example)

A **tool-check guardrail** sits between the LLM deciding to call a tool and the
tool actually running. The LLM proposes `tool + arguments`; the guardrail
evaluates that proposal against a **policy** and returns a decision:

```
allow · deny · require_approval · modify
```

The most important decision is **`require_approval`** (not just allow/deny):
it's how a human stays in the loop for the risky 5% while the safe 95% runs
autonomously. See [[Human in the Loop]].

### What a policy actually checks

A policy is a set of rules keyed on **`(tool, args, context)`**. Think of it as
a firewall rule table for tool calls.

| Axis | Example rule |
|------|-------------|
| **Tool allow-list** | Agent may only call `search`, `read_file` — never `shell` |
| **Argument validation** | `amount <= 1000`; path not in a secrets dir |
| **Destructive-action gate** | Any write / delete / send → `require_approval` |
| **Rate / budget** | Max 5 emails per run; max $10 API spend |
| **Scope / intent match** | Tool call must relate to the user's stated request |
| **Data egress** | Block recipients / args leaving the org |

Two design stances:
- **Allow-list** (`default: deny`) — nothing runs unless explicitly permitted.
  Safer, more setup. Aligns with **fail-safe defaults** above.
- **Deny-list** (`default: allow`) — everything runs except blocked patterns.
  Easier, leakier.

On **deny** you don't crash — the reason is fed back to the model as a tool
result (`"denied: mutating SQL blocked"`), and it re-plans with a safer call.

A tool-check policy decides *whether a call is allowed*; it does **not** contain
the blast radius if the call runs anyway. That's the [[Security Boundary]]'s job
— sandbox, scoped credentials, network limits — the harder enforcement layer
*beneath* the policy. Policy = "should this run?"; boundary = "what can it touch
if it does?".

### A policy is *rules*, not a file type

YAML is the common *teaching* form because it's readable, but the policy is the
**decision rules themselves** — the format is incidental. Real agents express the
same policy many ways, trading off *readability* vs *expressiveness* vs *auditability*:

```
POLICY = the rules + the decision they produce   (the abstract thing)
   └── expressed as → YAML | code | Rego | decorators | an LLM prompt
```

| Form | When used |
|------|-----------|
| **YAML / JSON config** | Simple rules; non-engineers edit them; read by a policy engine |
| **Plain code** (`if/else` fn) | Needs real logic — regex, lookups, stateful counts. Most frameworks |
| **Policy language** (OPA/Rego, Cedar) | Enterprise; rules in a dedicated language, evaluated by an engine; auditable |
| **Decorator on the tool** | `@tool(requires_approval=True, max_calls_per_run=5)` |
| **An LLM judge** | Fuzzy checks code can't express ("is this email rude?") — see [[LLM as Judge]] |

Same policy, two representations:

```yaml
# YAML form
- tool: execute_sql
  when:  { args.query: "~*(DELETE|DROP|TRUNCATE)" }
  action: deny
  reason: "Mutating SQL not allowed from agent"
```

```python
# Code form (the guardrail function that runs before the tool)
def tool_guardrail(tool, args, context):
    if tool not in context.allowed_tools:
        return DENY, "Tool not granted to this agent"
    if tool == "execute_sql" and re.search(r"\b(DELETE|DROP|TRUNCATE)\b", args["query"], re.I):
        return DENY, "Mutating SQL blocked"
    if tool == "send_email" and not args["to"].endswith("@mycompany.com"):
        return REQUIRE_APPROVAL, "External recipient"
    if context.calls_today[tool] > context.limits[tool]:
        return DENY, "Rate limit exceeded"
    return ALLOW, "OK"
```

## Q&A insights

- **"Is a policy a YAML file, then?"** — No. A policy is the *decision rules*, not
  a file format. YAML is just the most readable teaching form; in real agents the
  policy is very often a plain function (or a decorator on the tool), and in
  enterprise setups a dedicated language like Rego/Cedar for auditability. Pick
  the representation by trade-off: readability (YAML) vs expressiveness (code) vs
  auditability (Rego). A policy can even *be* another LLM ([[LLM as Judge]]) for
  fuzzy checks code can't express.
- **The key decision isn't allow/deny — it's `require_approval`.** That's the
  lever that keeps a human on the risky minority of calls while the safe majority
  runs autonomously.

## Related
- Part of [[Orchestrator]]'s responsibilities · headline of [[07 Safety Guardrails and Reliability]] · [[AI Agents MOC]]
- [[Security Boundary]] — secrets/auth/sandbox (the harder boundary)
- [[Output Validation]] — shape/safety checks on responses
- [[Prompt Injection]] — a threat guardrails defend against
- [[Fallback Strategies]] — human-handoff as a guardrail path
