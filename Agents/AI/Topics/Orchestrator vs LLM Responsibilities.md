---
title: Orchestrator vs LLM Responsibilities
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - architecture
  - orchestration
status: learning
aliases:
  - Orchestrator vs LLM
  - What logic belongs in the orchestrator vs the LLM
  - LLM proposes orchestrator disposes
---

# Orchestrator vs LLM Responsibilities

> **LLM proposes, orchestrator disposes.** The LLM *suggests* what to do; the
> orchestrator (deterministic code) decides whether and how to actually do it.
> Everything that must be reliable, secure, auditable, or repeatable lives in
> code; only genuine reasoning and language tasks go to the model.

## Terminology

Each term links to its own note — these are the drill-in points for going deeper.

- **[[Orchestrator]]** — the deterministic software running the agent (a.k.a. *harness*, *runtime*, *controller*, *scaffolding*).
  - *Example:* Claude Code's runtime in this session — it built my prompts, executed my tools, persisted state, and **blocked the `git push` to main**.
- **[[LLM as Reasoning Engine|LLM]]** — the model; a *reasoning engine*, the *policy* in RL terms. It is [[Non-Determinism|non-deterministic]], [[Statelessness|stateless]], and probabilistic.
  - *Example:* Claude reading "I want my money back" and proposing `refund(order=123)` — but not actually executing it.
- **[[Control Flow]]** — the logic deciding *what happens next*: loop, branch, or stop.
  - *Example:* the `for step in range(MAX_STEPS)` loop and the `if policy.allows(call)` branch in the canonical loop below — all code, no LLM.
- **[[Planning|Reasoning / planning]]** — interpreting ambiguity and decomposing a goal into steps.
  - *Example:* LLM output "To book a trip: 1) search flights, 2) check budget, 3) reserve" — a plan it proposes, the orchestrator carries out.
- **[[Control Plane vs Data Plane]]** — orchestrator = control plane (decisions/enforcement); tools + model = data plane (the actual work). Borrowed from networking.
  - *Example:* control plane = "*should* we call the payment API and are we allowed?"; data plane = the payment API call itself moving the money.
- **[[Cognitive Architecture]]** — the overall design of how reasoning, memory, tools, and control fit together.
  - *Example:* ReAct, plan-and-execute, and supervisor/subagent are three different cognitive architectures for the same task.

## What it is

A division-of-responsibility principle for agent design. The LLM and the
orchestrator have **opposite properties**, so each owns what it is good at:

| LLM | Orchestrator (code) |
|---|---|
| Non-deterministic | Deterministic |
| Stateless (forgets between calls) | Holds state |
| Can hallucinate | Exact |
| Slow (seconds/call) | Fast (ms) |
| Expensive per call | ~Free |
| Hard to test | Unit-testable |
| Great at fuzzy / language | Bad at fuzzy / language |

**Rule of thumb:** never spend an LLM call on something deterministic code can
do, and never trust the LLM with something that must be *guaranteed*.

### What goes where

**Orchestrator owns:**
- **The loop** — when to call the LLM, how often, **when to stop** ([[Termination Conditions]])
- **State & memory** — history, scratchpad, persistence (the LLM is stateless, so *all* memory is the orchestrator's job → [[Agent Memory]])
- **Tool execution** — invoking the API/function with timeouts, retries, idempotency, error handling
- **Enforcement / guardrails** — permissions, policy, validating the proposed action *before* doing it ([[Guardrails]])
- **Security boundary** — secrets, auth, sandboxing (LLM never touches raw credentials → [[Sandboxed Execution]])
- **Infrastructure** — logging, tracing, rate limits, caching, concurrency, cost accounting ([[Observability]])
- **Output parsing/validation** — schema-checking the model's response

**LLM owns:**
- Natural-language understanding
- Reasoning over ambiguous input
- **Planning** — proposing how to decompose a goal ([[Planning]])
- **Tool *selection*** — choosing *which* tool and *what args* ([[Tool Selection]])
- Summarization, extraction, generation

> Subtle but critical: **tool *selection* is the LLM's job; tool *execution* is
> the orchestrator's.** The model says `refund(order=123, amount=50)`; the
> orchestrator validates and runs it.

## Why it matters

This is *the* architect-level question. Getting the split wrong produces agents
that are unpredictable, insecure, expensive, and undebuggable. Getting it right
gives you a system where the unreliable part (the model) is sandboxed inside a
reliable part (the code) that can validate, retry, log, and stop it.

## How it works

The LLM never directly touches tools, the DB, or secrets. It emits *structured
intent*; the orchestrator validates → executes → feeds the result back.

```
          ┌─────────────────────────────────────────┐
  User ──▶ │           ORCHESTRATOR (code)           │
          │  loop · state · policy · tool dispatch   │
          └───┬───────────────┬──────────────┬───────┘
              │ prompt         │ validated    │ read/write
              ▼                │ tool call    ▼
        ┌──────────┐           ▼          ┌─────────┐
        │   LLM    │     ┌───────────┐    │  State  │
        │ (reason) │     │   Tools/  │    │  store  │
        └──────────┘     │  sandbox  │    └─────────┘
                         └───────────┘
```

### The canonical loop

```python
state = init(user_goal)
for step in range(MAX_STEPS):              # orchestrator: termination guard
    prompt   = build_prompt(state)         # orchestrator: state -> context
    response = llm(prompt)                  # LLM: reason / propose

    if response.is_final:                   # LLM proposed "done"
        return response.answer

    call = response.tool_call               # LLM: which tool + args
    if not policy.allows(call):             # orchestrator: ENFORCE
        state.append(deny(call)); continue
    if not schema.valid(call):              # orchestrator: VALIDATE
        state.append(error(call)); continue

    result = execute(call, timeout=..., idempotency_key=...)  # orchestrator: DO
    state.append(result)                    # orchestrator: persist
# fell out of loop -> hit step budget (a termination condition)
```

Note every line except `llm(prompt)` is deterministic code. The LLM contributes
exactly two things: *propose a tool call* or *propose a final answer*.

## Flavours — the workflow ↔ agent spectrum

The contentious part is **who owns control flow**:

```
WORKFLOW ◀───────────────────────────────────▶ AGENT
(code-driven control)              (LLM-driven control)

prompt chaining,        function-calling loop,   fully autonomous
routing, fixed graph    ReAct, plan-and-execute   open-ended agent
predictable, cheap,     flexible, handles         maximally adaptable,
testable, brittle       novel cases, less         least predictable,
to novelty              predictable               hardest to debug
```

Anthropic's *Building Effective Agents* draws this **workflow vs agent** line.
**Architect default: sit as far left as the problem allows** — use LLM-driven
control only where genuine adaptability is required. See [[Orchestration vs Choreography]].

## Examples

- **Support agent:** LLM decides "issue a refund." Orchestrator enforces
  ">$100 needs human approval," verifies the order, calls payment with an
  idempotency key, logs it.
- **Coding agent (Claude Code, observed live):** the LLM proposed
  `git push origin main`; the orchestrator's permission layer **blocked it**
  ("pushing to main bypasses review"). The model proposed, the orchestrator
  disposed — this concept in action.
- **LangGraph:** the graph (code) hardcodes the workflow; the LLM only fills in
  reasoning at each node. See [[LangGraph]].

## Constraints

- LLM **statelessness** → orchestrator carries all state.
- **Context window limits** → orchestrator decides what to include ([[Context Window Management]]).
- **Non-determinism** → never use the LLM for exact-match control gates.
- **Latency** → each call is seconds; minimize calls.
- LLM **cannot be trusted** for security- or correctness-critical decisions.

## Demo → production scaling

| Demo | Production |
|---|---|
| LLM decides everything | Known control flow moved into code |
| State in memory | Durable external state, crash & resume ([[Stateless Orchestrator Design]]) |
| Runs until LLM says done | Hard termination + max steps + budget cap ([[Termination Conditions]]) |
| Happy path | Retries, idempotency, fallbacks |
| `print()` debugging | Tracing on every step ([[Observability]]) |
| No limits | Guardrails + policy engine ([[Guardrails]]) |
| Ignore cost | Token accounting + caching ([[Token Cost Optimization]]) |

**Maturation arc:** as you learn which decisions the LLM makes reliably, migrate
them from LLM-driven to code-driven to cut cost, latency, and unpredictability.

## Likely issues

- **Over-delegating control to the LLM** → unpredictability, infinite loops, runaway cost, undebuggable behavior.
- **Trusting LLM output without validation** → security holes; injection that makes the agent *act* ([[Prompt Injection]]).
- **No termination** → runaway loops.
- **Lost state** → LLM "forgets" because the orchestrator didn't persist it.
- **Non-idempotent tools** → an LLM retry double-charges a customer.
- **Prompt + control logic tangled** → impossible to unit-test.

## Tradeoffs

- **Autonomy/flexibility ⟷ reliability/predictability** — the central tension.
  LLM-driven control adapts to novelty but is costly and unpredictable;
  code-driven control is cheap, testable, reliable but brittle to unforeseen input.
- **More LLM calls** = smarter but slower and pricier.
- **Thin orchestrator** = fast to build, less safe; **thick orchestrator** =
  safe and observable, more engineering effort.

## Cost

- Every LLM call = tokens = money + latency. A decision made by **code is
  ~free**; the same decision made by the **LLM costs a round-trip**.
- Cost **compounds in loops** — a 10-step agent is ~10× the calls.
- **Architect's rule:** push deterministic decisions into code; reserve LLM
  calls for irreducible reasoning. See [[Caching Strategies]], [[Token Cost Optimization]].

## Soundbite

> *"LLM proposes, orchestrator disposes. Keep everything that must be reliable,
> secure, auditable, or repeatable in deterministic code; reserve the model for
> genuine reasoning, planning, and language. The architecture skill is choosing,
> per decision, where it sits on the workflow-to-agent spectrum — defaulting to
> code wherever the problem allows."*

## Q&A insights

_(To be filled as we go deeper — questions Prajesh asks that add nuance get captured here.)_

## Related
- Part of [[02 Agent Architecture and Orchestration]] · [[AI Agents MOC]]
- [[Designing a Safe Agent Loop]] — applies this split to build a debuggable loop
- [[Termination Conditions]] — an orchestrator responsibility
- [[Stateless Orchestrator Design]] — where state lives for crash/resume
- [[Orchestration vs Choreography]] — control-flow patterns across agents
- [[Agent Loop]] — the loop this principle structures
- [[Tool Calling]] / [[Tool Selection]] — selection (LLM) vs execution (orchestrator)
- [[Guardrails]] — the enforcement layer
- [[Agents vs Workflows]] — the spectrum this sits on
