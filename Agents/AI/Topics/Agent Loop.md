---
title: Agent Loop
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - architecture
  - orchestration
status: learning
aliases:
  - The Agent Loop
  - Perceive Reason Act Observe
  - ReAct loop
---

# Agent Loop

> The repeating cycle the orchestrator runs: **perceive → reason → act →
> observe → repeat**, until a stop condition fires. It is the spine that ties
> every other orchestrator responsibility together.

## What it is

The control loop at the heart of every agent. Each iteration: gather context,
ask the LLM what to do, do it, record the result, decide whether to continue.
A chatbot answers once; an agent **loops** — that loop is what lets it take
multiple steps toward a goal.

The four phases:
- **Perceive** — gather the current state/inputs/tool results into context.
- **Reason** — the LLM decides the next action (or that it's done).
- **Act** — the orchestrator executes the chosen tool.
- **Observe** — capture the result and append it to state.

## Why it's the orchestrator's job

The LLM is stateless and does one forward pass per call — it cannot "loop" by
itself. The orchestrator owns the loop: it decides *when* to call the model,
*how many times*, and *when to stop* (see [[Termination Conditions]]). Everything
else — [[State Management]], [[Context Building]], [[Tool Calling]],
[[Guardrails]] — happens at specific points inside this loop.

## How it works

```
state = init(goal)
while not done:                 # ── loop control (orchestrator)
    ctx   = build_context(state)        # Perceive → [[Context Building]]
    step  = llm(ctx)                    # Reason   → the model proposes
    if step.is_final: return step.answer
    if guards.block(step): ...          # enforce  → [[Guardrails]]
    result = execute(step.tool)         # Act      → [[Tool Calling]]
    state.append(result)                # Observe  → [[State Management]]
    check_termination(state)            # stop?    → [[Termination Conditions]]
```

Only `llm(ctx)` is the model; every other line is deterministic code. The loop
is where "LLM proposes, orchestrator disposes" actually plays out — see
[[Orchestrator vs LLM Responsibilities]].

## Variants

**Foundational families:**
- **ReAct loop** — interleaves reasoning and action each step; linear, reactive.
  The standard function-calling loop ([[ReAct Prompting]]).
- **Plan-and-execute** — plan all steps up front, then run them; re-plan on failure.
- **Fixed workflow** — the loop is a hardcoded graph; the LLM only fills nodes
  ([[Agents vs Workflows]]).

**Advanced patterns** (mostly elaborations of the three above):
- **Reflexion / self-critique** — adds a *reflect* phase: the agent critiques its
  own output and retries if it isn't good enough ([[Reflection]]). For tasks where
  first attempts often fail (code, math).
- **Tree of Thoughts (ToT)** — explores multiple reasoning branches, scores them,
  and backtracks — a *search over thought-space*, not a linear loop. For hard
  problems with many candidate paths.
- **Plan-execute as a DAG (LLM-Compiler)** — plan a graph of tool calls and run
  independent ones in parallel; re-plan on failure. Faster for multi-tool tasks.
- **Supervisor / multi-agent loop** — the "action" is delegating to a sub-agent;
  a supervisor routes work to workers ([[Multi-Agent Systems]]).

### How to choose

The real question: *how predictable is the task, and do you care more about cost
or quality?*

| Variant | Use when… | Cost | Reliability |
|---|---|---|---|
| **ReAct** | open-ended, steps unknown ahead; general tool-use | medium | medium |
| **Plan-and-Execute** | many steps, knowable up front; want an auditable plan + fewer calls | lower | medium |
| **Fixed workflow** | process is known/repeatable; want testable, production-grade reliability | lowest | highest |
| **Reflexion** | quality critical, first tries fail often (code, math) | higher | higher |
| **Tree of Thoughts** | hard search/reasoning, many candidate paths | highest | high (hard problems) |
| **Supervisor / multi-agent** | task splits into specialties (research + write + review) | higher | depends on coordination |

**Rule:** start with the simplest that works — most agents are **ReAct**, or a
**fixed workflow** when steps are known. Add Reflexion / ToT / multi-agent only
when a concrete need appears (quality, parallel speed, specialization) — the same
"sit as far left as the problem allows" idea from
[[Orchestrator vs LLM Responsibilities]].

**Implementation:** ReAct / Reflexion → a `while` loop or a framework agent
executor; fixed workflow / DAG / supervisor → a graph framework like
[[LangGraph]]; ToT → usually custom search (BFS/DFS) calling the LLM to expand
and score nodes.

## Likely issues
- **No termination → runaway loop** (infinite steps, runaway cost).
- **Context not rebuilt correctly → the agent "forgets"** the last result.
- **Acting before validating** the LLM's output → unsafe execution.

## Example

Claude Code in this session ran an agent loop: perceive the repo state → reason
about the next edit/command → act (run a tool) → observe output → repeat — and
it stopped when the task was done or a guard blocked an action.

## Q&A insights

**Q: Are the three listed variants the only ones? How do we use them?**
No — ReAct, plan-and-execute, and fixed workflow are the *foundational families*.
The advanced patterns (Reflexion, Tree of Thoughts, DAG / LLM-Compiler,
supervisor / multi-agent) are mostly elaborations of them — e.g. ReAct + a reflect
step = Reflexion; plan-execute + branching = ToT. **How to use them:** choose by
how predictable the task is and whether you optimise for cost or quality (see the
"How to choose" table). Default to the simplest — usually ReAct, or a fixed
workflow when the steps are known — and reach for advanced patterns only for a
concrete need (extra quality, parallel speed, or specialization).

## Related
- Part of [[Orchestrator]]'s responsibilities · [[02 Agent Architecture and Orchestration]] · [[AI Agents MOC]]
- [[Termination Conditions]] — how the loop is forced to stop
- [[Context Building]] — the "perceive" phase
- [[Tool Calling]] — the "act" phase
- [[State Management]] — the "observe" phase
- [[Orchestrator vs LLM Responsibilities]] — who owns each line
- [[Designing a Safe Agent Loop]] — making the loop debuggable
