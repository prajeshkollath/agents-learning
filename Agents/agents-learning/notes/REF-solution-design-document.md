# REF - Solution Design Document (SDD) for AI Projects

**Purpose:** Reference for writing Solution Design Documents after discovery — covering guardrails, evals, AI Ops, and all implementation-level decisions. Also maps what RFP evaluators will ask for as proof/output at each stage.

---

## How This Document Fits in the Process

```
Stage 1: Discovery          Stage 2: RFP Response        Stage 3: SDD
────────────────────        ─────────────────────        ──────────────────
What is the problem?   →    What will we build?      →   How will we build it?
Use case classification     Architecture landscape        Guardrails design
Stack recommendation        Risk mapping                  Eval framework
Effort sizing               Phasing                       AI Ops plan
                                                          Rollout plan

Output: Discovery Report    Output: Technical Proposal    Output: SDD
Audience: Client sponsors   Audience: Evaluation panel    Audience: Eng team + client
```

> **RFP panels will ask for SDD-level detail** even during the proposal stage — especially for regulated industries, enterprise clients, or high-risk use cases. Prepare answers for every section below before the presentation.

---

## Section 1 — Solution Overview

**What goes here:** A one-page recap of what was found in discovery and what is being proposed. Ties the SDD back to the problem statement.

**Structure:**
- Problem statement (one paragraph — their words, not yours)
- Proposed solution (one paragraph — what you're building)
- Use case class (from discovery classification)
- Out of scope (what you are explicitly NOT building)
- Success definition (measurable — not "users will be happy")

**What RFP evaluators ask for:**
- "How did you arrive at this solution?" → Show the discovery → classification → decision path
- "What are you not doing and why?" → Out of scope section prevents scope creep disputes
- "How will we know it worked?" → Success definition with metrics

---

## Section 2 — Detailed Architecture

**What goes here:** The full architecture diagram with every component named, owned, and connected.

**Required components in the diagram:**
```
For every component, document:
  - Name (what it is)
  - Technology choice (specific product/service)
  - Owner (which team manages it)
  - Data in / Data out
  - Failure behaviour (what happens if this component goes down)
```

**Standard components to account for:**

| Component | Examples | Who Owns |
|-----------|---------|---------|
| User interface | Web app, Slack, API | Product/Frontend |
| Orchestration | LangChain, ADK, custom | AI Engineering |
| LLM gateway | Bedrock, Vertex, Azure OpenAI, Direct API | AI/Infra |
| Model | Claude, Gemini, GPT, Llama | AI team (selection) |
| Vector DB | OpenSearch, pgvector, Chroma | Data/Infra |
| Document store | S3, GCS, SharePoint, Confluence | Data/IT |
| Memory store | Redis, DynamoDB, CosmosDB | App/Infra |
| Tool integrations | CRM API, ticketing, email, database | App Engineering |
| Guardrails layer | Input filter, output filter | AI Engineering |
| Eval pipeline | Offline eval suite, online monitors | AI/QA |
| Observability | Logging, tracing, dashboards | DevOps/AI Ops |
| Auth & IAM | SSO, RBAC, API keys | Security/Infra |

**What RFP evaluators ask for:**
- "Show us the data flow end to end" → Sequence diagram: user → system → LLM → output → storage
- "What are the integration points?" → Named APIs, DB connections, auth method for each
- "What happens if the LLM is unavailable?" → Failure behaviour per component

---

## Section 3 — Guardrails Design

> **Guardrails = controls that prevent the AI from doing harm, going off-topic, or producing unsafe output.**
> They sit at the input (what goes IN to the model) and output (what comes OUT of the model).

### Guardrail Types

```
INPUT GUARDRAILS                    OUTPUT GUARDRAILS
────────────────                    ─────────────────
PII detection & redaction           Hallucination detection
Topic/scope restriction             Toxicity / harmful content filter
Prompt injection detection          PII in output scrubbing
Rate limiting per user              Confidence scoring
Input length limits                 Factual grounding check (vs. source)
Language filtering                  Format validation (is it valid JSON?)
```

### Guardrail Patterns

**Pattern 1 — LLM-as-Judge (Meta-evaluation)**
A second, cheaper LLM call evaluates the output before returning it to the user.
```
User input → Main LLM → Candidate output
                              ↓
                   Judge LLM (checks: safe? grounded? on-topic?)
                              ↓
                   PASS → return to user
                   FAIL → fallback response or human escalation
```
- Cost: ~10-20% overhead (cheaper model as judge)
- Best for: high-risk outputs, regulated content

**Pattern 2 — Rules-Based Filter**
Deterministic checks — no LLM involved, just code.
```
Output → regex / keyword scan → block list check → PII pattern match → pass/fail
```
- Cost: negligible
- Best for: PII scrubbing, profanity filters, format validation

**Pattern 3 — Grounding Check (RAG-specific)**
Verify that the answer is supported by retrieved source documents.
```
LLM answer + source chunks → check: does answer contradict sources?
```
- Cost: one extra LLM call
- Best for: RAG systems where hallucination on factual queries is a risk

**Pattern 4 — Scope Restriction (System Prompt)**
Tell the model what it is and is not allowed to discuss.
```
System prompt: "You are an assistant for [Company] HR policies only.
               If asked about anything outside HR policy, say:
               'I can only help with HR-related questions.'"
```
- Cost: zero extra calls
- Best for: focused use cases where out-of-scope queries are common

**Pattern 5 — Prompt Injection Detection**
Detect attempts to override system instructions via user input.
```
User input → classifier: is this a jailbreak / prompt injection attempt?
→ YES → block + log + alert
→ NO  → proceed to LLM
```

### Guardrail Decision Table (what to use when)

| Risk | Guardrail to apply |
|------|--------------------|
| PII in inputs (names, emails, IDs) | Input PII redaction before LLM call |
| PII in outputs | Output PII scrubbing before returning to user |
| Off-topic queries | Scope restriction in system prompt + classifier |
| Harmful / toxic content | Output toxicity filter (rules-based or LLM-judge) |
| Hallucination on facts | Grounding check (RAG) or LLM-as-judge |
| Prompt injection attacks | Input injection classifier |
| Agentic actions (irreversible) | Human approval gate before execution |
| Low confidence answers | Confidence threshold + escalation |

**What RFP evaluators ask for:**
- "How do you prevent the AI from saying something wrong or harmful?" → Guardrail patterns + where they sit in the flow
- "How do you handle PII?" → Input redaction + output scrubbing + audit log
- "What happens if someone tries to jailbreak it?" → Prompt injection detection
- "Who is responsible when it gets it wrong?" → Human-in-the-loop design + audit trail

---

## Section 4 — Evaluation Framework

> **Evals = how you measure whether the AI is performing correctly.**
> Without evals, you cannot claim the system works. Every RFP panel will ask for this.

### Three Types of Evals

**1. Offline Evals (Pre-deployment)**
Run against a fixed test dataset before releasing any version.
```
Test dataset (golden Q&A pairs)
     ↓
Run model on all test cases
     ↓
Score each output (automated or human)
     ↓
Compare to baseline / threshold
     ↓
PASS threshold → deploy | FAIL → fix and re-run
```

**2. Online Evals (Post-deployment, continuous)**
Running checks on live production traffic — a sample of real requests.
```
Live requests (10% sample)
     ↓
Automated scorer (LLM-as-judge or rules)
     ↓
Metrics logged to dashboard
     ↓
Alert if metric drops below threshold
```

**3. Human Evals**
Human reviewers score a sample of outputs — the ground truth.
```
Weekly sample of 50-100 outputs
     ↓
Domain expert rates: correct / partially correct / wrong
     ↓
Score feeds back into eval dataset and model improvement
```

### What to Measure (Metrics by Use Case Class)

| Use Case | Key Metrics |
|----------|------------|
| Q&A / RAG (Class 1) | Answer correctness, groundedness (% answers supported by source), retrieval precision (did it find the right chunk?) |
| Content Generation (Class 2) | Factual accuracy, tone match, format compliance, human preference score |
| Classification (Class 3) | Precision, recall, F1 score per category, confusion matrix |
| Data Extraction (Class 4) | Field accuracy (% fields correctly extracted), false positive rate |
| Conversational (Class 5) | Task completion rate, user satisfaction (CSAT), escalation rate |
| Agentic (Class 6) | Task success rate, tool call accuracy, hallucinated actions %, steps to completion |
| Multi-Agent (Class 7) | End-to-end task success, agent handoff accuracy, total cost per task |

### Eval Dataset — What It Is and How to Build It

```
Golden dataset = a set of inputs with known correct outputs
                 used to test the model every time you deploy

How to build:
  Phase 1 (pre-launch): SMEs write 50-200 test cases by hand
  Phase 2 (post-launch): capture real user queries + human-label the correct answer
  Phase 3 (ongoing): flag edge cases and failures → add to dataset
```

**Minimum viable eval dataset sizes:**
- Classification: 200+ examples per category
- RAG Q&A: 100+ question-answer-source triples
- Extraction: 50+ documents with labelled field values
- Agentic: 30+ end-to-end task scenarios

### Regression Testing

Every time the model changes (new model version, new prompt, new tools), re-run the full eval suite.

```
New model version released
     ↓
Run offline eval suite (golden dataset)
     ↓
Compare scores to previous version
     ↓
Regression? (score dropped > 5%?) → block deployment
No regression → approve deployment
```

**What RFP evaluators ask for:**
- "How do you know it's accurate?" → Eval framework + metrics + dataset size
- "What is your accuracy target?" → Threshold per metric per use case
- "How do you test before deploying a new version?" → Regression testing process
- "Who validates the outputs?" → Human eval cadence + who the reviewers are
- "What's your baseline?" → Current human performance or previous system performance

---

## Section 5 — AI Ops & Monitoring

> **AI Ops = keeping the system healthy in production.**
> Different from standard software monitoring because models degrade silently — no errors, just worse answers.

### What to Monitor

**Infrastructure metrics (same as any software):**
- API latency (p50, p95, p99)
- Error rate (API timeouts, failed requests)
- Throughput (requests per second)
- Cost per request / daily spend

**AI-specific metrics (unique to LLM systems):**

| Metric | What it means | Alert threshold |
|--------|--------------|----------------|
| Answer quality score | Ongoing eval score from LLM-judge on live traffic | Drop >5% from baseline |
| Hallucination rate | % outputs that contain ungrounded claims | >2% |
| Retrieval precision | % correct chunks retrieved (RAG) | Drop >10% |
| Escalation rate | % queries escalated to human | Spike >20% above baseline |
| User rejection rate | % outputs user explicitly rejected / thumbs-downed | Spike >15% |
| Token usage per query | Average input+output tokens | Spike = prompt injection or runaway agent |
| Tool failure rate | % tool calls that errored (agentic) | >5% |

### Drift Detection

Models degrade over time even without code changes — because the real world changes.

**Types of drift:**
```
Data drift:    User queries change in topic/style → retrieval misses
Model drift:   Provider updates the model silently → behaviour changes
Concept drift: The right answer changes (policy updates, new products)
```

**How to detect:**
```
Weekly: compare current eval score to 4-week rolling average
Monthly: human review sample of 100 live outputs
Quarterly: full re-evaluation against golden dataset
On any provider model update: run regression suite immediately
```

### Model Versioning & Update Policy

```
New model version available (e.g., Claude Sonnet 4.7 releases)
     ↓
Run eval suite on new version (shadow mode — no live traffic)
     ↓
Compare: better / same / worse than current?
     ↓
Better on key metrics → schedule upgrade with change control
Same → optional (monitor for cost/latency improvements)
Worse on any key metric → stay on current version
```

**Shadow mode testing:**
```
Production traffic → Current model → Live response to user
                  ↘ New model    → Logged only (not shown to user)
                                    Compare outputs offline
```

### Incident Response

**Severity levels:**

| Severity | Definition | Response Time | Action |
|----------|-----------|--------------|--------|
| P1 — Critical | AI producing harmful/dangerous output | Immediate | Kill switch → fallback → human takeover |
| P2 — High | Accuracy drop >20%, high escalation rate | 2 hours | Rollback to previous version |
| P3 — Medium | Accuracy drop 5-20%, anomalous behaviour | 24 hours | Investigate, patch, redeploy |
| P4 — Low | Minor quality issues, isolated incidents | Next sprint | Add to eval dataset, tune prompt |

**Kill switch design (for agentic systems):**
```
Every agentic system must have:
  1. Immediate disable — turn off agent, queue requests
  2. Rollback — revert to previous version in <15 minutes
  3. Human takeover path — manual process documented for every automated task
  4. Audit log — every action the agent took, retrievable within minutes
```

**What RFP evaluators ask for:**
- "How do you know when it stops working?" → Monitoring dashboard + alert thresholds
- "What do you do when it fails?" → Incident response plan + severity levels
- "Can you turn it off immediately?" → Kill switch design
- "How do you handle model updates from the provider?" → Model versioning policy
- "Who is on-call?" → AI Ops ownership, escalation path

---

## Section 6 — Data Pipeline & Refresh Strategy

**What goes here:** How data gets into the system and stays current.

### For RAG Systems

```
Source documents (SharePoint, Confluence, S3, DB)
     ↓
Ingestion pipeline (scheduled or event-triggered)
     ↓
Chunking → Embedding → Vector DB
     ↓
Available to retriever at query time
```

**Refresh triggers:**

| Trigger | Example | Approach |
|---------|---------|---------|
| Scheduled | Nightly re-index of all docs | Full or incremental refresh |
| Event-driven | New document uploaded → immediate index | Webhook → ingestion job |
| Manual | Admin triggers re-index after bulk update | UI or CLI command |

**What RFP evaluators ask for:**
- "What happens when our documents change?" → Refresh strategy + lag time
- "How do you handle deleted documents?" → Deletion propagation to vector DB
- "How fresh is the knowledge?" → Lag between source update and AI knowing about it

---

## Section 7 — Security Implementation

**Standard security controls for AI systems:**

| Control | Implementation |
|---------|---------------|
| Authentication | SSO / OAuth2 for user access, API keys rotated regularly |
| Authorisation | RBAC — user can only query data they have permission to see |
| Data in transit | TLS 1.2+ on all API calls |
| Data at rest | Encryption at rest on vector DB, memory store, logs |
| PII handling | Redact before LLM call, scrub from output, never log raw PII |
| Prompt confidentiality | System prompt not exposed to users |
| Audit logging | Every query, every action, every model call logged with user ID + timestamp |
| Rate limiting | Per-user and per-tenant request limits |
| VNet / Private endpoint | If using Bedrock / Azure / Vertex — no traffic over public internet |

**What RFP evaluators ask for:**
- "Where does our data go?" → Data residency, VNet design, provider's data policy
- "Who can see the logs?" → Log access controls
- "Can your AI access data the user isn't allowed to see?" → Auth-scoped retrieval design
- "What data do you store and for how long?" → Retention policy

---

## Section 8 — Rollout Plan

**Standard phases:**

```
Phase 1 — POC (2-6 weeks)
  Goal: prove the concept works on a small dataset / controlled scenario
  Users: internal team only
  Evals: manual, ad-hoc
  Success: "does it produce reasonable output?"

Phase 2 — Pilot (4-12 weeks)
  Goal: test with real users on real data, measure quality formally
  Users: limited group (10-50 users)
  Evals: offline eval suite in place, human review weekly
  Success: eval metrics above threshold, users prefer it to current process

Phase 3 — Production (ongoing)
  Goal: full rollout with AI Ops in place
  Users: all target users
  Evals: continuous online eval, weekly human review, quarterly regression
  Success: sustained quality metrics, measurable business impact (time saved, cost reduced)
```

**Rollback plan (must exist before go-live):**
```
For every production deployment, document:
  - How to revert to previous version (< 15 min target)
  - How to revert to manual process (if AI is fully down)
  - Who approves the rollback decision
  - Who communicates to users
```

---

## Section 9 — Effort & Team

**Typical team composition for an AI project:**

| Role | Responsibility | When needed |
|------|---------------|------------|
| AI Engineer | Prompts, agent logic, framework, evals | Full project |
| Backend Engineer | APIs, integrations, tool connections | Full project |
| Data Engineer | Vector DB, ingestion pipeline, embeddings | RAG projects |
| Infrastructure / DevOps | Cloud setup, VNet, monitoring, CI/CD | Phase 2 onwards |
| Security / Compliance | PII design, audit logging, compliance review | Phase 2 onwards |
| Domain SME | Eval dataset creation, output review | Phase 1 + ongoing |
| Product Manager | Requirements, user feedback, roadmap | Full project |

---

## What RFP Panels Will Ask — Master List

Collect answers to these before any RFP presentation:

**On solution design:**
- How did you arrive at this architecture?
- What alternatives did you consider and reject?
- What is explicitly out of scope?

**On guardrails:**
- How do you prevent harmful or incorrect output?
- How do you handle PII?
- What happens if someone tries to manipulate the AI?
- Who is responsible when the AI is wrong?

**On evals:**
- How do you know it's accurate?
- What is your accuracy target and how did you set it?
- How do you test before deploying a new version?
- Who validates the outputs and how often?

**On AI Ops:**
- How do you know when it stops working?
- How quickly can you detect and respond to a quality drop?
- What is your process when the model provider releases a new version?
- Can you disable it immediately if something goes wrong?
- Who is responsible for ongoing monitoring?

**On data:**
- Where does our data go?
- What data do you store and for how long?
- How fresh is the AI's knowledge?
- What happens when our documents change?

**On security:**
- Can the AI access data the user isn't allowed to see?
- Who can see the query logs?
- How is data encrypted in transit and at rest?

**On rollout:**
- What does the POC look like?
- How do we measure success at each phase?
- What is the rollback plan?

---

[← Solution Discovery & RFP](REF-solution-discovery-rfp.md) | [← AI SDKs Reference](REF-ai-sdks-and-apis.md) | [← Back to ROADMAP](../ROADMAP.md)
