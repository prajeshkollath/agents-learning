---
title: Durable Execution
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - architecture
  - orchestration
  - infrastructure
status: learning
aliases:
  - Durable Engine
  - Workflow Engine
  - Crash and Resume
---

# Durable Execution

> A system that **records every step of a workflow automatically** so that if the
> process crashes or redeploys, it **replays the history to resume exactly where
> it left off** — including resuming multi-hour waits. You write code that *looks*
> like it never fails; the engine makes it true. Level 6 on the
> [[Orchestrator Maturity Ladder]].

## What it is

In ordinary [[State Management]] *you* write the load/save/resume logic and must
reason about "what if we crash between step 2 and step 3?" A **durable execution
engine** (Temporal, Restate, AWS Step Functions, Inngest) takes that over: it
persists each step's result as an **event history** and drives the workflow from
that history. The state *is* the recorded history — you never write a `save()`.

## Why / when you need it

For a 10-second support reply, you don't — plain Postgres state is enough. You
need durable execution when a run is:
- **Long** — minutes to hours of multi-tool work you can't afford to restart.
- **Waiting on a human** — parks for hours/days for an approval without holding a process.
- **Must-not-lose-progress** — a deploy or crash mid-run must resume, not restart.
- **Exactly-once** — a side effect (disburse a loan, charge a card) must happen once.

## How it works — replay

The engine logs each completed step. On restart it **replays the history**:
already-completed steps return their *recorded* results instantly (they don't
re-run), and execution continues from the first unfinished step. That's why
activities should be deterministic given their inputs, and side-effecting work is
wrapped so it isn't repeated (pairs with [[Retries and Idempotency]]).

```python
@workflow.defn
class LoanAgent:
    @workflow.run
    async def run(self, application):
        credit   = await workflow.execute_activity(check_credit, application)  # recorded
        analysis = await workflow.execute_activity(llm_assess, credit)         # recorded

        # PARK up to 3 days waiting for a human — no process held open
        approved = await workflow.wait_condition(
            lambda: self.decision is not None, timeout=timedelta(days=3))

        if approved:
            await workflow.execute_activity(disburse_funds, application,
                                            idempotency_key=application.id)  # exactly once
```

If servers redeploy while it waits on the manager, the engine resumes the *exact*
workflow afterward — `check_credit` doesn't re-run, the wait continues.

## You-manage-state vs durable engine

| You manage (Redis/Postgres) | Durable engine |
|---|---|
| You write load/save each step | Automatic — every step checkpointed |
| You handle resume-after-crash yourself | Engine replays history and resumes |
| Waiting hours = hard (hold a process) | `await sleep(days)` — engine parks it |
| Simple infra | Needs a cluster/service + a mental-model shift |

## The landscape — is Temporal a "provider"?

**No — Temporal is a *product* (a durable-workflow engine), not a cloud provider
like AWS.** AWS is the whole marketplace; Temporal is one specific tool that
*runs on* a provider. Forms and competitors:

| Engine | Who runs it | Lock-in |
|---|---|---|
| **Temporal** (self-host the open-source server, or **Temporal Cloud** managed) | you, or Temporal Technologies | none — runs anywhere, incl. on AWS |
| **AWS Step Functions** | AWS (managed) | AWS only |
| **Azure Durable Functions** | Microsoft | Azure only |
| **Restate / Inngest** | newer startups | varies |

So AWS's *own* equivalent of Temporal is **Step Functions**. Trade-off mirrors
everything else: **Temporal = vendor-neutral, runs anywhere, more setup;
Step Functions = managed and easy, but ties you to AWS.**

## How you run it (Temporal)

Stand up a **Temporal cluster** (self-host) or use **Temporal Cloud**; write your
**Workflow** (orchestration) + **Activities** (the tool/LLM calls); run a
**Worker** process that executes them. The engine stores the event history and
drives execution.

## Likely issues
- **Non-deterministic workflow code** → replay diverges from history and breaks.
- **Side effects not made idempotent/wrapped** → repeated on replay ([[Retries and Idempotency]]).
- **Reaching for it too early** → heavy infra and a learning curve for a short agent.

## Tradeoffs / cost
- **Bulletproof vs heavy** — durable execution is the most reliable option but adds
  a real service to run (or a SaaS bill) and a new programming model.
- **Build cost** — rewriting an agent as workflow + activities is non-trivial.
- **Run cost** — a cluster (self-host) or per-action fees (Temporal Cloud /
  Step Functions), on top of the LLM cost.

## Q&A insights

**Q: Is Temporal a provider like AWS?**
No. AWS is a cloud provider (a whole marketplace); Temporal is one specific
product — a durable-workflow engine — that *runs on* providers like AWS. It comes
self-hosted (open-source) or as managed "Temporal Cloud". AWS's own competing
product is **Step Functions** (AWS-locked), vs Temporal which is vendor-neutral.

## Related
- Level 6 of [[Orchestrator Maturity Ladder]] · part of [[Orchestrator]] · [[AI Agents MOC]]
- [[State Management]] — the manual version this automates
- [[Stateless Orchestrator Design]] — externalised state, the simpler cousin
- [[Retries and Idempotency]] — why side effects must be safe under replay
- [[Termination Conditions]] — still needed to bound long runs
