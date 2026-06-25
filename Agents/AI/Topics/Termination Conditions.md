---
title: Termination Conditions
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - architecture
  - orchestration
  - reliability
status: learning
aliases:
  - Termination
  - Stopping Conditions
  - Loop Termination
---

# Termination Conditions

> The rules that **force the [[Agent Loop]] to stop**. Without them an agent can
> loop forever, burning tokens and money. A non-negotiable orchestrator
> responsibility.

## What it is

The set of checks, evaluated each iteration, that decide whether the loop ends.
An agent should stop for one of two reasons: it **succeeded** (the good case) or
it **hit a limit** (the safety net). You need both — never rely on the model
alone to decide it's finished.

## Why it's the orchestrator's job

The LLM is non-deterministic and may never emit "done" — it can loop, repeat
itself, or chase a goal it can't reach. The orchestrator must impose hard,
deterministic limits the model cannot override.

## Types of termination

**Success (intended):**
- The LLM signals completion (a final answer / a `finish` tool).
- A goal-check passes (the target state is reached).

**Limits (safety net):**
- **Max steps / iterations** — e.g. stop after 15 loops.
- **Token / cost budget** — stop after N tokens or $X ([[Cost Control]]).
- **Wall-clock timeout** — stop after T seconds.
- **No-progress / loop detection** — stop if the last K steps repeat or don't advance.
- **Repeated failure** — stop after N consecutive tool errors.
- **Human stop** — an operator or user aborts.

## How it works

```
for step in range(MAX_STEPS):           # max-steps guard
    ...
    if response.is_final: return ...     # success
    if tokens_used > BUDGET: raise Stop  # cost guard ([[Cost Control]])
    if looks_stuck(history): raise Stop  # no-progress guard
# fell out of loop → hit the step ceiling
```

The success check and the limit checks live at different points: success right
after the LLM responds, limits before/after each action.

## Likely issues
- **Only a success condition, no limits** → runaway loop on any edge case.
- **Limits too tight** → the agent gives up on legitimately long tasks.
- **No loop/no-progress detection** → the agent spins on the same failing action.
- **Silent termination** → it stops but doesn't say *why* (log the reason).

## Tradeoffs
- Generous limits = more capable but riskier/costlier; tight limits = safe but
  may truncate real work. Tune per task and **always log which condition fired**.

## Example

The refund agent: stop on success (refund issued), or stop at 15 steps / $2 of
tokens / 60 s — whichever comes first, with the triggering condition logged for
[[Observability]].

## Q&A insights

_(To be filled as we go deeper.)_

## Related
- Part of [[Orchestrator]]'s responsibilities · [[02 Agent Architecture and Orchestration]] · [[AI Agents MOC]]
- [[Agent Loop]] — what these conditions stop
- [[Cost Control]] — the budget-based limits
- [[Observability]] — log why it stopped
- [[Designing a Safe Agent Loop]] — termination as a safety mechanism
