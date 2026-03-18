# REF - Responsible AI & Governance

**Purpose:** Reference for governance, compliance, EU AI Act, responsible AI principles, data readiness, and what regulated clients require. Covers what RFP panels in regulated industries will ask.

---

## Why This Matters in RFPs

AI governance is no longer a "nice to have" — it is increasingly:
- **Legally mandated** (EU AI Act came into force August 2024, compliance deadlines phased to 2026)
- **Procurement required** (large enterprises and public sector require AI governance statements)
- **Reputationally critical** (a single AI incident can dominate news cycles)
- **Board-level concern** (AI risk now sits alongside cyber risk in most enterprise risk registers)

Panels will ask: *"What is your approach to responsible AI?"* You need a real answer, not a vague policy statement.

---

## Part 1 — EU AI Act

### What It Is

The EU AI Act is the world's first comprehensive AI regulation. It classifies AI systems by risk level and sets obligations accordingly. Applies to any AI system **used in the EU** — not just built there.

### Risk Classification Tiers

```
UNACCEPTABLE RISK — BANNED
─────────────────────────────────────────────────────────────
AI systems that are prohibited outright:
  • Social scoring by governments
  • Real-time biometric surveillance in public spaces (with narrow exceptions)
  • AI that exploits vulnerabilities to manipulate behaviour
  • Subliminal manipulation techniques

If a client asks you to build these: refuse. Full stop.

HIGH RISK — HEAVILY REGULATED
─────────────────────────────────────────────────────────────
AI in these domains requires conformity assessment, registration,
human oversight, and detailed documentation:

  Critical infrastructure:   Energy grids, water, transport
  Education:                 Exam scoring, student assessment
  Employment:                CV screening, performance monitoring, promotion decisions
  Essential services:        Credit scoring, insurance risk, social benefits
  Law enforcement:           Risk assessment for crime, evidence reliability
  Migration / border:        Asylum processing, visa decisions
  Justice:                   Legal interpretation assistance to courts

Obligations for high-risk AI:
  □ Risk management system documented
  □ Data governance (training data quality, bias testing)
  □ Technical documentation (architecture, training process)
  □ Logging / audit trail of every decision
  □ Human oversight mechanism
  □ Accuracy, robustness, cybersecurity measures
  □ Register in EU database (for public authority use)

LIMITED RISK — TRANSPARENCY REQUIRED
─────────────────────────────────────────────────────────────
AI systems that interact with humans must disclose they are AI:
  • Chatbots / conversational agents → must tell users they are AI
  • Deepfakes / synthetic content → must be labelled
  • Emotion recognition systems → must disclose

MINIMAL RISK — NO OBLIGATIONS
─────────────────────────────────────────────────────────────
Most business AI applications fall here:
  • Spam filters, AI in games, recommendation systems
  • Standard document summarisation, writing assistance
  • Most RAG Q&A, classification, content generation tools

Still good practice to apply responsible AI principles, but no legal obligation.
```

### Key Deadlines (phased implementation)

| Date | What Applies |
|------|-------------|
| Feb 2025 | Banned practices prohibited |
| Aug 2025 | GPAI (General Purpose AI) model obligations apply to providers |
| Aug 2026 | High-risk AI system obligations fully apply |
| Aug 2027 | High-risk AI in existing products must comply |

### What to Say in an RFP

> "We design all AI solutions in line with EU AI Act requirements. For the majority of business applications (content generation, Q&A, classification), these fall into the Minimal Risk category with transparency obligations — we disclose where AI is used. If your use case touches employment decisions, credit, or essential services, we conduct a formal risk classification and design accordingly, including human oversight, audit logging, and the required technical documentation."

---

## Part 2 — Responsible AI Principles

Most major providers and enterprise clients expect you to have a named framework. These six principles are the industry consensus (aligned with EU AI Act, OECD AI Principles, and major corporate frameworks):

### 1. Fairness
- AI must not discriminate based on protected characteristics (gender, race, age, disability, religion)
- Eval datasets must be representative of all user groups
- Monitor for disparate impact — does the system perform differently for different groups?

**In practice:**
```
  Eval dataset: ensure test cases cover diverse demographics, geographies, languages
  Monitoring: track model performance segmented by user group
  High-risk: formal bias audit before deployment (especially in hiring, credit, benefits)
```

### 2. Transparency
- Users should know when they are interacting with AI
- The system's purpose and limitations should be disclosed
- Decisions affecting people should be explainable

**In practice:**
```
  Chatbot disclosure: "I'm an AI assistant..." on first interaction
  Output sourcing: RAG systems should cite sources
  Decision explanation: "This recommendation is based on X, Y, Z factors"
  System card: document what the AI is, what it does, what it doesn't do
```

### 3. Accountability
- Clear ownership of AI decisions and outcomes
- Human oversight where the system affects people materially
- Audit trail for every consequential decision

**In practice:**
```
  Named AI owner within client organisation
  Human-in-the-loop for irreversible or high-stakes actions
  Audit log: who used the system, what query, what response, what action
  Incident reporting process
```

### 4. Privacy & Data Protection
- Minimum necessary data (don't collect more than needed)
- PII handled according to GDPR / applicable regulation
- Data subjects' rights respected (right to access, right to erasure)

**In practice:**
```
  PII redaction before LLM call
  No PII in logs (or anonymised)
  Data retention limits (90 days? 1 year? defined and enforced)
  DPIA (Data Protection Impact Assessment) for high-risk processing
```

### 5. Safety & Security
- System must not cause harm (physical, psychological, financial, reputational)
- Robust against adversarial inputs (prompt injection, jailbreaks)
- Fail safely when uncertain

**In practice:**
```
  Guardrails (input + output filtering)
  Prompt injection detection
  Confidence thresholds + human escalation
  Kill switch — disable immediately if harm detected
  Regular red-teaming (adversarial testing)
```

### 6. Human Oversight
- Humans must be able to understand, correct, and override AI decisions
- Especially critical where AI affects individuals' rights or material outcomes
- AI should augment humans, not replace human judgement on consequential matters

**In practice:**
```
  Human approval gates for irreversible actions
  Override mechanism — human can correct or reject AI output
  Monitoring dashboard — humans can see what AI is doing
  Regular review of AI decisions by domain expert
```

---

## Part 3 — Data Readiness for AI

Clients often underestimate how important data quality is. "AI-ready data" is a real concept.

### The Data Readiness Assessment

Before building, assess the client's data across five dimensions:

```
1. AVAILABILITY
   □ Does the data exist in a digital, accessible form?
   □ Is it in one place or scattered across systems?
   □ Who has permission to access it?
   Red flag: "It's in people's heads" / "It's on paper" / "We need to ask IT"

2. QUALITY
   □ Is it accurate and up to date?
   □ Is it consistently structured / formatted?
   □ Does it have gaps, errors, or conflicts?
   Red flag: Inconsistent naming, missing fields, outdated records, no owner

3. VOLUME
   □ Is there enough data to build a meaningful knowledge base (RAG)?
   □ Is there enough labelled data for fine-tuning (if needed)?
   □ For evals: can the client produce 100+ test cases with known correct answers?
   Red flag: "We have a few documents" when the use case needs thousands

4. SENSITIVITY
   □ Does it contain PII, financial data, health data, or IP?
   □ What regulations govern it?
   □ Can it be sent to a cloud LLM API, or must it stay on-premise?
   Red flag: GDPR-sensitive data heading to a US-hosted API without a DPA

5. FRESHNESS
   □ How often does this data change?
   □ Is there a process to keep the AI's knowledge current?
   □ Who owns the update cadence?
   Red flag: Policy documents updated monthly but no re-ingestion process planned
```

### Data Readiness Scoring (for discovery)

| Dimension | Score 1-3 | Impact if Low |
|-----------|----------|--------------|
| Availability | 1=scattered, 2=accessible, 3=API-ready | Adds weeks to ingestion build |
| Quality | 1=poor, 2=adequate, 3=clean | Low quality = high hallucination risk |
| Volume | 1=sparse, 2=sufficient, 3=rich | Too little = model can't answer confidently |
| Sensitivity | 1=highly regulated, 2=internal, 3=non-sensitive | Constrains model/gateway choice |
| Freshness | 1=static, 2=periodic, 3=real-time | Affects architecture complexity |

> If any dimension scores 1, flag it as a risk and include data remediation in the proposal scope.

### Common Data Problems and What They Mean for the Project

| Problem | AI Impact | Mitigation |
|---------|-----------|-----------|
| Documents in PDFs with scanned images | Can't be indexed without OCR | Add OCR pipeline to scope |
| Data in many inconsistent formats | Poor retrieval quality | Data normalisation sprint |
| No single source of truth | Conflicting AI answers | Data governance work before AI build |
| PII mixed into knowledge base | Can't send to cloud LLM | On-premise model OR PII scrubbing pipeline |
| Data owned by different teams | Access delays | Establish data access agreement upfront |
| Knowledge "in people's heads" | Can't be RAG'd | Knowledge capture workshop before build |

---

## Part 4 — AI Governance Framework for Clients

When a client asks "what governance do we need around this AI system?" — here's the structure:

### The Four Governance Pillars

```
1. POLICY
   ├── AI Use Policy: what the organisation will and won't use AI for
   ├── Acceptable Use Policy: rules for employees using AI tools
   └── AI Ethics Statement: public-facing principles

2. PROCESS
   ├── AI Risk Assessment: done before any new AI system goes live
   ├── Change Control: how model updates are managed
   ├── Incident Response: what to do when AI fails
   └── Human Review Cadence: regular review of AI outputs

3. PEOPLE
   ├── AI Owner: named accountable person per AI system
   ├── AI Ethics Board / Review Committee (for large orgs)
   ├── Training: all AI users understand limitations and responsible use
   └── Red Team: adversarial testing of AI systems

4. TECHNOLOGY
   ├── Audit Logging: every consequential AI decision logged
   ├── Monitoring: dashboards, alerts, quality metrics
   ├── Access Control: who can use what AI system
   └── Data Governance: how AI training/retrieval data is managed
```

### Minimum Viable Governance (for most clients)

For non-regulated clients building their first AI system:
```
  □ Named AI owner (person accountable for this system)
  □ AI acceptable use policy (what employees can/can't ask it)
  □ Chatbot disclosure (users know they're talking to AI)
  □ Audit log (every query and response stored for 90 days)
  □ Human review process (monthly sample of outputs reviewed)
  □ Incident response plan (what to do if it produces harmful output)
  □ Model update policy (how to handle provider model changes)
```

### Full Governance (for regulated clients or high-risk AI)

Everything above, plus:
```
  □ Formal AI risk classification (EU AI Act tier)
  □ DPIA (Data Protection Impact Assessment)
  □ Bias audit (pre-deployment and annually)
  □ Technical documentation (architecture, training, data provenance)
  □ EU AI Act registration (if high-risk and public authority use)
  □ External audit / third-party review
  □ Board-level AI risk reporting
```

---

## Part 5 — Provider Responsible AI Positions

Knowing where each provider stands helps in RFPs — especially regulated industry clients.

### Anthropic
- Founded on AI safety as core mission ("responsible development and maintenance of advanced AI")
- Constitutional AI (CAI): model trained with a set of principles, not just RLHF
- Usage policy prohibits: weapons of mass destruction, non-consensual content, undermining AI oversight
- No training on customer data via API (by default)
- **Strongest safety positioning** of major providers — good for regulated clients

### OpenAI
- Safety team + preparedness framework for catastrophic risk
- Usage policies enforced via moderation API
- No training on customer API data (Enterprise tier)
- SOC2 Type II, GDPR compliant
- ChatGPT Enterprise: no training on org data, SSO, admin controls

### Google (Gemini)
- AI Principles published since 2018 (after Project Maven controversy)
- Responsible AI practices include fairness, interpretability, privacy, security
- Vertex AI: enterprise governance controls, VPC, audit logging
- No training on customer data in enterprise tiers

### Meta (Llama — Open Source)
- Responsible Use Guide published with model releases
- Open weights: you control the model, but also the responsibility
- No provider-level safety net — safety is entirely your implementation
- **Important RFP point:** open-source = full control but full responsibility

---

## RFP Questions on This Topic

**"What is your approach to responsible AI?"**
> "We align with the six core responsible AI principles: fairness, transparency, accountability, privacy, safety, and human oversight. In practice, this means: every AI system we build includes guardrails, audit logging, human oversight design, and a named client AI owner. For regulated industries or high-risk use cases, we conduct a formal EU AI Act risk classification and design accordingly."

**"How do you comply with the EU AI Act?"**
> "Most business AI applications — document Q&A, content generation, classification — fall into the Minimal Risk category, which requires transparency (disclosing AI use) but no formal conformity assessment. If your use case involves employment decisions, credit, or essential services, it may be High Risk, requiring human oversight, audit logging, bias testing, and technical documentation. We assess the risk tier as part of discovery and design accordingly."

**"What happens when the AI is wrong and makes a consequential decision?"**
> "Our design principle is that AI does not make consequential decisions alone — it augments human judgement. For any output that affects people materially, we design human approval or review gates. Every decision is logged with the AI's output, the human's action, and the timestamp. If the AI produces a harmful output, our incident response plan defines severity levels, response times, and remediation steps."

**"Is our data safe with your AI system?"**
> "Data security is designed in from the start. For your specific requirements: [data never leaves X region / PII is redacted before reaching the model / all traffic is over private VNet / data retention is limited to N days / audit logs are available to your security team]. We sign a DPA (Data Processing Agreement) with you, and the model provider has signed a DPA covering their processing of the data."

**"How do you test for bias?"**
> "Our eval framework includes a representative test dataset that covers diverse user groups and scenarios. We track whether the model performs consistently across different user types, languages, and query styles. For high-risk systems affecting individuals, we conduct a formal bias audit before go-live and annually thereafter."

---

[← Back to Index](REF-INDEX.md) | [← Back to ROADMAP](../ROADMAP.md)
