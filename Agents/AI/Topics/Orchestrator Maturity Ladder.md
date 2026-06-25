---
title: Orchestrator Maturity Ladder
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - architecture
  - orchestration
  - infrastructure
status: learning
aliases:
  - Maturity Ladder
  - Orchestrator Build Levels
---

# Orchestrator Maturity Ladder

> **You don't build all of this at once.** You start at Level 0 and climb only
> as far as the *stakes* demand. Each rung is triggered by a real pain you hit —
> not by a desire to be thorough. The companion to [[Orchestrator]].

## Level 0 — The bare loop

**Adds:** a `while` loop that calls the LLM, parses a tool call, runs it, appends
the result, and repeats.
**Real-life:** a weekend "chat with my PDFs" prototype, or an agent in a Jupyter
notebook. This is the conceptual core of *every* agent, Claude Code included.
**Infra:** just Python + the model SDK (`anthropic` / `openai`). Runs on your
laptop; state is a Python list. No DB, no server.
**You're here when:** you're proving the idea works at all.

## Level 1 — Tool registry & schema validation

**Adds:** a formal registry (tool name → function + JSON schema). Validate the
LLM's proposed arguments *before* executing; reject hallucinated tools or
malformed args.
**Real-life:** your demo grows from 2 tools to 10 and the model starts inventing
arguments or calling tools that don't exist — e.g. an internal ops assistant with
`restart_service`, `query_db`, `page_oncall`.
**Infra:** Pydantic for schemas, a dict registry, the provider's
tool-use/function-calling API. Still one process.
**Trigger:** the model produces a call your code can't safely execute.

## Level 2 — External state store

**Adds:** move agent/conversation state out of process memory into a database.
Now it survives restarts and multiple users get isolated sessions.
**Real-life:** the agent goes from "just me testing" to "a Slack bot 50
colleagues use" — each thread needs its own persisted state; a support
conversation spans hours.
**Infra:** Redis (fast session cache) or Postgres (durable, queryable) with a
`sessions` table keyed by `conversation_id`; SQLAlchemy.
**Trigger:** a restart wipes conversations, or two users' contexts bleed together.

## Level 3 — Guardrails, termination & budget caps

**Adds:** an enforcement layer. Check policy before executing (allowed? needs
approval?). Cap max steps and token budget so it can't loop forever or blow the
bill.
**Real-life:** the refund agent — refunds > $100 need human approval, max 15
steps, halt if it has burned $2 of tokens. Or blocking a coding agent from
`rm -rf` / a force-push — exactly the `git push` block seen in the session that
created this vault.
**Infra:** a policy module (rules in code, or OPA), a step counter, token
accounting from the API's usage field, and a human-in-the-loop approval queue
(a DB table + a Slack approval button).
**Trigger:** the agent can do something expensive, irreversible, or dangerous.

## Level 4 — Retries, idempotency, fallbacks

**Adds:** production hardening. Tools fail (timeout, 500, rate-limit) → retry
with backoff. Make tool calls **idempotent** so a retry doesn't double-act. Fall
back when the model or a tool is down.
**Real-life:** a payment agent hit by a network blip mid-refund must *never*
refund twice; the model API returns `529 overloaded` → retry with backoff or
fall back to a cheaper/secondary model.
**Infra:** tenacity for retries, idempotency keys stored in the DB, circuit
breakers, dead-letter queues, multi-model routing via a gateway.
**Trigger:** real money/side-effects + flaky networks = no tolerance for
duplicates or crashes.

## Level 5 — Tracing & observability

**Adds:** every step emits traces/logs/metrics, so you can replay the exact
trajectory across 12 steps and 4 tool calls and see where it went wrong.
**Real-life:** a user reports "the agent gave a wrong answer." You open the
trace, see that at step 7 it selected the wrong tool with bad args. Without
tracing, you're blind.
**Infra:** LangSmith / Langfuse / Arize Phoenix, or OpenTelemetry → Grafana /
Datadog; structured logs; a trace ID spanning the whole run.
**Trigger:** real users + non-deterministic failures you can't reproduce by hand.

## Level 6 — Streaming, concurrency, durable execution

**Adds:** scale and UX. Stream output token-by-token; handle many concurrent
runs; **durable execution** so a 30-minute run survives a deploy or crash and
resumes mid-flight.
**Real-life:** a SaaS with thousands of simultaneous users; deploys happen while
agents are running and must not kill them; users expect ChatGPT-style streaming.
**Infra:** SSE/WebSockets (streaming), asyncio + worker pools (concurrency),
Temporal / Restate (durable execution), Kubernetes autoscaling, a queue
(SQS/Celery).
**Trigger:** scale, long runs, and zero-downtime deploys.

## How far should you climb?

| System | Stop around |
|---|---|
| Hackathon / prototype | L0–L1 |
| Internal tool (trusted users) | L2–L3 |
| Customer-facing production | L4–L5 |
| Regulated (finance/health) / high-scale | L6 (all of it) |

**The mistake in both directions:** shipping a finance agent at L1 (unsafe), or
gold-plating a prototype to L6 (wasted weeks). Match the rung to the stakes.

## Q&A insights

_(To be filled as we go deeper.)_

## Related

- Companion to [[Orchestrator]] — this is the detailed build-up of that note's ladder.
- Part of [[02 Agent Architecture and Orchestration]] · [[AI Agents MOC]]

**Rungs that are big enough to be their own concepts** (each link explained):

- [[Agent Memory]] **(Level 2)** — *where and how the agent remembers.* The
  external state store is the orchestrator's mechanism; Agent Memory is the
  broader topic of working/episodic/semantic/procedural memory it enables.
- [[Guardrails]] **(Level 3)** — *the enforcement layer that vets actions before
  they run.* Policy checks, approval gates, and the safe-default rules that sit
  between the LLM's proposal and execution.
- [[Termination Conditions]] **(Level 3)** — *how the loop is forced to stop.*
  Max steps, token/cost budgets, and done-detection so an agent can't run away.
- [[Durable Execution]] **(Level 6)** — *crash-and-resume for long runs.* A
  workflow engine checkpoints each step so a deploy or crash mid-run resumes
  instead of restarting; pairs with [[Stateless Orchestrator Design]].
- [[Observability]] **(Level 5)** — *seeing inside a multi-step run.* Traces,
  logs, and metrics that let you replay a trajectory and find where a
  non-deterministic agent went wrong.
- [[Tool Calling]] **(Level 1)** — *how the agent invokes tools.* The registry,
  schemas, and validation that turn an LLM's proposed call into a safe execution.
