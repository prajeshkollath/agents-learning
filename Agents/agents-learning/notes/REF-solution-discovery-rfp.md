# REF - Solution Discovery & RFP Preparation for AI/Agent Projects

**Purpose:** A structured playbook for discovery conversations, solution design, and RFP responses involving AI, LLMs, and agents.

---

## The Discovery Mindset

> **Never recommend a solution before you understand the problem.**
> Most clients come in saying "we want AI" or "we want an agent" — your job in discovery is to find out what they actually need, which is often simpler (or more complex) than what they asked for.

Three questions that cut through the noise:
1. **What does a human do today that you want AI to do?**
2. **What does "good" look like — how will you know it worked?**
3. **What happens if it gets it wrong?**

---

## Phase 1 — Discovery Questions (What to Ask)

### About the Problem
- What is the task or process you want to improve/automate?
- Who does this today, and how long does it take?
- How often does this happen? (one-off vs. real-time vs. batch)
- What inputs go in? (text, documents, images, structured data, audio?)
- What output is expected? (text, action, structured data, decision?)

### About the Data
- Where does the data live? (internal docs, databases, APIs, emails, PDFs?)
- Is the data structured or unstructured?
- How sensitive is the data? (PII, financial, health, confidential IP?)
- How fresh does the data need to be? (real-time vs. updated weekly vs. static knowledge)

### About Users
- Who are the end users? (employees, customers, developers, executives?)
- What's their technical comfort level?
- Is this human-in-the-loop (human approves actions) or fully automated?
- What's the volume? (10 users vs. 10,000 concurrent users?)

### About Risk & Compliance
- What industry are you in? (finance, healthcare, legal = high compliance)
- Are there regulations to comply with? (GDPR, HIPAA, SOC2, ISO27001?)
- What's the cost of a wrong answer? (minor inconvenience vs. legal liability?)
- Does data need to stay within a specific region or cloud?

### About Infrastructure
- What cloud does the client use? (AWS, Azure, GCP, on-prem, hybrid?)
- What existing systems need to connect? (CRM, ERP, databases, APIs?)
- What's the expected scale? (concurrent users, requests per second?)
- Is there an existing AI/ML platform or team?

### About Budget & Timeline
- Is this a POC, pilot, or production system?
- What's the budget range? (affects model choice — GPT-4o vs. Haiku 4.5 is 20x cost difference)
- What's the deadline driving this? (compliance date, product launch, board demo?)

---

## Phase 2 — Use Case Classification

Once you understand the problem, classify it. Each class maps to a different architecture.

### Class 1 — Q&A / Information Retrieval
**What it is:** User asks questions, AI answers from a knowledge base.
**Examples:** Internal knowledge base chatbot, policy Q&A, product documentation assistant
**Key signal:** "We have documents/data and people keep asking the same questions"
**Architecture:** RAG (Retrieval Augmented Generation)
```
User Question → Search docs → Add context to prompt → LLM answers
```
**Complexity:** Low-Medium | **Risk:** Low | **Time to build:** 2-6 weeks

---

### Class 2 — Content Generation
**What it is:** AI generates text, reports, summaries, emails, code.
**Examples:** Auto-generate RFP responses, summarise meeting notes, write marketing copy, generate code
**Key signal:** "We spend hours writing the same type of document"
**Architecture:** Single LLM call with structured prompt, possibly with templates
```
Input data + Template prompt → LLM → Generated content → Human review
```
**Complexity:** Low | **Risk:** Low-Medium (hallucination risk) | **Time to build:** 1-3 weeks

---

### Class 3 — Classification & Routing
**What it is:** AI reads input and categorises or routes it.
**Examples:** Support ticket routing, email triage, sentiment analysis, intent detection
**Key signal:** "We manually sort/categorise X every day and it's tedious"
**Architecture:** Classifier LLM call → downstream workflow
```
Input → LLM classifies → Routes to correct system/team/process
```
**Complexity:** Low | **Risk:** Medium (errors affect downstream) | **Time to build:** 1-2 weeks

---

### Class 4 — Data Extraction & Transformation
**What it is:** AI reads unstructured input and outputs structured data.
**Examples:** Extract fields from invoices/contracts, parse emails into CRM records, convert PDFs to structured JSON
**Key signal:** "We have humans reading documents and manually entering data"
**Architecture:** LLM with structured output (JSON mode / function calling)
```
Document → LLM extracts fields → Structured JSON → System of record
```
**Complexity:** Low-Medium | **Risk:** Medium | **Time to build:** 1-4 weeks

---

### Class 5 — Conversational Assistant (Stateful Chat)
**What it is:** Multi-turn conversation with memory of prior exchanges.
**Examples:** Customer support bot, HR assistant, sales assistant, onboarding guide
**Key signal:** "We need back-and-forth conversation, not just one-shot answers"
**Architecture:** LLM + conversation history + optional RAG + optional tools
```
User message → Add history + retrieved context → LLM responds → Store to history
```
**Complexity:** Medium | **Risk:** Medium | **Time to build:** 3-8 weeks

---

### Class 6 — Agentic Workflow (Tool Use)
**What it is:** AI takes actions in the world — reads systems, writes data, calls APIs.
**Examples:** AI that books meetings, files tickets, queries databases, runs reports, sends emails
**Key signal:** "We want AI to DO things, not just answer questions"
**Architecture:** Agent loop with tools
```
Goal → Agent thinks → Calls tool → Gets result → Thinks again → Calls next tool → Done
```
**Complexity:** High | **Risk:** High (actions are real) | **Time to build:** 6-16 weeks

---

### Class 7 — Multi-Agent System
**What it is:** Multiple specialised AI agents coordinated by an orchestrator.
**Examples:** Research → Write → Review → Publish pipeline, complex business process automation
**Key signal:** "The task is too complex for one agent, needs specialisation and parallelism"
**Architecture:** Orchestrator + specialised sub-agents
```
Orchestrator routes → Agent A (research) + Agent B (write) + Agent C (review) → Aggregated result
```
**Complexity:** Very High | **Risk:** Very High | **Time to build:** 3-6 months+

---

## Phase 3 — Architecture Decision Tree

```
Does it need to take actions in external systems?
├── YES → Agentic (Class 6 or 7)
│         Is it complex enough to need specialised agents?
│         ├── YES → Multi-Agent (Class 7)
│         └── NO  → Single Agent with tools (Class 6)
│
└── NO → Does it need conversation history?
          ├── YES → Conversational Assistant (Class 5)
          │         Does it need to search internal knowledge?
          │         ├── YES → Class 5 + RAG
          │         └── NO  → Class 5 only
          │
          └── NO → Is it one input → one output?
                    ├── Generate content?   → Class 2
                    ├── Classify/Route?     → Class 3
                    ├── Extract data?       → Class 4
                    └── Answer questions from docs? → Class 1 (RAG)
```

---

## Phase 4 — Technology Selection

### Model Selection

| Need | Recommended Model | Why |
|------|------------------|-----|
| Best reasoning, complex tasks | Claude Opus 4.6, GPT-4o, o1/o3 | Top capability |
| Balanced cost/performance | Claude Sonnet 4.6, GPT-4o mini | 80% capability, 20% cost |
| High volume, simple tasks | Claude Haiku 4.5, Gemini 2.0 Flash | Cheapest, fastest |
| Very large documents (>100K tokens) | Gemini 1.5 Pro (2M ctx), Claude (200K ctx) | Context window size |
| Coding/technical tasks | Claude Sonnet 4.6, GPT-4o | Strongest on code benchmarks |
| Real-time / low latency | Groq + Llama 3.3, Gemini 2.0 Flash | Fastest inference |
| Open source / self-hosted | Llama 3.3 70B via Ollama or Groq | No vendor dependency |

---

### Infrastructure Selection

| Client Situation | Gateway/Platform | SDK |
|-----------------|-----------------|-----|
| AWS-native | AWS Bedrock | `boto3` |
| Azure enterprise | Azure OpenAI | `openai` → Azure endpoint |
| GCP-native | Vertex AI | `google-cloud-aiplatform` |
| No cloud preference, direct API | Provider directly | Provider's own SDK |
| On-premise, air-gapped | Ollama (local models) | `openai` (compatible) |
| Multi-cloud, model-agnostic | Bedrock or Vertex as gateway | One gateway SDK |

---

### Framework Selection

| Situation | Framework | Why |
|-----------|-----------|-----|
| RAG-heavy (document search) | LlamaIndex | Purpose-built for retrieval pipelines |
| General agents + tools | LangChain | Most mature, largest ecosystem |
| Multi-agent, role-based | CrewAI | Clean abstraction for agent roles |
| Google ecosystem (GCP client) | Google ADK | Native Vertex AI deployment |
| Research / prompt optimisation | DSPy | Automatic prompt tuning |
| Simple, custom control | No framework (raw SDK) | Less overhead, full control |

---

## Phase 5 — Risk & Compliance Mapping

### Risk by Use Case Class

| Class | Action Risk | Hallucination Risk | Data Risk | Overall |
|-------|------------|-------------------|-----------|---------|
| 1 - Q&A / RAG | None | Medium (wrong answer) | Medium (sensitive docs) | Medium |
| 2 - Content Generation | None | High (fabricated facts) | Low | Medium |
| 3 - Classification | Low (routing error) | Low | Low | Low |
| 4 - Data Extraction | Low | Medium (missed fields) | Medium | Medium |
| 5 - Conversational | None-Low | Medium | Medium | Medium |
| 6 - Agentic | **High** (real actions) | Medium | High | **High** |
| 7 - Multi-Agent | **Very High** | Medium | High | **Very High** |

### Mitigation Strategies by Risk Type

**Hallucination risk:**
- Constrain model to retrieved context only (RAG with strict grounding)
- Use structured output (JSON schema) to limit free-form generation
- Human-in-the-loop review before output is used
- Confidence scoring + fallback to human

**Action risk (agentic):**
- Human approval gates for irreversible actions (send email, delete record, make payment)
- Dry-run mode before production deployment
- Audit log every action the agent takes
- Scope tools to minimum required permissions

**Data risk:**
- Use gateway with VNet/private endpoint (Bedrock, Azure OpenAI)
- No PII in prompts — anonymise before sending to LLM
- On-premise model for highest sensitivity (Ollama + Llama)
- Enforce data residency via cloud region selection

---

## Phase 6 — Sizing & Effort Estimation

### Rough Build Effort by Class

| Class | POC | Pilot | Production |
|-------|-----|-------|-----------|
| 1 - Q&A / RAG | 1-2 weeks | 4-6 weeks | 3-4 months |
| 2 - Content Generation | 3-5 days | 2-3 weeks | 6-8 weeks |
| 3 - Classification | 3-5 days | 2-3 weeks | 4-6 weeks |
| 4 - Data Extraction | 1 week | 3-4 weeks | 6-10 weeks |
| 5 - Conversational | 2-3 weeks | 6-8 weeks | 3-5 months |
| 6 - Agentic | 3-4 weeks | 8-12 weeks | 4-8 months |
| 7 - Multi-Agent | 4-6 weeks | 3-4 months | 6-12 months |

### Cost Signals (what drives API cost)

- **Volume:** requests per day × tokens per request
- **Model tier:** Opus/GPT-4o = 20-50x more expensive than Haiku/Flash
- **Context size:** large context = more tokens = more cost (RAG especially)
- **Caching:** repeated system prompts can be cached — 90% cost reduction on cached tokens (Gemini, Claude)
- **Rule of thumb:** prototype with best model, optimise down to cheapest model that still passes quality bar

---

## RFP Response — Standard Sections to Cover

When writing the technical response to an RFP:

1. **Understanding of Requirements** — restate the problem in your words to show you understood it
2. **Proposed Solution Architecture** — diagram + explanation of each layer (model, SDK, gateway, framework)
3. **Use Case Classification** — which class(es) this falls into and why
4. **Model & Provider Recommendation** — which model, why, with alternatives
5. **Data Flow** — how data moves from user → system → LLM → output → storage
6. **Security & Compliance** — how PII is handled, where data lives, audit logging
7. **Risk & Mitigation** — known risks and how the design addresses them
8. **Integration Points** — what existing systems connect and how
9. **Phasing** — POC → Pilot → Production milestones
10. **Effort & Team** — rough sizing, skills needed (ML engineer, backend, infra)

---

## One-Page Cheat Sheet (for Discovery Meetings)

```
DISCOVERY CHEAT SHEET
─────────────────────────────────────────────
FIRST: What does a human do today that AI should do?

INPUT?          OUTPUT?         FREQUENCY?
Text / Docs     Text answer     Real-time
Images          Structured data Batch / scheduled
Audio           Action taken    On-demand
Structured DB   Decision made

SENSITIVITY?    CLOUD?          COMPLIANCE?
Public          AWS             GDPR
Internal        Azure           HIPAA
Confidential    GCP             SOC2
Regulated       On-prem         Other

MAP TO CLASS:
  Answering from docs?     → RAG (Class 1)
  Writing / summarising?   → Generation (Class 2)
  Sorting / routing?       → Classification (Class 3)
  Pulling fields from docs?→ Extraction (Class 4)
  Back-and-forth chat?     → Conversational (Class 5)
  Taking actions?          → Agentic (Class 6)
  Complex multi-step?      → Multi-Agent (Class 7)

RISK CHECK:
  Wrong answer → inconvenience or liability?
  Wrong action → reversible or irreversible?
  Data → who sees it, where does it go?
─────────────────────────────────────────────
```

---

## Phase 7 — Complete Stack Examples (Common RFP Scenarios)

> For each scenario: Use Case Class → Model → Gateway/Platform → SDK → Framework → Architecture pattern

---

### Scenario 1: Internal Document Q&A (AWS Client)
**Client says:** "Our staff waste hours searching internal policies and manuals. We want to ask questions and get instant answers."

| Layer | Choice | Reason |
|-------|--------|--------|
| Use Case Class | Class 1 — RAG | Answering from internal docs |
| Model | Claude Sonnet 4.6 | Strong comprehension, 200K context |
| Gateway | AWS Bedrock | Client is AWS-native, data stays in AWS |
| SDK | `boto3` (Bedrock) | Single SDK via Bedrock |
| Framework | LlamaIndex | Purpose-built for RAG pipelines |
| Vector DB | Amazon OpenSearch or pgvector (RDS) | AWS-native, no extra infra |

```
Staff Question
     ↓
LlamaIndex retriever → searches OpenSearch (vector DB)
     ↓
Retrieved doc chunks + question → Bedrock (Claude Sonnet)
     ↓
Answer returned to staff UI
```

**Key architecture decisions:** Chunking strategy for long docs, embedding model (Titan or Cohere via Bedrock), refresh schedule for new documents.

---

### Scenario 2: Customer Support Chatbot (Azure Client)
**Client says:** "We want a chatbot to handle Tier 1 support queries, escalating to humans only when needed."

| Layer | Choice | Reason |
|-------|--------|--------|
| Use Case Class | Class 5 — Conversational + Class 3 — Classification | Chat + routing to human |
| Model | GPT-4o mini (routine) → GPT-4o (complex) | Cost-tier routing |
| Gateway | Azure OpenAI Service | Client is Azure-native, enterprise compliance |
| SDK | `openai` → Azure endpoint | Same SDK, Azure-hosted |
| Framework | LangChain | Handles conversation memory + routing logic |
| Memory | Azure Cosmos DB | Stores session history |

```
Customer message
     ↓
LangChain classifier → routine or complex?
     ↓                        ↓
GPT-4o mini             GPT-4o
(FAQ answers)           (complex reasoning)
     ↓                        ↓
Confidence check → below threshold?
     ↓ YES
Human escalation queue (existing CRM)
```

**Key architecture decisions:** Escalation threshold tuning, session timeout policy, handoff data format to human agents.

---

### Scenario 3: Contract Data Extraction (Regulated Industry, On-Premise)
**Client says:** "We process hundreds of contracts weekly. We want to extract key fields automatically — but data cannot leave our premises."

| Layer | Choice | Reason |
|-------|--------|--------|
| Use Case Class | Class 4 — Data Extraction | Structured fields from unstructured docs |
| Model | Llama 3.3 70B (self-hosted) | No data leaves client environment |
| Gateway | None — local inference | Air-gapped, on-prem requirement |
| SDK | `openai` SDK → Ollama endpoint | Ollama is OpenAI-compatible, runs locally |
| Framework | None or lightweight custom | Simple enough — one prompt, structured JSON out |
| Output | JSON → existing contract management system | Structured output mode |

```
Contract PDF → text extraction (OCR if needed)
     ↓
Ollama (Llama 3.3) with JSON schema prompt
     ↓
Structured JSON { party, value, dates, clauses }
     ↓
Contract Management System (existing)
```

**Key architecture decisions:** GPU sizing for local inference, OCR pipeline for scanned PDFs, validation layer to catch missed fields before system write.

---

### Scenario 4: Sales Content Generation (No Cloud Preference, Speed Priority)
**Client says:** "Our sales team spends hours writing proposals. We want AI to draft them from a brief."

| Layer | Choice | Reason |
|-------|--------|--------|
| Use Case Class | Class 2 — Content Generation | Text in → polished document out |
| Model | Claude Sonnet 4.6 | Best writing quality at mid cost |
| Gateway | None — direct Anthropic API | Simple use case, no cloud mandate |
| SDK | `anthropic` | Direct, simple |
| Framework | None | Single prompt → output, no agent loop needed |
| Caching | Prompt caching on system prompt | Company templates cached = 90% cost reduction |

```
Sales brief (bullet points, client name, deal context)
     ↓
anthropic SDK → Claude Sonnet 4.6
(system prompt = company tone + template — CACHED)
     ↓
Draft proposal → human review → send
```

**Key architecture decisions:** Template versioning, human review gate (never auto-send), feedback loop to improve prompts over time.

---

### Scenario 5: Automated Reporting Agent (GCP Client)
**Client says:** "Every Monday, someone manually pulls data from BigQuery, writes a summary, and emails it to leadership. We want this automated."

| Layer | Choice | Reason |
|-------|--------|--------|
| Use Case Class | Class 6 — Agentic | AI takes actions: query DB, write report, send email |
| Model | Gemini 2.0 Flash | GCP-native, fast, cost-effective for scheduled task |
| Gateway | Vertex AI | GCP-native deployment, managed scheduling |
| SDK | `google-cloud-aiplatform` | Vertex AI SDK |
| Framework | Google ADK | Native Vertex + BigQuery + Gmail tool integrations |

```
Scheduled trigger (Cloud Scheduler, every Monday 7am)
     ↓
ADK Agent
  → Tool: query BigQuery (last week's data)
  → Tool: generate summary (Gemini 2.0 Flash)
  → Tool: format as HTML report
  → Tool: send via Gmail API
     ↓
Leadership inbox
```

**Key architecture decisions:** Failure alerting (what if BigQuery query fails?), report approval gate for first N runs before full automation, audit log of every sent report.

---

### Scenario 6: Multi-Model Research Pipeline (Enterprise, Model-Agnostic)
**Client says:** "We want AI to research topics, synthesise findings, and produce briefing documents — but we don't want to be locked into one AI vendor."

| Layer | Choice | Reason |
|-------|--------|--------|
| Use Case Class | Class 7 — Multi-Agent | Research + synthesise + write = specialised agents |
| Model | Claude Sonnet (synthesis) + Gemini Flash (search/retrieval) | Right model for right task |
| Gateway | AWS Bedrock | Hosts both Claude and other models, single entry point |
| SDK | `boto3` (Bedrock) | One SDK, all models |
| Framework | LangChain + LangGraph | Multi-agent orchestration with state graph |

```
Research request
     ↓
Orchestrator (LangGraph state machine)
     ├─→ Researcher Agent (Gemini Flash — fast, broad search)
     │       ↓ sources + raw notes
     ├─→ Analyst Agent (Claude Sonnet — deep reasoning)
     │       ↓ structured analysis
     └─→ Writer Agent (Claude Sonnet — best writing)
             ↓
     Briefing document → human review
```

**Key architecture decisions:** State persistence between agents (if one fails, resume not restart), source citation enforcement, token budget per agent to control cost.

---

### Scenario 7: High-Volume Ticket Classification (Cost-Sensitive)
**Client says:** "We receive 50,000 support tickets a day. We want them auto-classified by category and priority before human agents see them."

| Layer | Choice | Reason |
|-------|--------|--------|
| Use Case Class | Class 3 — Classification | Pure routing, no generation |
| Model | Claude Haiku 4.5 or Gemini 2.0 Flash | Cheapest, fastest — classification needs no heavy reasoning |
| Gateway | None — direct API | Simple, high-volume, low-latency |
| SDK | `anthropic` or `google-genai` | Whichever model chosen |
| Framework | None | Single prompt per ticket, batch processing |
| Caching | System prompt cached | Classification schema stays constant = massive savings |

```
50,000 tickets/day
     ↓
Batch processor (async, parallel calls)
     ↓
Haiku / Flash: classify → { category, priority, sentiment }
     ↓
Write to ticket system → routed to correct queue
```

**Key architecture decisions:** Async batching to stay within rate limits, fallback to rule-based classification when API is down, confidence threshold (low confidence = human review queue).

---

## Phase 8 — Architecture Landscape for RFPs

> Every RFP technical response needs an architecture landscape — a view of all the components, who owns them, and how they connect.

### The Standard AI Architecture Layers

```
┌──────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                        │
│  Web UI / Mobile App / Slack Bot / API endpoint / CLI        │
│  Owner: Frontend team / Product team                         │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                        │
│  Agent loop / Workflow logic / Routing / Prompt builder      │
│  Framework: LangChain / LlamaIndex / ADK / CrewAI / Custom  │
│  Owner: AI engineering team                                  │
└──────┬──────────────────┬───────────────┬────────────────────┘
       ↓                  ↓               ↓
┌──────────────┐  ┌───────────────┐  ┌────────────────────────┐
│  TOOL LAYER  │  │ RETRIEVAL     │  │  MEMORY LAYER          │
│              │  │ LAYER         │  │                        │
│  APIs called │  │ Vector DB     │  │  Conversation history  │
│  DBs queried │  │ Document store│  │  User preferences      │
│  Code run    │  │ Embeddings    │  │  Session state         │
│  Emails sent │  │               │  │                        │
│  Owner: App  │  │ Owner: Data   │  │  Owner: App/AI team    │
│  team        │  │ team          │  │                        │
└──────┬───────┘  └───────┬───────┘  └───────────┬────────────┘
       └──────────────────┴──────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│                      MODEL LAYER                              │
│  Gateway (Bedrock / Vertex / Azure OpenAI) OR Direct API     │
│  Provider SDK (anthropic / google-genai / openai / boto3)    │
│  Model (Claude / Gemini / GPT / Llama)                       │
│  Owner: AI/Infra team                                        │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE LAYER                        │
│  Cloud: AWS / Azure / GCP / On-prem                          │
│  Compute, networking, IAM, VNet, logging, monitoring         │
│  Owner: Infrastructure / DevOps team                         │
└──────────────────────────────────────────────────────────────┘
```

---

### Key Architecture Decisions to Document in Every RFP

**1. Sync vs Async**

| Pattern | When to use | Example |
|---------|------------|---------|
| Synchronous | User waits for response, <5 seconds | Chat, classification, extraction |
| Asynchronous | Long-running tasks, batch | Report generation, research pipelines |
| Streaming | Real-time token output, feels faster | Chatbots, content generation |

**2. Human-in-the-Loop Placement**

```
Option A — Before action (approval gate):
  Agent proposes action → Human approves → Action executes
  Use when: irreversible actions (send email, delete record, make payment)

Option B — After output (review gate):
  LLM generates output → Human reviews → Published/sent
  Use when: content generation, reports, external communications

Option C — Exception only (confidence gate):
  LLM acts → Low confidence? → Escalate to human
  Use when: classification, extraction at scale

Option D — Full automation (no gate):
  LLM acts without human
  Use when: reversible, low-risk, internal only
```

**3. Where the Vector DB Lives**

| Client Cloud | Recommended Vector DB |
|-------------|----------------------|
| AWS | Amazon OpenSearch, pgvector on RDS |
| Azure | Azure AI Search, pgvector on Azure PostgreSQL |
| GCP | Vertex AI Vector Search, AlloyDB pgvector |
| On-prem / Cloud-agnostic | Chroma, Qdrant, Weaviate, pgvector (self-hosted) |

**4. Stateless vs Stateful**

| | Stateless | Stateful |
|---|-----------|---------|
| Each request is independent | ✅ | ❌ |
| Conversation history needed | ❌ | ✅ |
| Easier to scale horizontally | ✅ | ❌ |
| Needs session/memory store | ❌ | ✅ (Redis, DynamoDB, CosmosDB) |
| Use for | Classification, extraction, one-shot generation | Chatbots, agents with memory |

**5. Single Model vs Multi-Model**

| | Single Model | Multi-Model |
|---|-------------|------------|
| Simpler to build and debug | ✅ | ❌ |
| Cost-optimised per task | ❌ | ✅ (cheap model for simple tasks) |
| Vendor lock-in risk | Higher | Lower |
| Needs gateway or framework | Optional | Required |
| Use when | POC, simple use case, one provider preferred | Production at scale, different tasks need different strengths |

**6. Deployment Pattern**

| Pattern | What it means | Use when |
|---------|--------------|---------|
| Managed API (SaaS) | Call provider API directly, no infra to manage | Most cases — simplest |
| Managed platform | Bedrock / Vertex / Azure OpenAI — cloud manages the model endpoint | Enterprise, compliance, existing cloud spend |
| Self-hosted (cloud VM) | Run model on your own cloud VM (e.g., Ollama on EC2) | Need customisation, on-prem-like control in cloud |
| Fully on-premise | Run model on your own hardware | Air-gapped, regulated, data never leaves building |

---

### Architecture Landscape Template (for RFP Documents)

Use this as the skeleton for your architecture section in any RFP response:

```
[Client Name] — AI Solution Architecture

PRESENTATION
  [What the user sees and interacts with]

ORCHESTRATION
  [Framework + logic that coordinates everything]
  [Agent loop / workflow pattern / routing rules]

TOOLS & INTEGRATIONS
  [What external systems the AI can access or act on]
  [APIs, databases, email systems, etc.]

RETRIEVAL (if applicable)
  [Document store + vector DB + embedding model]

MEMORY (if applicable)
  [What is stored, where, for how long]

MODEL
  [Which model(s), via which gateway, using which SDK]
  [Primary model + fallback model if applicable]

INFRASTRUCTURE
  [Cloud provider, region, VNet, IAM, monitoring]

HUMAN-IN-THE-LOOP
  [Where humans review or approve, and what triggers escalation]

DATA FLOW
  [Step-by-step: input → processing → output → storage]

SECURITY & COMPLIANCE
  [PII handling, data residency, audit logging, access control]
```

---

[← AI SDKs Reference](REF-ai-sdks-and-apis.md) | [← Back to ROADMAP](../ROADMAP.md)
