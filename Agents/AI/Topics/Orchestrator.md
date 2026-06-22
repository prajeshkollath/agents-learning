---
title: Orchestrator
created: 2026-06-22
updated: 2026-06-22
tags:
  - ai-agents
  - architecture
  - orchestration
  - infrastructure
status: learning
aliases:
  - Agent Orchestrator
  - Agent Runtime
  - Harness
  - Agent Controller
---

# Orchestrator

> **The orchestrator is the application; the LLM is a function it calls.**
> Everything that makes an agent a *running system* — the loop, memory, tool
> execution, rules, logging — lives here. Strip the LLM out and you still have a
> program; strip the orchestrator out and you have a chatbot that can't *do*
> anything.

## What it is

The deterministic program that runs the agent — the *runtime* / *harness* /
*controller* around the model.

Two analogies that stick:
- **LLM = brain; orchestrator = body + nervous system + rulebook.** The brain
  reasons; the body senses, acts, remembers, and refuses to touch the hot stove.
- **LLM = CPU; orchestrator = operating system.** The OS schedules work, manages
  memory, enforces permissions, talks to devices; the CPU just computes when asked.

See the responsibility split in [[Orchestrator vs LLM Responsibilities]].

## Its job (the spec)

The loop · state/memory · tool dispatch · enforcement/[[Guardrails]] · output
validation · [[Observability]] · retries/idempotency · cost control · the
security boundary. That's *what* it does — the rest of this note is *how you
build and ship one*.

## Types of orchestrator (the options)

Four independent axes; a real orchestrator is one choice on each.

**Axis 1 — Control model** (who drives the next step):
- **Workflow / code-driven** — fixed graph/DAG, you hardcode the steps. Predictable, cheap, testable. *(LangGraph graphs, prompt chains.)*
- **Autonomous / LLM-driven** — the model picks the next action each turn. Flexible, less predictable. *(ReAct / function-calling loops → [[ReAct Prompting]].)*
- **Hybrid** — code skeleton with LLM-driven nodes. Most production systems.
- See the full spectrum in [[Agents vs Workflows]].

**Axis 2 — Build approach** (build vs buy):
- **Roll-your-own** — a `while` loop in Python; ~20 lines to start. Max control, max effort.
- **Framework** — [[LangGraph]], LlamaIndex, [[CrewAI]], [[AutoGen]], Semantic Kernel, Pydantic AI, [[Claude Agent SDK]], OpenAI Agents SDK, Google ADK. They give you the loop, tool plumbing, state, tracing hooks.
- **Managed / hosted** — OpenAI Assistants, AWS Bedrock Agents, Azure AI Agent Service, Vertex AI Agent Builder. They run the loop for you. Least control, fastest to ship.

**Axis 3 — Execution model** (how it runs over time):
- **In-process / synchronous loop** — runs inside one request. Simple; dies if the process dies. Fine for short agents (seconds).
- **Durable execution** — backed by a workflow engine (Temporal, Restate, AWS Step Functions, Inngest) that checkpoints every step so it can **crash and resume**. Needed for long-running agents → [[Durable Execution]], [[Stateless Orchestrator Design]].
- **Event-driven / queue-based** — steps flow through queues/event buses. Scales, decouples, good for multi-agent → [[Agent Communication Protocols]].

**Axis 4 — Topology:**
- **Single-agent** — one loop, one model.
- **Multi-agent** — a supervisor orchestrator coordinating sub-agents → [[Multi-Agent Systems]].

## How to build one (maturity ladder)

Start at Level 0; add layers only as production demands them.

```
Level 0  while-loop + llm() + tool dispatch        ← works on your laptop
Level 1  + tool registry & schema validation
Level 2  + state store (in-mem → Redis/Postgres)
Level 3  + guardrails / policy + termination & budget caps
Level 4  + retries, idempotency, error handling, fallbacks
Level 5  + tracing/observability (OTel, Langfuse, LangSmith)
Level 6  + streaming, concurrency, durable execution
```

Levels map to: [[Tool Calling]], [[Agent Memory]], [[Guardrails]],
[[Termination Conditions]], [[Observability]], [[Durable Execution]].
**The art is not over-building** — a demo needs L0–1; a finance agent needs all.

## How to deploy it

**Packaging — how it's exposed:**
- **Sync API** (FastAPI/Flask, request/response) — short agents only; HTTP times out (~30–60 s).
- **Async job + webhook/polling** — submit task → return job ID → background worker runs it → poll/callback. Standard for agents that run minutes.
- **Streaming** (SSE / WebSocket) — stream tokens/steps to the user live.

**Where it runs:** container on Cloud Run / ECS / Kubernetes; serverless (Lambda)
for short tasks; persistent queue-worker for long tasks.

**The scaling rule:** keep the **orchestrator process stateless** — push all
state to an external store. Then run N identical instances behind a load
balancer; any instance handles any request, and a crash loses nothing. This is
[[Stateless Orchestrator Design]] — the key deployment insight.

**Production infra to wire in:**
- Rate limiting toward the **model API** (provider limits hit fast under load)
- **Secrets management** (orchestrator holds API keys; the LLM never sees them)
- Observability backend (traces for multi-step debugging)
- Cost monitoring (token spend per run)
- Autoscaling + concurrency caps

### Concrete deployment sketch

```
                 ┌──────────────┐     enqueue      ┌───────────┐
   client ──────▶│  FastAPI     │ ───────────────▶ │  queue    │
   (POST /run)   │  (stateless) │                  │ (SQS/Redis)│
                 └──────┬───────┘                  └─────┬─────┘
                        │ return job_id                  │ pull
   client ◀── job_id ───┘                                ▼
                                              ┌────────────────────┐
   client ──▶ GET /status/{job_id} ──────────│  worker (the loop) │
                        ▲                     │  llm + tools       │
                        │ read                └──────┬─────────────┘
                 ┌──────┴───────┐   read/write       │
                 │  Postgres    │◀───────────────────┘
                 │  (state)     │   step-by-step persistence
                 └──────────────┘
```

API and worker are both **stateless**; Postgres holds run state → both scale
horizontally and survive restarts.

## Architect's decision summary

| Decision | Cheap/fast | Robust |
|---|---|---|
| Build approach | Managed (Bedrock/Assistants) | Roll-your-own / framework |
| Control model | Workflow (code) | Autonomous (LLM) |
| Execution | In-process loop | Durable (Temporal) |
| State | In-memory | External (Postgres/Redis) |
| Deploy | Sync API | Async workers + queue |

Default **left** for prototypes; move **right** as reliability/scale demands.

## Examples

- **Claude Code (this session)** — orchestrator that built prompts, ran tools,
  persisted state, and **blocked the `git push` to main**.
- **Production pattern** — FastAPI + queue + worker running a [[LangGraph]] agent
  on Cloud Run, Postgres for state, Langfuse for tracing.

## Constraints
- LLM is stateless → orchestrator carries all state.
- Context limits → orchestrator curates what's in the prompt ([[Context Window Management]]).
- Model latency → minimize calls.
- Provider rate limits → throttle and queue under load.

## Likely issues
- HTTP timeout kills a long agent mid-run → use async/durable.
- Stateful orchestrator can't scale horizontally → externalize state.
- Framework "magic" hides the prompt/loop → undebuggable; know what it generates.
- No idempotency → a retried run repeats side effects (double charge).

## Tradeoffs
- **Framework vs roll-your-own:** frameworks save weeks but add abstraction you
  debug *through*; a hand-rolled loop is more code but fully understood. Common
  arc: start with a framework, hit limits, rewrite the core loop.
- **Managed vs self-hosted:** managed = fast, less control, lock-in, opaque
  internals; self-hosted = full control, full ops burden.
- **Sync vs durable:** durable execution is bulletproof but real infra to run/learn.

## Cost
- **Build:** roll-your-own = high dev time; managed = low dev, higher per-call fees + lock-in.
- **Run:** orchestrator compute is cheap; **LLM calls dominate**; durable engines add infra cost. See [[Token Cost Optimization]], [[Caching Strategies]].

## Soundbite
> *"The orchestrator is the application; the LLM is a function it calls. Build the
> smallest loop that works, keep it stateless so it scales, externalize state so
> it survives crashes, and reach for a framework or durable engine only when the
> problem demands it."*

## Q&A insights

_(To be filled as we go deeper.)_

## Related
- Defined in [[Orchestrator vs LLM Responsibilities]] · part of [[02 Agent Architecture and Orchestration]] · [[AI Agents MOC]]
- [[Stateless Orchestrator Design]] — keep it stateless to scale & resume
- [[Durable Execution]] — crash-and-resume for long-running agents
- [[Designing a Safe Agent Loop]] — the loop the orchestrator runs
- [[Termination Conditions]] — an orchestrator responsibility
- [[Guardrails]] — the enforcement layer
- [[Observability]] — tracing the multi-step loop
- [[Agents vs Workflows]] — the control-model spectrum
- Frameworks: [[LangGraph]] · [[CrewAI]] · [[AutoGen]] · [[Claude Agent SDK]]
