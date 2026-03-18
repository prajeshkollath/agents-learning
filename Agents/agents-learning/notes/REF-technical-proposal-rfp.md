# REF - Technical Proposal (RFP Response) — Stage 2

**Purpose:** Reference for writing the Technical Proposal submitted to clients after discovery and before contract. This is what the evaluation panel scores. Written to WIN.

---

## Where This Sits in the Process

```
Stage 1: Discovery Report       Stage 2: Technical Proposal      Stage 3: SDD
─────────────────────────       ───────────────────────────       ──────────────
Internal. Your team only.  →    Submitted to client.         →   Post-contract.
"Here's what we found."         "Here's what we'll build            "Here's how
                                 and why you should pick us."        we'll build it."

Audience: Your team             Audience: Eval panel                Audience: Eng team
Tone: Analytical                Tone: Confident, clear, visual      Tone: Technical
Length: 10-20 pages             Length: 20-40 pages                 Length: 30-60 pages
```

---

## Proposal Writing Principles

**Write for two readers simultaneously:**
- **Business sponsor** — reads executive summary, benefits, pricing, team. Skims the rest.
- **Technical evaluator** — reads architecture, stack justification, security, evals. Scores line by line.

**The three things that win RFPs:**
1. **Understanding** — show you understood their problem better than competitors
2. **Credibility** — show you've done this before and know what can go wrong
3. **Clarity** — the panel should never have to guess what you're proposing

**What loses RFPs:**
- Generic proposals that could be for any client
- Architecture diagrams with no explanation
- Vague timelines and effort estimates
- No mention of risk or what happens when things go wrong
- Walls of text with no visual structure

---

## Document Structure

### Cover Page
```
[Client Name] — [Project Name]
Technical Proposal

Submitted by: [Your Company]
Date: [Submission date]
Version: 1.0
Confidentiality: This document is confidential and intended for [Client Name] only.

Contact: [Name, email, phone]
```

---

### Table of Contents
Number every section. Evaluators score against sections — make it easy to navigate.

```
1. Executive Summary
2. Our Understanding of Your Requirements
3. Proposed Solution
4. Solution Architecture
5. Technology Stack & Justification
6. Security & Compliance
7. Guardrails & Responsible AI
8. Evaluation & Quality Assurance
9. Implementation Approach
10. Team & Credentials
11. Commercials
12. Appendix
```

---

## Section 1 — Executive Summary

**Purpose:** The business sponsor reads this. One page maximum. No jargon.

**Structure:**
```
Para 1 — THE PROBLEM (their words, not yours)
  Restate what they told you in discovery. This signals you listened.
  "You currently process X manually, which takes Y hours and costs Z.
   Errors in this process result in [consequence]."

Para 2 — OUR SOLUTION (what you're proposing)
  One clear sentence on what you're building.
  "We propose an AI-powered [solution name] that [does what],
   reducing [metric] by [X%] within [timeframe]."

Para 3 — WHY US (your differentiator)
  One reason you are the right partner.
  Not "we have great expertise" — be specific.
  "We have delivered three similar solutions for [industry] clients,
   including [named example if permitted]."

Para 4 — KEY OUTCOMES (measurable)
  3-4 bullet points. Numbers where possible.
  • Reduce manual processing time from X hours to Y minutes
  • Handle Z queries/day with <3 second response time
  • Accuracy target: >92% on [metric]
  • Go-live in [N] weeks from contract signature
```

**What evaluators score here:**
- Did they understand our problem?
- Is the solution clearly stated?
- Are the outcomes measurable and credible?

---

## Section 2 — Our Understanding of Your Requirements

**Purpose:** Prove you understood the brief. This section differentiates you from competitors who wrote a generic proposal.

**Structure:**

```
2.1 Business Context
    Why this project matters to the client's organisation.
    Reference anything they shared about strategic goals, pain points, pressures.

2.2 Current State (As-Is)
    How the process works today.
    Who does it, how long it takes, what tools they use.
    What goes wrong and what it costs when it does.

2.3 Requirements Summary
    Functional: what the system must do
    Non-functional: performance, scale, availability, security
    Constraints: cloud platform, compliance, budget, timeline

2.4 What Success Looks Like
    Restate their definition of success in their language.
    Then add your measurable version.
```

**Tip:** Use a table to show you've mapped requirements to your solution:

| Their Requirement | How Our Solution Addresses It |
|------------------|------------------------------|
| Process contracts 3x faster | Automated extraction reduces review time from 45 min to 12 min |
| Data must stay within EU | Deployed on Azure West Europe, no data leaves region |
| 99.5% availability | Managed Azure OpenAI SLA + failover design |

---

## Section 3 — Proposed Solution

**Purpose:** Describe WHAT you're building in plain language before the technical detail. Business and technical readers both read this section.

**Structure:**

```
3.1 Solution Overview
    One paragraph. What it is, what it does, who uses it.
    Include a simple "before / after" if it helps.

3.2 Use Case Classification
    State which class(es) this falls into (RAG, Agentic, Conversational, etc.)
    Explain why this classification led to this architecture.
    "Because this use case requires the AI to take actions in external systems,
     we have designed an agentic architecture with human approval gates..."

3.3 Key Capabilities
    Bullet list of what the solution can do.
    Written from the user's perspective, not the technology's.
    ✓ Answer questions from your policy documents in plain English
    ✓ Flag when it is unsure and escalate to a human
    ✓ Maintain conversation context across a session
    ✓ Log every interaction for audit purposes

3.4 What Is Out of Scope
    Explicitly state what you are NOT building.
    This prevents scope disputes and shows you thought it through.
```

---

## Section 4 — Solution Architecture

**Purpose:** The technical evaluator scores this section hardest. Must be clear, complete, and justified.

**4.1 Architecture Diagram**

Include the full stack diagram. Label every component. Every component must appear in the written explanation too.

```
Tips for good RFP architecture diagrams:
  - Use boxes and arrows, not text walls
  - Colour-code by layer (presentation / orchestration / model / infra)
  - Show data flow direction with arrows
  - Label every integration point
  - Include the human-in-the-loop touchpoint if applicable
  - Show where the guardrails layer sits
```

**4.2 Component Descriptions**

For every component in the diagram, one paragraph:
```
[Component Name]
What it is: [plain description]
Technology: [specific product/service]
Why we chose it: [justification — not just "it's good", be specific]
Owner: [which team manages this]
```

**4.3 Data Flow**

Step-by-step narrative of how data moves through the system:
```
1. User submits query via [interface]
2. Query passes through input guardrails (PII check, scope check)
3. Orchestration layer retrieves relevant documents from vector DB
4. Retrieved context + user query sent to [Model] via [Gateway]
5. Model response passes through output guardrails (grounding check, toxicity filter)
6. Response returned to user; interaction logged to [store]
```

**4.4 Integration Points**

Table of every external system connection:

| System | Integration Method | Auth | Data Direction | Owner |
|--------|------------------|------|---------------|-------|
| Client CRM | REST API | OAuth2 | Read (customer records) | Client IT |
| Email system | SMTP / Graph API | Service account | Write (send notifications) | Client IT |
| Document store | S3 / SharePoint API | IAM role | Read (policy documents) | Client IT |

**4.5 Scalability & Availability**

- Expected load (requests/day, concurrent users, peak times)
- How the system scales (horizontal, auto-scaling, rate limits)
- Availability target (99.5%? 99.9%?) and how it's achieved
- Single points of failure and how they're mitigated

---

## Section 5 — Technology Stack & Justification

**Purpose:** Show your stack is the right choice — not just what you know how to use.

**5.1 Stack Summary Table**

| Layer | Technology | Version/Tier | Reason |
|-------|-----------|-------------|--------|
| Model | Claude Sonnet 4.6 | Anthropic direct | Best reasoning quality, 200K context |
| Gateway | AWS Bedrock | — | Client is AWS-native, data residency |
| SDK | boto3 (Bedrock) | Latest | Single SDK for all models via Bedrock |
| Framework | LlamaIndex | 0.10.x | Purpose-built RAG, strong AWS integrations |
| Vector DB | Amazon OpenSearch | Serverless | AWS-managed, no infra overhead |
| Memory | Amazon DynamoDB | On-demand | Session state, serverless |
| Orchestration runtime | AWS Lambda | — | Serverless, scales to zero |
| Observability | Amazon CloudWatch + custom dashboard | — | Client already uses CloudWatch |

**5.2 Alternatives Considered**

Show you evaluated options — this builds credibility:

| Decision | Option Considered | Why Rejected |
|----------|------------------|-------------|
| Model | GPT-4o (Azure) | Client is AWS-native; Bedrock keeps all traffic in AWS |
| Framework | LangChain | LlamaIndex has stronger RAG primitives for this use case |
| Vector DB | Pinecone | Adds external dependency; OpenSearch keeps data in AWS |

**5.3 Model Selection Rationale**

Specific section justifying model choice — panels always ask about this:
```
Primary model: Claude Sonnet 4.6
  - 200K context window handles the client's longest contracts
  - Strongest comprehension benchmark scores on document Q&A tasks
  - Bedrock-hosted: no data leaves AWS

Fallback model: Claude Haiku 4.5
  - Used for classification and routing (10x cheaper, sufficient for this task)
  - Same provider, same gateway — no additional integration

Future consideration: If query volume exceeds 1M/day, evaluate
  Gemini 2.0 Flash for cost reduction with quality validation.
```

---

## Section 6 — Security & Compliance

**Purpose:** For regulated clients this section can be the deciding factor.

**6.1 Data Residency**
- Where data is stored (cloud region)
- What data leaves the client environment (if any)
- Provider's data processing agreements (DPA)

**6.2 Data Classification & Handling**

| Data Type | Where It Goes | Retention | Access Control |
|-----------|--------------|-----------|---------------|
| User queries | Logs (CloudWatch) | 90 days | Read: AI Ops team only |
| PII (redacted before LLM) | Never sent to model | — | — |
| LLM responses | Logs | 90 days | Read: AI Ops team only |
| Documents (source) | Client S3 (unchanged) | Client policy | IAM role, read-only |

**6.3 Security Controls**

| Control | Implementation |
|---------|---------------|
| Auth | SSO via client's existing IdP (SAML/OIDC) |
| Authorisation | RBAC — users only retrieve docs they have SharePoint access to |
| Encryption in transit | TLS 1.3 on all API calls |
| Encryption at rest | AES-256 on all stores |
| Audit logging | Every query logged: user ID, timestamp, query hash, response hash |
| PII handling | Regex + ML PII detector on input; scrubber on output |
| Network | All traffic via VPC; no public endpoints |
| Secrets management | AWS Secrets Manager for all API keys; rotated every 90 days |

**6.4 Compliance Alignment**
State which regulations apply and how the design addresses each:
```
GDPR:  Data residency in EU West; right to erasure implemented via log deletion API;
       DPA signed with Anthropic/AWS
SOC2:  AWS Bedrock is SOC2 Type II certified; audit logs available for auditors
HIPAA: [if applicable] BAA signed with AWS; PHI never sent to LLM; de-identified only
```

---

## Section 7 — Guardrails & Responsible AI

**Purpose:** Newer requirement in most enterprise RFPs. Shows you've thought about AI risk.

**7.1 Guardrails Summary**

| Risk | Guardrail | Where It Sits |
|------|-----------|--------------|
| PII in user queries | PII redaction (regex + ML classifier) | Input, before LLM |
| Off-topic queries | Scope restriction in system prompt + classifier | Input |
| Prompt injection | Injection pattern detector | Input |
| Hallucinated answers | Grounding check — answer must cite source | Output |
| Harmful content | Toxicity filter | Output |
| Low confidence | Confidence threshold → escalate to human | Output |

**7.2 Human-in-the-Loop Design**
Where humans are kept in the loop and why:
```
[Example for agentic system]
The agent will NOT execute the following actions without human approval:
  - Send any external communication (email, Slack)
  - Modify or delete any record in the CRM
  - Initiate any financial transaction

Approval workflow:
  Agent proposes action → UI shows proposed action + reasoning →
  Authorised user approves/rejects → Action executes (or is cancelled) →
  Both outcomes logged with user ID and timestamp
```

**7.3 Bias & Fairness Considerations**
- If system makes decisions affecting people: how bias is monitored and addressed
- Eval dataset diversity check (does it represent all user groups?)

---

## Section 8 — Evaluation & Quality Assurance

**Purpose:** Show you can prove the system works. Panels score this heavily.

**8.1 Quality Targets**

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Answer accuracy | >90% | Offline eval vs golden dataset |
| Groundedness | >95% answers cite source | LLM-as-judge on 10% live sample |
| Latency (p95) | <4 seconds | CloudWatch metrics |
| Escalation rate | <15% of queries | Dashboard metric |
| User satisfaction | >4.0/5.0 | In-app rating (optional thumbs up/down) |

**8.2 Eval Approach**
```
Pre-launch (Phase 1 & 2):
  - Golden dataset: 150 Q&A pairs built with client SMEs
  - Offline eval suite run on every deployment
  - Human review: 50 outputs reviewed by domain expert weekly

Post-launch (Phase 3):
  - Online eval: LLM-judge scores 10% of live traffic daily
  - Human review: 100 outputs monthly
  - Quarterly full regression against golden dataset
```

**8.3 Acceptance Testing**

Define exactly what "done" means before going live:
```
UAT criteria (all must pass before Phase 3 go-live):
  ✓ Offline eval score >90% on golden dataset
  ✓ Latency p95 <4s under simulated load (500 concurrent users)
  ✓ Zero P1 guardrail failures in 1-week UAT period
  ✓ Client SME sign-off on 50-output human eval sample
  ✓ Security penetration test passed
  ✓ Rollback tested and confirmed <15 min
```

---

## Section 9 — Implementation Approach

**Purpose:** Show you have a credible plan — not just ideas.

**9.1 Phasing**

```
Phase 1 — POC          Phase 2 — Pilot          Phase 3 — Production
──────────────         ───────────────           ────────────────────
[N] weeks              [N] weeks                 [N] weeks
Internal only          [X] pilot users           All users
Controlled dataset     Real data                 Full data
Manual eval            Formal eval suite         Continuous monitoring
Goal: prove it works   Goal: prove quality       Goal: full rollout
Deliverable:           Deliverable:              Deliverable:
 Working prototype      Eval report +             Production system +
 + demo                 go/no-go decision         AI Ops runbook
```

**9.2 Milestone Table**

| Week | Milestone | Deliverable | Sign-off Required |
|------|-----------|-------------|------------------|
| 2 | Infrastructure provisioned | Cloud environment ready | Infra lead |
| 4 | RAG pipeline working | Demo on client documents | Client sponsor |
| 6 | Guardrails integrated | Security review passed | Security team |
| 8 | Eval suite in place | Eval report (Phase 1) | Client sponsor |
| 10 | Pilot launch | 20 users onboarded | Client sponsor |
| 14 | Pilot eval complete | Go/no-go report | Steering committee |
| 16 | Production go-live | All users, AI Ops active | Client exec |

**9.3 Dependencies & Assumptions**

Things you need from the client to hit the timeline:
```
We assume the following will be provided within [N] weeks of contract start:
  □ API access to [CRM / document store / email system]
  □ Sample dataset of [N] documents for initial RAG build
  □ Access to [N] SMEs for eval dataset creation (4 hours total)
  □ Cloud environment provisioned with [permissions]
  □ Named project contact with authority to make decisions

Timeline is at risk if these are delayed.
```

**9.4 Risk Register**

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Document quality poor (inconsistent, unstructured) | Medium | High | Discovery doc quality review in Week 1; remediation plan if needed |
| Accuracy target not met in Pilot | Medium | High | Model tuning + prompt refinement sprint; acceptance criteria clearly defined |
| Client IT delays API access | High | Medium | Begin with synthetic data; parallel-track integration |
| Provider model update changes behaviour | Low | Medium | Shadow mode testing on all model updates; regression suite |
| Scope expansion during Pilot | High | Medium | Change control process defined upfront; out of scope list in contract |

---

## Section 10 — Team & Credentials

**Purpose:** The panel is evaluating the people, not just the proposal.

**10.1 Team Structure**

| Role | Name | Responsibility |
|------|------|---------------|
| Project Lead | [Name] | Client relationship, delivery oversight |
| AI Lead | [Name] | Architecture, model selection, eval design |
| AI Engineer | [Name] | Agent/RAG build, framework implementation |
| Backend Engineer | [Name] | Integrations, APIs, infrastructure |
| Data Engineer | [Name] | Vector DB, ingestion pipeline |
| DevOps / AI Ops | [Name] | Cloud, monitoring, CI/CD |

**10.2 Relevant Experience**

For each team member or as a company:
```
[Project name or type] — [Year]
  Client: [industry, anonymised if needed]
  What we built: [1-2 sentences]
  Use case class: [RAG / Agentic / etc.]
  Scale: [users, requests/day]
  Outcome: [measurable result]
```

**10.3 Certifications & Partnerships**
- Cloud partner tiers (AWS Advanced Partner, Google Cloud Partner, etc.)
- Relevant certifications (AWS ML Specialty, Google Professional ML Engineer, etc.)
- AI provider relationships (Anthropic partner, etc.)

---

## Section 11 — Commercials

**Purpose:** Pricing, payment terms, commercial structure.

**11.1 Pricing Structure**

```
Option A — Fixed Price
  Phase 1 (POC):        £X
  Phase 2 (Pilot):      £X
  Phase 3 (Production): £X
  Total:                £X
  Best for: well-defined scope, client prefers certainty

Option B — Time & Materials
  AI Lead:        £X/day × estimated Y days
  AI Engineer:    £X/day × estimated Y days
  [etc.]
  Estimated total: £X (±20%)
  Best for: exploratory scope, likely to change

Option C — Retainer (AI Ops ongoing)
  Monthly: £X for [N] hours AI Ops + monitoring + model management
  Best for: post-launch ongoing support
```

**11.2 Pass-Through Costs (API / Cloud)**

Separate from your fees — client pays these directly or via you:
```
LLM API costs (estimated):
  [Model] at [price/1M tokens] × estimated [X]M tokens/month = £X/month

Cloud infrastructure:
  [Service] = estimated £X/month

These are estimates based on [N] users / [N] queries/day.
Actual costs depend on usage — we recommend a cost monitoring dashboard.
```

**11.3 Payment Terms**
```
Suggested milestone-based:
  25% on contract signature
  25% on Phase 1 completion (POC demo sign-off)
  25% on Phase 2 completion (go/no-go sign-off)
  25% on Phase 3 go-live
```

---

## Section 12 — Appendix

Include supporting material that would interrupt the main flow:
- Full architecture diagram (large format)
- Detailed data flow diagrams
- Security controls checklist
- CVs / bios of key team members
- Case studies
- Provider certifications
- Glossary of terms

---

## Proposal Review Checklist

Before submitting, check every item:

**Content:**
- [ ] Executive summary is one page and jargon-free
- [ ] Problem statement uses client's own language
- [ ] All requirements from the RFP brief are addressed (map each one)
- [ ] Out of scope is explicitly stated
- [ ] Success metrics are specific and measurable
- [ ] Architecture diagram labels every component
- [ ] Every component in diagram is explained in text
- [ ] Technology choices have documented justification
- [ ] Alternatives considered and rejected are listed
- [ ] Guardrails design is present
- [ ] Eval approach and quality targets are defined
- [ ] Acceptance criteria are clear
- [ ] Risk register is honest (don't hide risks — show mitigations)
- [ ] Dependencies and assumptions are explicit
- [ ] Team members are named with relevant experience

**Presentation:**
- [ ] Consistent formatting throughout
- [ ] Table of contents with page numbers
- [ ] Every section numbered (evaluators score by section)
- [ ] Diagrams are readable (not too small)
- [ ] No spelling or grammar errors
- [ ] Client name spelled correctly throughout (common mistake)
- [ ] Version number and date on cover page
- [ ] Confidentiality notice on cover page

**Commercial:**
- [ ] All phases priced
- [ ] Pass-through costs separated from your fees
- [ ] Payment milestones tied to deliverables
- [ ] Assumptions that affect price are stated

---

[← Solution Design Document](REF-solution-design-document.md) | [← Solution Discovery](REF-solution-discovery-rfp.md) | [← AI SDKs Reference](REF-ai-sdks-and-apis.md) | [← Back to ROADMAP](../ROADMAP.md)
