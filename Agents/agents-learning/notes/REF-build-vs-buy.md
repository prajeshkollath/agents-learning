# REF - Build vs Buy vs Configure

**Purpose:** Answer the question every RFP panel asks — "Why not just use Microsoft Copilot / ChatGPT Enterprise / Google Workspace AI instead of building something custom?"

---

## The Three Options

```
BUY (SaaS)                  CONFIGURE (Platform)         BUILD (Custom)
──────────────              ────────────────────         ──────────────
Off-the-shelf AI            AI platform you              Custom application
product. Plug in,           configure and extend.        built specifically
subscribe, use.             Low-code / no-code.          for your use case.

Examples:                   Examples:                    Examples:
  Microsoft Copilot M365      Microsoft Copilot Studio     LangChain + Claude
  ChatGPT Enterprise          Google Agentspace            Custom agent system
  Google Workspace AI         ServiceNow AI                LlamaIndex RAG
  Notion AI                   Salesforce Einstein          Full custom stack
  Grammarly                   Power Platform AI
  GitHub Copilot

Speed: Days                 Speed: Weeks                 Speed: Months
Cost: Subscription/user     Cost: Platform + config      Cost: Build + maintain
Control: Low                Control: Medium              Control: Full
```

---

## Decision Framework

```
Is there an off-the-shelf product that does exactly what you need?
├── YES, and data security / compliance is acceptable → BUY
│
└── NO, or compliance is a blocker →
      Is the use case standard enough for a configurable platform?
      ├── YES → CONFIGURE (lower cost, faster than build)
      │
      └── NO, or platform can't meet requirements → BUILD
```

**Four factors that drive the decision:**

| Factor | Points toward BUY | Points toward BUILD |
|--------|------------------|---------------------|
| Use case uniqueness | Generic (writing, search) | Proprietary process |
| Data sensitivity | Public / low sensitivity | Confidential / regulated |
| Integration depth | Standalone tool | Deep system integration |
| Control needed | Behaviour is acceptable as-is | Must control every output |

---

## Major SaaS AI Products — What They Do and Don't Do

### Microsoft Copilot for Microsoft 365
**What it is:** AI assistant embedded across Word, Excel, Outlook, Teams, SharePoint.
**What it does well:**
- Drafting and summarising emails, documents, meeting notes
- Searching across M365 content (emails, files, Teams chats)
- Generating presentations, Excel formulas, meeting summaries

**What it doesn't do:**
- Connect to non-Microsoft systems (SAP, Salesforce, custom DBs) without connectors
- Execute multi-step agentic workflows reliably
- Give you control over prompts, model behaviour, or output format
- Provide usage analytics per-query or cost per-task visibility
- Custom guardrails beyond Microsoft's defaults

**Price:** ~$30/user/month (on top of M365 licence)
**Best for:** Productivity uplift for knowledge workers already on M365

---

### ChatGPT Enterprise (OpenAI)
**What it is:** GPT-4o with enterprise data privacy — no training on your data, SSO, admin controls.
**What it does well:**
- General-purpose AI assistant for any text task
- Code generation, analysis, writing, research
- Data privacy (no training on org data)
- Custom GPTs (configured assistants per department)

**What it doesn't do:**
- Connect to your internal systems without custom API work
- Agent workflows that take actions in your systems
- Guaranteed output format or structure
- Domain-specific quality without significant prompt work
- Source citation from your documents

**Price:** ~$30-60/user/month
**Best for:** General productivity, replacing ad-hoc ChatGPT usage, reducing shadow IT risk

---

### Google Workspace AI (Gemini for Workspace)
**What it is:** Gemini integrated into Gmail, Docs, Sheets, Meet, Drive.
**What it does well:**
- Writing assistance, email drafting, meeting summaries
- Search and synthesis across Google Drive content
- Deep Google ecosystem integration

**What it doesn't do:**
- Connect to non-Google systems without extra work
- Custom agent workflows
- Regulated industry compliance without additional configuration

**Price:** ~$20-30/user/month (on top of Workspace)
**Best for:** Organisations fully on Google Workspace

---

### Microsoft Copilot Studio
**What it is:** Low-code platform to build custom AI agents on Microsoft infrastructure.
**What it does well:**
- Build chatbots and agents without deep coding
- Connect to M365, Dynamics, Power Platform, custom APIs
- Deploy to Teams, web, or as a standalone app
- Governance within Microsoft ecosystem

**What it doesn't do:**
- Support non-Microsoft models natively
- Fine-grained control over model behaviour
- Complex multi-agent orchestration
- Non-M365 enterprise integrations without connectors

**Price:** ~$200/month + per-message costs (~$0.01/message)
**Best for:** M365-native organisations wanting chatbots without full dev team

---

### Salesforce Einstein / Agentforce
**What it is:** AI embedded in Salesforce CRM — predictions, recommendations, agent automation.
**What it does well:**
- AI within Salesforce data (leads, cases, opportunities)
- Pre-built sales and service AI actions
- Native CRM integration — no extra connectors needed

**What it doesn't do:**
- Work outside Salesforce context
- Give model-level control or customisation
- Connect to non-Salesforce systems without extra work

**Price:** Bundled or ~$50-75/user/month add-on
**Best for:** Clients whose primary system of record is Salesforce

---

### GitHub Copilot
**What it is:** AI code completion and generation within IDEs.
**What it does well:**
- Code completion, generation, explanation, review
- Integrated into VS Code, JetBrains, etc.
- Significant developer productivity gains

**What it doesn't do:**
- Anything outside of coding context
- Custom model behaviour or organisation-specific patterns without fine-tuning

**Price:** ~$10-19/user/month
**Best for:** Software development teams — almost always worth it

---

## Buy vs Build — Side-by-Side

| Dimension | Buy (SaaS) | Configure (Platform) | Build (Custom) |
|-----------|-----------|---------------------|---------------|
| **Time to value** | Days | Weeks | Months |
| **Upfront cost** | Low | Medium | High |
| **Ongoing cost** | Per-user subscription | Platform + usage | Maintenance + API |
| **Customisation** | Minimal | Moderate | Full |
| **Data control** | Provider's policy | Cloud platform policy | You control entirely |
| **Integration depth** | Shallow (works for them) | Medium (platform connectors) | Deep (any system) |
| **Model choice** | Fixed (their model) | Limited (platform's models) | Any model |
| **Guardrails control** | Provider's defaults | Limited | Full |
| **Eval / quality measure** | None / basic | Basic | Full custom eval framework |
| **Vendor dependency** | Very high | High | Low (if architected well) |
| **Scales with unique needs** | ❌ | ⚠️ | ✅ |
| **Scales with user volume** | ✅ (just add licences) | ✅ | Needs architecture work |

---

## When to Recommend Each

### Recommend BUY when:
- Use case is generic (writing assistance, email drafting, meeting summaries)
- Client is fully within one ecosystem (all M365, all Google)
- Speed to value is paramount (board demo in 2 weeks)
- Client has no dev capacity to build or maintain
- Data is not sensitive and provider's terms are acceptable
- Budget is per-user subscription (easier to justify politically)

### Recommend CONFIGURE when:
- Use case is specific but follows standard patterns (support chatbot, FAQ bot)
- Client wants to self-manage after delivery
- Client is on M365/Salesforce and wants native integration
- Moderate customisation is enough
- Client wants low-code extensibility without full dev dependency

### Recommend BUILD when:
- Use case is proprietary and unique to the client's business process
- Deep integration with internal systems is required (not just APIs — business logic integration)
- Client needs full control over model behaviour, guardrails, and evals
- Data is sensitive, regulated, or cannot leave a specific environment
- Client wants to own the IP and the system long-term
- The workflow is agentic (takes actions, not just generates text)
- Quality bar is high enough to need custom eval framework
- Cost at scale favours custom (subscriptions get expensive at 1,000+ users)

---

## The "Why Not Just Use Copilot?" Answer

This is the most common version of this question. Script for it:

> "Microsoft Copilot is excellent for general productivity — drafting emails, summarising meetings, searching your M365 content. It's the right choice if that's the problem.
>
> What you've described is different — you need AI that [connects to X system] / [takes actions in Y process] / [works with Z data that lives outside M365] / [produces output that meets this specific quality bar]. Copilot can't do that without significant custom development — at which point you're building anyway, just on Microsoft's platform with their constraints.
>
> What we're proposing gives you full control over model behaviour, custom guardrails, a measurable quality framework, and integrations with your actual systems — not just M365. The cost difference at [N] users over [N] years is [£X vs £Y]."

---

## Cost Comparison at Scale

**Example: 500 users, document Q&A use case, 3 years**

```
OPTION A — Microsoft Copilot M365
  Licence: £30/user/month × 500 users × 36 months = £540,000
  Works for: M365 document search only
  Custom integrations: Not possible

OPTION B — Copilot Studio (configure)
  Platform: £200/month + £0.01/message × ~150,000 msg/month = £1,700/month
  Build/config cost: £30,000 (one-time)
  3-year total: £30,000 + (£1,700 × 36) = £91,200
  Works for: M365 ecosystem, moderate customisation

OPTION C — Custom Build (RAG + Claude Sonnet)
  Build cost: £80,000 (one-time)
  API + infra: ~£4,500/month (500 users × ~50 queries/day)
  Maintenance: £12,000/year
  3-year total: £80,000 + (£4,500 × 36) + (£12,000 × 3) = £314,000
  Works for: Any system, full control, custom evals, any data

Note: Custom build more expensive here — but if use case is truly proprietary
or Copilot genuinely can't do it, cost comparison is irrelevant.
The real question is: can the off-the-shelf product solve the actual problem?
```

**The cost crossover:**
```
BUY wins at:   Generic use case, <500 users, already in ecosystem
BUILD wins at: Proprietary use case, >1,000 users, or when SaaS simply can't do it
CONFIGURE:     Usually the best value for medium complexity, platform-native clients
```

---

## Hybrid Approaches (Common in Enterprise)

Don't present it as binary. Many real solutions combine:

```
Example: Law firm
  BUY:        GitHub Copilot for dev team (coding assistance)
  BUY:        Copilot M365 for general staff (email, docs)
  BUILD:      Custom RAG system for contract analysis (proprietary data, high quality bar)

Example: Retailer
  BUY:        ChatGPT Enterprise for marketing team (content generation)
  CONFIGURE:  Copilot Studio for customer support chatbot (standard M365 deployment)
  BUILD:      Custom agentic system for supply chain decisions (proprietary logic)
```

This shows maturity — you're not just selling custom build, you're recommending the right tool for each problem.

---

## RFP Questions on This Topic

**"Why not use an off-the-shelf product?"**
> Lead with agreement: "For some parts of this, off-the-shelf is the right answer — we'd recommend [X] for [generic task]. For [specific use case], the off-the-shelf products fall short because [specific reason — integration, control, data, quality]. That's where custom build is justified."

**"Isn't building more expensive?"**
> "In year one, yes. At scale and over time, it depends. A £30/user/month subscription for 1,000 users is £360,000/year in perpetuity with no IP ownership. A custom build at £150,000 and £60,000/year in running costs breaks even in year two and you own the asset."

**"What if we just want to start with Copilot and build later?"**
> "That's a reasonable phasing approach. We'd suggest a 90-day Copilot pilot alongside a clear criteria for what 'not good enough' looks like — so the decision to build is evidence-based, not assumption-based."

---

[← Back to Index](REF-INDEX.md) | [← Back to ROADMAP](../ROADMAP.md)
