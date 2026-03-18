# REF — Master Index of RFP Reference Documents

**Purpose:** Quick lookup — find which document covers which topic before a discovery meeting, proposal write, or client Q&A.

---

## The 8 Reference Documents

| # | Document | What It Covers |
|---|----------|---------------|
| 1 | [REF-ai-sdks-and-apis.md](REF-ai-sdks-and-apis.md) | SDK landscape, gateways, frameworks, stack map |
| 2 | [REF-solution-discovery-rfp.md](REF-solution-discovery-rfp.md) | Discovery questions, use case classification, architecture decisions |
| 3 | [REF-technical-proposal-rfp.md](REF-technical-proposal-rfp.md) | Stage 2 proposal structure, all 12 sections, review checklist |
| 4 | [REF-solution-design-document.md](REF-solution-design-document.md) | Stage 3 SDD — guardrails, evals, AI Ops, rollout, master Q&A list |
| 5 | [REF-cost-estimation.md](REF-cost-estimation.md) | Token pricing, provider costs, worked examples, cost optimisation |
| 6 | [REF-fine-tuning-vs-rag-vs-prompting.md](REF-fine-tuning-vs-rag-vs-prompting.md) | When to use each approach, how to recommend, RFP answers |
| 7 | [REF-build-vs-buy.md](REF-build-vs-buy.md) | Custom build vs Copilot vs SaaS vs platforms, cost comparison |
| 8 | [REF-responsible-ai-governance.md](REF-responsible-ai-governance.md) | EU AI Act, responsible AI principles, data readiness, governance |

---

## Topic Coverage Map

### Concepts & Engineering

| Topic | Document | Section |
|-------|----------|---------|
| What is an SDK / how it connects to models | REF-ai-sdks-and-apis | Provider SDK Map |
| Full stack map (app → framework → SDK → gateway → model) | REF-ai-sdks-and-apis | Full Stack Map |
| When to skip the framework or gateway layer | REF-ai-sdks-and-apis | When to skip each layer |
| OpenAI-compatible API standard | REF-ai-sdks-and-apis | OpenAI-Compatible API Standard |
| Google ADK — where it fits | REF-ai-sdks-and-apis | Provider-First Frameworks |
| RAG — how it works | REF-solution-discovery-rfp | Class 1 — Q&A / RAG |
| Agentic tool use — how it works | REF-solution-discovery-rfp | Class 6 — Agentic |
| Multi-agent architecture | REF-solution-discovery-rfp | Class 7 — Multi-Agent |
| Fine-tuning vs RAG vs prompting | REF-fine-tuning-vs-rag-vs-prompting | All sections |
| Token pricing mechanics | REF-cost-estimation | Part 1 — How LLM Pricing Works |
| Prompt caching — how it works | REF-cost-estimation | Part 1 — Cached Tokens |
| Guardrails — patterns and types | REF-solution-design-document | Section 3 — Guardrails Design |
| Evaluation frameworks — offline / online / human | REF-solution-design-document | Section 4 — Evaluation Framework |
| AI Ops — what to monitor | REF-solution-design-document | Section 5 — AI Ops & Monitoring |
| Drift detection | REF-solution-design-document | Section 5 — Drift Detection |
| Model versioning and update policy | REF-solution-design-document | Section 5 — Model Versioning |
| Human-in-the-loop design patterns | REF-solution-design-document | Section 8 — Architecture Decisions |
| Vector DB — where it lives by cloud | REF-solution-design-document | Section 8 — Architecture Decisions |
| Stateless vs stateful design | REF-solution-design-document | Section 8 — Architecture Decisions |

---

### Available Solutions & What to Recommend

| Topic | Document | Section |
|-------|----------|---------|
| Use case classification (7 classes) | REF-solution-discovery-rfp | Phase 2 — Use Case Classification |
| Architecture decision tree (which class to use) | REF-solution-discovery-rfp | Phase 3 — Architecture Decision Tree |
| Complete stack examples (7 real scenarios) | REF-solution-discovery-rfp | Phase 7 — Complete Stack Examples |
| Model selection by need | REF-solution-discovery-rfp | Phase 4 — Model Selection |
| Framework selection by situation | REF-solution-discovery-rfp | Phase 4 — Framework Selection |
| Infrastructure/gateway selection by client cloud | REF-solution-discovery-rfp | Phase 4 — Infrastructure Selection |
| Microsoft Copilot — what it does and doesn't do | REF-build-vs-buy | Microsoft Copilot for M365 |
| ChatGPT Enterprise — what it does and doesn't do | REF-build-vs-buy | ChatGPT Enterprise |
| Google Workspace AI — what it does and doesn't do | REF-build-vs-buy | Google Workspace AI |
| Copilot Studio — configure option | REF-build-vs-buy | Microsoft Copilot Studio |
| Salesforce Einstein / Agentforce | REF-build-vs-buy | Salesforce Einstein |
| When to recommend Build vs Buy vs Configure | REF-build-vs-buy | When to Recommend Each |
| When to recommend RAG | REF-fine-tuning-vs-rag-vs-prompting | RAG — When to Add It |
| When to recommend fine-tuning | REF-fine-tuning-vs-rag-vs-prompting | Fine-Tuning — When It's Actually Needed |
| Fine-tuning availability by provider | REF-fine-tuning-vs-rag-vs-prompting | Fine-tuning availability table |
| Decision matrix: client situation → stack | REF-ai-sdks-and-apis | Decision Matrix for RFP |

---

### Discovery & Proposal Process

| Topic | Document | Section |
|-------|----------|---------|
| Discovery questions (problem, data, users, risk, infra, budget) | REF-solution-discovery-rfp | Phase 1 — Discovery Questions |
| One-page discovery cheat sheet | REF-solution-discovery-rfp | One-Page Cheat Sheet |
| Stage 1 → 2 → 3 process map | REF-solution-design-document | Section 1 — Where This Fits |
| Executive summary structure | REF-technical-proposal-rfp | Section 1 — Executive Summary |
| Requirements → solution mapping | REF-technical-proposal-rfp | Section 2 — Understanding Requirements |
| Architecture section structure | REF-technical-proposal-rfp | Section 4 — Solution Architecture |
| Technology stack justification | REF-technical-proposal-rfp | Section 5 — Technology Stack |
| Alternatives considered format | REF-technical-proposal-rfp | Section 5 — Alternatives Considered |
| Security section structure | REF-technical-proposal-rfp | Section 6 — Security & Compliance |
| Guardrails in the proposal | REF-technical-proposal-rfp | Section 7 — Guardrails |
| Quality targets and UAT criteria | REF-technical-proposal-rfp | Section 8 — Evaluation & QA |
| Risk register format | REF-technical-proposal-rfp | Section 9 — Risk Register |
| Phasing (POC → Pilot → Production) | REF-technical-proposal-rfp | Section 9 — Phasing |
| Proposal review checklist | REF-technical-proposal-rfp | Proposal Review Checklist |

---

### Cost & Commercial

| Topic | Document | Section |
|-------|----------|---------|
| Provider pricing tables (Anthropic, Google, OpenAI) | REF-cost-estimation | Part 2 — Provider Pricing Reference |
| Gateway pricing (Bedrock, Azure, Vertex, Groq) | REF-cost-estimation | Part 3 — Gateway Pricing |
| Token estimation by use case class | REF-cost-estimation | Part 4 — Token Estimation by Use Case |
| Infrastructure costs (vector DB, cloud) | REF-cost-estimation | Part 5 — Infrastructure Costs |
| Full cost model template | REF-cost-estimation | Part 6 — Full Cost Model Template |
| Worked full example (7-step) | REF-cost-estimation | Part 7 — Worked Full Example |
| Cost optimisation strategies | REF-cost-estimation | Part 8 — Cost Optimisation Strategies |
| How to present cost in an RFP | REF-cost-estimation | Part 9 — How to Present Cost |
| Build vs Buy cost comparison at scale | REF-build-vs-buy | Cost Comparison at Scale |
| Pricing proposals (fixed / T&M / retainer) | REF-technical-proposal-rfp | Section 11 — Commercials |

---

### Security, Compliance & Governance

| Topic | Document | Section |
|-------|----------|---------|
| EU AI Act — risk tiers (banned / high / limited / minimal) | REF-responsible-ai-governance | Part 1 — EU AI Act |
| EU AI Act — compliance deadlines | REF-responsible-ai-governance | Key Deadlines |
| Responsible AI principles (6) | REF-responsible-ai-governance | Part 2 — Responsible AI Principles |
| Data readiness assessment (5 dimensions) | REF-responsible-ai-governance | Part 3 — Data Readiness |
| Data problems and their AI impact | REF-responsible-ai-governance | Common Data Problems |
| AI governance framework (policy / process / people / tech) | REF-responsible-ai-governance | Part 4 — AI Governance Framework |
| Minimum viable governance checklist | REF-responsible-ai-governance | Minimum Viable Governance |
| Provider responsible AI positions | REF-responsible-ai-governance | Part 5 — Provider Positions |
| Security controls (auth, encryption, PII, VNet) | REF-solution-design-document | Section 7 — Security |
| Security in the proposal | REF-technical-proposal-rfp | Section 6 — Security & Compliance |
| Compliance (GDPR, HIPAA, SOC2) | REF-technical-proposal-rfp | Section 6 — Compliance Alignment |
| Risk mapping by use case class | REF-solution-discovery-rfp | Phase 5 — Risk & Compliance |

---

### RFP Questions — Where to Find the Answer

| Question Panel Will Ask | Document | Section |
|------------------------|----------|---------|
| Should we fine-tune or use RAG? | REF-fine-tuning-vs-rag-vs-prompting | RFP Questions |
| Why not just use Microsoft Copilot? | REF-build-vs-buy | The "Why Not Just Use Copilot?" Answer |
| How do you comply with the EU AI Act? | REF-responsible-ai-governance | RFP Questions |
| What is your responsible AI approach? | REF-responsible-ai-governance | RFP Questions |
| How do you know when it stops working? | REF-solution-design-document | Master RFP Q&A List |
| How do you prevent hallucinations? | REF-solution-design-document | Section 3 — Guardrails |
| How do you handle PII? | REF-solution-design-document | Section 3 + Section 7 |
| What is your accuracy target? | REF-solution-design-document | Section 4 — Evaluation |
| Can you turn it off immediately? | REF-solution-design-document | Kill Switch Design |
| What happens if the model provider updates the model? | REF-solution-design-document | Model Versioning Policy |
| Where does our data go? | REF-technical-proposal-rfp | Section 6 — Security |
| Which model is best for our use case? | REF-ai-sdks-and-apis | Key RFP Talking Points |
| Why not lock into one provider? | REF-ai-sdks-and-apis | Key RFP Talking Points |
| What does the rollout look like? | REF-technical-proposal-rfp | Section 9 — Phasing |
| What happens when it fails? | REF-solution-design-document | Section 5 — Incident Response |
| Is this more expensive than buying off-the-shelf? | REF-build-vs-buy | Cost Comparison at Scale |

---

## Process Flow (When to Use Which Doc)

```
CLIENT ENQUIRY / RFP RECEIVED
          ↓
    [REF-solution-discovery-rfp]
    Run discovery, classify use case,
    draft architecture landscape
          ↓
    [REF-ai-sdks-and-apis]
    Decide stack: model → SDK → gateway → framework
          ↓
    [REF-build-vs-buy]
    Answer: should they build or use off-the-shelf?
          ↓
    [REF-fine-tuning-vs-rag-vs-prompting]
    Answer: RAG, fine-tune, or just prompting?
          ↓
    [REF-cost-estimation]
    Build cost model with assumptions
          ↓
    [REF-technical-proposal-rfp]
    Write the Stage 2 proposal (all 12 sections)
          ↓
    CONTRACT SIGNED
          ↓
    [REF-solution-design-document]
    Write the Stage 3 SDD (guardrails, evals, AI Ops)
          ↓
    [REF-responsible-ai-governance]
    Design governance, EU AI Act compliance, data readiness
```

---

[← Back to ROADMAP](../ROADMAP.md)
