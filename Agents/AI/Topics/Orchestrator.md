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

## What the orchestrator performs (its responsibilities)

This is *what* it does — each item **branches to its own detailed page** (drilled
as we go). The rest of *this* note is *how you build and ship one*.

**Control flow**
- [[Agent Loop]] — the perceive → reason → act → observe cycle the orchestrator runs.
- [[Routing]] — choosing the next step, branch, or sub-agent.
- [[Termination Conditions]] — forcing the loop to stop (max steps, budget, done-detection).

**State & context**
- [[State Management]] — the live execution state (current step, scratchpad), persisted so runs survive restarts.
- [[Agent Memory]] — longer-term recall (working / episodic / semantic / procedural).
- [[Context Building]] — assembling each prompt from state + memory + tool specs ("context engineering").

**Tools & I/O contracts**
- [[Tool Calling]] — dispatching the LLM's chosen tool with its arguments.
- [[Schemas]] — the structured input/output contracts for tools and responses.
- [[Output Validation]] — runtime checking/parsing of the LLM's output *before* acting on it.

**Reliability**
- [[Error Handling]] — catching tool/model failures without crashing the run.
- [[Retries and Idempotency]] — retrying safely so a repeat doesn't double-act.
- [[Fallback Strategies]] — switching model / tool / path when the primary fails.

**Safety & governance**
- [[Guardrails]] — policy/permission enforcement between the LLM's proposal and execution.
- [[Security Boundary]] — secrets, auth, and sandboxing the LLM never crosses (see [[Sandboxed Execution]]).

**Operations**
- [[Observability]] — logs, traces, and metrics across every step (your "logs/tracing").
- [[Cost Control]] — token accounting and budget caps per run.

> **"Evals" vs "output validation" — these are different, don't conflate them.**
> [[Output Validation]] is a *runtime* orchestrator check: *is this single
> response well-formed and safe to act on?* [[Agent Evaluation]] is *quality
> measurement of the agent across many runs* — a separate domain
> ([[08 Evaluation]]), not a per-step orchestrator function.

## Types of orchestrator (the options)

These are **four independent dimensions, not a menu you pick one item from.**
**Every real orchestrator sits on all four axes at once** — to *describe* an
orchestrator you state where it sits on each.

> **Analogy — ordering coffee.** *Size*, *milk*, *hot/iced*, and *shots* are
> independent axes; you don't pick "size OR milk," you choose a value on *each*.
> Same here: one orchestrator = one choice on every axis simultaneously.

| #   | Axis                | The question it answers       | Options                                                   |     |
| --- | ------------------- | ----------------------------- | --------------------------------------------------------- | --- |
| 1   | **Control model**   | *Who decides the next step?*  | code-driven (workflow) ↔ LLM-driven (autonomous) ↔ hybrid |     |
| 2   | **Build approach**  | *Who wrote the orchestrator?* | roll-your-own ↔ framework ↔ managed/hosted                |     |
| 3   | **Execution model** | *How does it run over time?*  | in-process loop ↔ durable ↔ event-driven/queue            |     |
| 4   | **Topology**        | *How many agents?*            | single-agent ↔ multi-agent                                |     |

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

### One orchestrator, plotted on all four

Same word "orchestrator", four independent knobs → completely different systems:

| | Axis 1 Control | Axis 2 Build | Axis 3 Execution | Axis 4 Topology |
|---|---|---|---|---|
| **Claude Code** (this session) | LLM-driven | managed/framework | in-process loop | single-agent |
| **Production refund agent** | hybrid | framework (LangGraph) | durable (Temporal) | single-agent |

**Interview point:** "workflow vs agent" is only *Axis 1*. An architect names where
the system sits on **all four** and why — e.g. *"LLM-driven control because the task
is open-ended, but durable execution because runs take 20 minutes and we can't lose
progress."* That combination **is** the design.

### How the axes interact

The axes are independent, but choices on one **pull** you toward choices on
another. The common couplings:

- **Control (1) → Execution (3):** LLM-driven control means an *unpredictable*
  number of steps and longer runs → pushes you toward **durable execution** +
  hard [[Termination Conditions]]. A fixed workflow has predictable runtime, so an
  in-process loop is usually fine.
- **Topology (4) → Execution (3):** multi-agent systems need agents to talk →
  pushes you toward **event-driven / queue-based** execution ([[Agent Communication Protocols]]). A single agent runs happily as one in-process loop.
- **Topology (4) → Build (2):** multi-agent is a lot to hand-roll → pushes you
  toward frameworks built for it ([[CrewAI]], [[AutoGen]]).
- **Build (2) → Execution (3):** **managed/hosted** services lock you into *their*
  execution model — you often **can't** add your own durable engine. Rolling your
  own keeps Axis 3 fully open.
- **Control (1) → Build (2):** a simple autonomous loop is ~20 lines (roll-your-own
  is easy); a complex branching workflow graph is where a framework like
  [[LangGraph]] earns its keep.

**Takeaway:** pick the axis your *hardest constraint* lives on first (e.g. "runs
take 20 min, can't lose progress" → Execution = durable), then let that pull the
others into place.

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

> **Full walkthrough:** see [[Orchestrator Maturity Ladder]] for each rung
> explained with real-life triggers and the infrastructure it requires.

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

**Q: What are the "4 axes" meant to be — do I pick one?**
No. They are **independent dimensions, not a menu.** Every orchestrator sits on
*all four at once*; to describe one you state its value on each (like ordering
coffee: size + milk + temperature + shots are separate choices, not alternatives).
"Workflow vs agent" is only Axis 1 — naming all four (control, build, execution,
topology) and *why* is the actual architect-level answer. See the worked table
above (Claude Code vs a refund agent plotted across all four).

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
