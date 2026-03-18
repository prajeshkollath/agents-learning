# REF - AI Cost Estimation for Client Proposals

**Purpose:** Reference for estimating and presenting API, gateway, and infrastructure costs in RFPs and solution proposals.

> ⚠️ **Prices change frequently.** All figures here are indicative for estimation purposes.
> Always verify against official provider pricing pages before submitting a proposal.
> - Anthropic: https://www.anthropic.com/pricing
> - Google: https://ai.google.dev/pricing
> - OpenAI: https://openai.com/api/pricing
> - AWS Bedrock: https://aws.amazon.com/bedrock/pricing
> - Azure OpenAI: https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service
> - Vertex AI: https://cloud.google.com/vertex-ai/pricing

---

## Part 1 — How LLM Pricing Works

### The Billing Unit: Tokens

Everything is priced in **tokens** — not words, not characters, not API calls.

```
What is a token?
  ~4 characters = 1 token
  ~0.75 words   = 1 token  (or ~1.33 tokens per word)

Quick conversions:
  1 word         ≈ 1.3 tokens
  1 sentence     ≈ 20 tokens
  1 paragraph    ≈ 80 tokens
  1 page (A4)    ≈ 500 tokens
  1,000 words    ≈ 1,300 tokens
  10-page report ≈ 5,000 tokens
  100-page doc   ≈ 50,000 tokens
```

### Two Types of Tokens — Both Billed Differently

```
INPUT TOKENS                        OUTPUT TOKENS
────────────                        ─────────────
Everything sent TO the model        Everything the model generates back

Includes:                           Includes:
  System prompt                       The model's response
  Conversation history                Structured JSON output
  Retrieved context (RAG)             Tool call parameters
  User message                        Chain-of-thought (if visible)
  Tool definitions

Priced lower (typically)            Priced higher (typically)
Ratio: ~3-5x cheaper than output    Ratio: ~3-5x more expensive than input
```

### Third Type: Cached Tokens (Where You Save Money)

```
CACHED INPUT TOKENS
───────────────────
Tokens the provider already processed and stored — you pay a fraction.

What can be cached:
  System prompts (stays same across all users)
  Document context (same docs retrieved repeatedly)
  Tool definitions (same tools in every call)

Savings: 80-90% reduction on cached token cost
Minimum cache size: 1,024 tokens (OpenAI) / 4,096 tokens (Gemini) / 1,024 tokens (Claude)
Cache duration: typically 5 minutes (Claude) to 1 hour (varies by provider)
```

---

## Part 2 — Provider Pricing Reference

> Prices in USD per 1 million tokens. Verify before use.

### Anthropic (Claude)

| Model | Input ($/1M) | Output ($/1M) | Cached Input ($/1M) | Context Window | Best For |
|-------|-------------|--------------|--------------------|----|---------|
| Claude Haiku 4.5 | ~$0.80 | ~$4.00 | ~$0.08 | 200K | High volume, simple tasks |
| Claude Sonnet 4.6 | ~$3.00 | ~$15.00 | ~$0.30 | 200K | Balanced quality/cost |
| Claude Opus 4.6 | ~$15.00 | ~$75.00 | ~$1.50 | 200K | Complex reasoning |

### Google (Gemini)

| Model | Input ($/1M) | Output ($/1M) | Cached Input ($/1M) | Context Window | Best For |
|-------|-------------|--------------|--------------------|----|---------|
| Gemini 2.0 Flash | ~$0.10 | ~$0.40 | ~$0.025 | 1M | High volume, cost-sensitive |
| Gemini 1.5 Flash | ~$0.075 | ~$0.30 | ~$0.019 | 1M | Very high volume |
| Gemini 1.5 Pro | ~$1.25 | ~$5.00 | ~$0.31 | 2M | Large documents |

### OpenAI (GPT)

| Model | Input ($/1M) | Output ($/1M) | Cached Input ($/1M) | Context Window | Best For |
|-------|-------------|--------------|--------------------|----|---------|
| GPT-4o mini | ~$0.15 | ~$0.60 | ~$0.075 | 128K | Cost-sensitive, general |
| GPT-4o | ~$2.50 | ~$10.00 | ~$1.25 | 128K | Balanced, strong coding |
| o1 | ~$15.00 | ~$60.00 | ~$7.50 | 128K | Deep reasoning tasks |
| o3 | ~$10.00 | ~$40.00 | ~$2.50 | 200K | Advanced reasoning |

### Model Tier Summary (Rule of Thumb)

```
CHEAPEST                                                    MOST EXPENSIVE
────────────────────────────────────────────────────────────────────────────
Gemini Flash  GPT-4o mini  Haiku  Gemini Pro  GPT-4o  Sonnet  Opus / o1 / o3
~$0.25/1M    ~$0.37/1M    ~$2.4  ~$3.1/1M   ~$6.25  ~$9/1M  ~$45-90/1M
(blended)    (blended)    /1M    (blended)   /1M     (blend) (blended)

Note: Blended = weighted average of input + output assuming ~70% input / 30% output split
```

---

## Part 3 — Gateway Pricing

Gateways add a layer over the provider — sometimes a markup, sometimes included in cloud spend.

### AWS Bedrock

| Model via Bedrock | Input ($/1M) | Output ($/1M) | vs Direct |
|-------------------|-------------|--------------|---------|
| Claude Sonnet 4.6 | ~$3.00 | ~$15.00 | Same as direct |
| Claude Haiku 4.5 | ~$0.80 | ~$4.00 | Same as direct |
| Llama 3.3 70B | ~$0.72 | ~$0.72 | No direct API |
| Mistral Large | ~$4.00 | ~$12.00 | Similar to direct |

> **Bedrock note:** Model prices are generally the same as direct API. Bedrock charges separately for provisioned throughput (if needed) and data transfer. Value is compliance + unified billing, not cheaper tokens.

### Azure OpenAI

| Model | Input ($/1M) | Output ($/1M) | vs Direct OpenAI |
|-------|-------------|--------------|----------------|
| GPT-4o | ~$2.50 | ~$10.00 | Same |
| GPT-4o mini | ~$0.15 | ~$0.60 | Same |
| o1 | ~$15.00 | ~$60.00 | Same |

> **Azure note:** Prices match OpenAI direct. Additional Azure costs: VNet private endpoint (~$0.01/hour), if using PTU (Provisioned Throughput Units) — separate pricing model for guaranteed throughput at scale.

### Google Vertex AI

| Model | Input ($/1M) | Output ($/1M) | vs Direct Gemini |
|-------|-------------|--------------|----------------|
| Gemini 2.0 Flash | ~$0.10 | ~$0.40 | Same |
| Gemini 1.5 Pro | ~$1.25 | ~$5.00 | Same |
| Claude Sonnet (via Vertex) | ~$3.00 | ~$15.00 | Same as Anthropic direct |

> **Vertex note:** Prices same as direct. Additional cost: Vertex AI endpoint hosting if using fine-tuned models. Google Cloud egress charges if data leaves GCP.

### Groq (Speed-First, Open Source Models)

| Model | Input ($/1M) | Output ($/1M) | Speed |
|-------|-------------|--------------|-------|
| Llama 3.3 70B | ~$0.59 | ~$0.79 | ~300 tokens/sec |
| Llama 3.1 8B | ~$0.05 | ~$0.08 | ~750 tokens/sec |
| Mixtral 8x7B | ~$0.24 | ~$0.24 | ~450 tokens/sec |

> **Groq note:** 10-50x faster than standard APIs. No proprietary models — open source only. Best for latency-critical apps where open source quality is acceptable.

---

## Part 4 — Token Estimation by Use Case

### Building Your Token Estimate

For each request, count what goes IN and what comes OUT:

```
INPUT = system prompt + conversation history + retrieved context + user message + tool defs
OUTPUT = model response + tool call params (if agentic)
```

### Estimation Guide by Use Case Class

---

**Class 1 — RAG / Q&A**

```
Typical request breakdown:
  System prompt:          500 tokens   (instructions, persona, format)
  Retrieved chunks:     2,000 tokens   (3-5 chunks × 400-500 tokens each)
  Conversation history:   500 tokens   (last 2-3 turns if stateful)
  User question:          100 tokens
  ─────────────────────────────────
  TOTAL INPUT:          3,100 tokens

  Model answer:           300 tokens   (typically concise for Q&A)
  ─────────────────────────────────
  TOTAL OUTPUT:           300 tokens

  TOTAL PER REQUEST:    3,400 tokens

Cache opportunity: system prompt (500 tokens) + tool defs if same across users
After caching:    ~500 cached + 2,600 uncached input + 300 output
```

**Worked example — RAG system, 1,000 queries/day:**
```
Input tokens/day:   2,600 × 1,000 = 2.6M uncached + 0.5M cached
Output tokens/day:    300 × 1,000 = 0.3M

Claude Sonnet 4.6:
  Uncached input:  2.6M × $3.00/1M  = $7.80/day
  Cached input:    0.5M × $0.30/1M  = $0.15/day
  Output:          0.3M × $15.00/1M = $4.50/day
  ──────────────────────────────────────────────
  Daily total:   $12.45  |  Monthly: ~$374  |  Annual: ~$4,544

Claude Haiku 4.5 (if quality acceptable):
  Daily total:   ~$1.60  |  Monthly: ~$48   |  Annual: ~$576
```

---

**Class 2 — Content Generation**

```
Typical request breakdown:
  System prompt:          800 tokens   (tone, format, company style guide)
  Input brief/data:     1,000 tokens   (the content they want turned into output)
  Examples (few-shot):  1,500 tokens   (optional but improves quality)
  User instruction:       200 tokens
  ─────────────────────────────────
  TOTAL INPUT:          3,500 tokens

  Generated content:    1,500 tokens   (report, proposal, email — longer output)
  ─────────────────────────────────
  TOTAL OUTPUT:         1,500 tokens

  TOTAL PER REQUEST:    5,000 tokens

Cache opportunity: system prompt + few-shot examples (2,300 tokens)
```

**Worked example — Proposal generation, 50 proposals/day:**
```
Claude Sonnet 4.6:
  Uncached input:  1.2M × $3.00/1M  = $3.60/day
  Cached input:    115K × $0.30/1M  = $0.03/day
  Output:          75K  × $15.00/1M = $1.13/day
  ──────────────────────────────────────────────
  Daily total:   $4.76  |  Monthly: ~$143  |  Annual: ~$1,737
```

---

**Class 3 — Classification / Routing**

```
Typical request breakdown:
  System prompt:          300 tokens   (categories, rules)
  Item to classify:       200 tokens   (email, ticket, query)
  ─────────────────────────────────
  TOTAL INPUT:            500 tokens

  Classification output:   20 tokens   (category + confidence)
  ─────────────────────────────────
  TOTAL OUTPUT:            20 tokens

  TOTAL PER REQUEST:      520 tokens

Cache opportunity: system prompt (300 tokens) — massive savings at volume
After caching:    200 uncached + 300 cached input + 20 output
```

**Worked example — 50,000 tickets/day (high volume):**
```
Claude Haiku 4.5:
  Uncached input:  10M  × $0.80/1M  = $8.00/day
  Cached input:    15M  × $0.08/1M  = $1.20/day
  Output:          1M   × $4.00/1M  = $4.00/day
  ──────────────────────────────────────────────
  Daily total:   $13.20  |  Monthly: ~$396  |  Annual: ~$4,818

Gemini 2.0 Flash (alternative):
  Daily total:   ~$1.80  |  Monthly: ~$54   |  Annual: ~$657
```

---

**Class 4 — Data Extraction**

```
Typical request breakdown:
  System prompt + schema:   600 tokens   (what fields to extract, output format)
  Document content:       3,000 tokens   (contract, invoice, form — varies hugely)
  ─────────────────────────────────
  TOTAL INPUT:            3,600 tokens

  Extracted JSON:           300 tokens   (structured field values)
  ─────────────────────────────────
  TOTAL OUTPUT:             300 tokens

  TOTAL PER REQUEST:      3,900 tokens

Note: Document size dominates — a 10-page contract = ~5,000 tokens alone
```

---

**Class 5 — Conversational Assistant (Stateful)**

```
Typical request breakdown (mid-conversation, turn 5):
  System prompt:            500 tokens
  Conversation history:   2,000 tokens   (grows with each turn — key cost driver)
  Retrieved context:      1,500 tokens   (if RAG-backed)
  Current user message:     150 tokens
  ─────────────────────────────────
  TOTAL INPUT:            4,150 tokens

  Model response:           400 tokens
  ─────────────────────────────────
  TOTAL OUTPUT:             400 tokens

  TOTAL PER REQUEST:      4,550 tokens

Key insight: cost per conversation GROWS with turns.
  Turn 1:  ~1,200 tokens input
  Turn 5:  ~3,500 tokens input
  Turn 10: ~6,000 tokens input

Mitigation: summarise history after N turns instead of keeping full log.
```

**Worked example — Support chatbot, 500 conversations/day, avg 6 turns:**
```
Avg tokens per turn: ~4,000 input + 400 output
Total turns/day: 500 × 6 = 3,000

Claude Sonnet 4.6:
  Input:   12M × $3.00/1M  = $36.00/day
  Output:  1.2M × $15.00/1M = $18.00/day
  ──────────────────────────────────────
  Daily total:   $54.00  |  Monthly: ~$1,620  |  Annual: ~$19,710

GPT-4o mini (alternative):
  Daily total:   ~$3.60  |  Monthly: ~$108   |  Annual: ~$1,314
```

---

**Class 6 — Agentic (Tool Use)**

```
Agentic calls are multi-step — each step is a separate API call.
Estimate number of steps first, then cost per step.

Typical 5-step agent task:
  Step 1 — Initial reasoning:  3,000 input + 200 output (decides first tool)
  Step 2 — After tool result:  3,200 input + 150 output (tool result fed back)
  Step 3 — After tool result:  3,350 input + 200 output
  Step 4 — After tool result:  3,550 input + 300 output
  Step 5 — Final response:     3,850 input + 500 output
  ─────────────────────────────────────────────────────
  TOTAL:  ~16,950 input tokens + 1,350 output tokens per task

  TOTAL PER AGENT TASK: ~18,300 tokens (vs ~3,400 for simple RAG query)
  Rule of thumb: agentic tasks cost 4-6x more than a simple query.

Tool definitions also add input tokens:
  Each tool definition: ~100-300 tokens
  10 tools defined: ~2,000 extra input tokens per call (cacheable)
```

**Worked example — Agentic reporting, 100 tasks/day:**
```
Claude Sonnet 4.6:
  Input:  1.7M × $3.00/1M  = $5.10/day
  Output: 135K × $15.00/1M = $2.03/day
  ───────────────────────────────────────
  Daily total:   $7.13  |  Monthly: ~$214  |  Annual: ~$2,603
```

---

## Part 5 — Infrastructure & Supporting Costs

These are separate from LLM API costs — often forgotten in proposals.

### Vector Database

| Service | Cost Model | Estimate |
|---------|-----------|---------|
| Amazon OpenSearch Serverless | Per OCU (compute unit) | ~$0.24/OCU-hour, min 2 OCUs = ~$345/month |
| pgvector on RDS | Per DB instance | t3.medium = ~$50/month |
| Pinecone (Starter) | Per pod | ~$70/month for 1M vectors |
| Chroma / Qdrant (self-hosted) | Your VM cost | ~$20-100/month depending on VM |
| Vertex AI Vector Search | Per node hour | ~$0.10/node-hour |

### Embedding Model (for RAG)

Converting documents to vectors — one-time cost when indexing, small ongoing cost for new docs.

| Service | Cost | Notes |
|---------|------|-------|
| Gemini Embedding | ~$0.025/1M tokens | Very cheap — good default choice |
| OpenAI text-embedding-3-small | ~$0.02/1M tokens | Cheap, strong quality |
| OpenAI text-embedding-3-large | ~$0.13/1M tokens | Higher quality |
| Cohere Embed | ~$0.10/1M tokens | Strong multilingual |
| Amazon Titan Embeddings (Bedrock) | ~$0.10/1M tokens | AWS-native |

**Example:** Index 10,000 pages of documents (5M tokens) with Gemini Embedding:
`5M × $0.025/1M = $0.13` — essentially free. Ongoing cost only for new documents.

### Cloud Infrastructure (Monthly Estimates)

| Component | AWS | Azure | GCP |
|-----------|-----|-------|-----|
| App hosting (Lambda/Functions) | ~$20-100 | ~$20-100 | ~$20-100 |
| API Gateway | ~$10-50 | ~$10-50 | ~$10-50 |
| Vector DB (managed) | ~$50-350 | ~$50-300 | ~$50-300 |
| Memory/cache (Redis) | ~$30-100 | ~$30-100 | ~$30-100 |
| Logging & monitoring | ~$20-80 | ~$20-80 | ~$20-80 |
| VNet / private endpoint | ~$10-30 | ~$10-30 | ~$10-30 |
| **Total infra (small-medium)** | **~$140-710** | **~$140-660** | **~$140-660** |

---

## Part 6 — Full Cost Model Template

Use this structure for every proposal:

```
COST CATEGORY              UNIT          VOLUME        UNIT COST    MONTHLY COST
─────────────────────────────────────────────────────────────────────────────────
LLM API — Input (uncached)  per 1M tokens  [X]M          $[Y]/1M      $[Z]
LLM API — Input (cached)    per 1M tokens  [X]M          $[Y]/1M      $[Z]
LLM API — Output            per 1M tokens  [X]M          $[Y]/1M      $[Z]
Embedding model             per 1M tokens  [X]M          $[Y]/1M      $[Z]
Vector database             per month      1             $[Y]         $[Z]
App hosting / compute       per month      1             $[Y]         $[Z]
Storage                     per GB/month   [X]GB         $[Y]/GB      $[Z]
Monitoring / logging        per month      1             $[Y]         $[Z]
─────────────────────────────────────────────────────────────────────────────────
TOTAL INFRASTRUCTURE + API                                           $[TOTAL]/month
─────────────────────────────────────────────────────────────────────────────────
```

---

## Part 7 — Worked Full Example (RFP-Ready)

**Client:** Mid-size law firm
**Use case:** Internal contract Q&A (Class 1 — RAG)
**Scale:** 200 users, ~50 queries/user/day = 10,000 queries/day
**Stack:** Claude Sonnet 4.6 via AWS Bedrock, Amazon OpenSearch, Lambda

### Step 1 — Token Estimate Per Query

```
System prompt (cached):         600 tokens
Retrieved chunks:             2,500 tokens   (5 chunks × 500 tokens)
User question:                  120 tokens
Model answer:                   350 tokens (output)
─────────────────────────────────────────
Input (uncached):             2,620 tokens
Input (cached):                 600 tokens
Output:                         350 tokens
```

### Step 2 — Daily Volume

```
10,000 queries/day
  Uncached input:  2,620  × 10,000 = 26.2M tokens/day
  Cached input:      600  × 10,000 =  6.0M tokens/day
  Output:            350  × 10,000 =  3.5M tokens/day
```

### Step 3 — Monthly Tokens

```
  Uncached input:  26.2M × 30 = 786M tokens/month  = 786 × $3.00/1M   = $2,358
  Cached input:     6.0M × 30 = 180M tokens/month  = 180 × $0.30/1M   =    $54
  Output:           3.5M × 30 = 105M tokens/month  = 105 × $15.00/1M  = $1,575
  ────────────────────────────────────────────────────────────────────────────
  LLM API monthly:                                                       $3,987
```

### Step 4 — Infrastructure Monthly

```
  Amazon OpenSearch Serverless (vector DB):                               $350
  AWS Lambda (app hosting):                                                $80
  API Gateway:                                                             $30
  CloudWatch (logging + monitoring):                                       $50
  S3 (document storage):                                                   $20
  ────────────────────────────────────────────────────────────────────────────
  Infrastructure monthly:                                                 $530
```

### Step 5 — Total Monthly Cost

```
  LLM API:          $3,987
  Infrastructure:     $530
  ──────────────────────────
  Total monthly:    $4,517    ← pass-through to client

  Per user/month:     $22.59  (200 users)
  Per query:          $0.45   (10,000 queries/day)
  Annual estimate:  ~$54,204
```

### Step 6 — Sensitivity Analysis (show this in proposals)

| Scenario | Queries/day | Monthly Cost | Per User/Month |
|----------|------------|-------------|---------------|
| Low (adoption 30%) | 3,000 | ~$1,505 | ~$7.50 |
| Mid (expected) | 10,000 | ~$4,517 | ~$22.59 |
| High (peak adoption) | 20,000 | ~$8,704 | ~$43.52 |

### Step 7 — Model Alternatives Comparison

| Model | Monthly (10K q/day) | Quality Trade-off |
|-------|--------------------|--------------------|
| Claude Haiku 4.5 | ~$680 | Acceptable for simple Q&A |
| Claude Sonnet 4.6 | ~$3,987 | **Recommended** — strong legal comprehension |
| Claude Opus 4.6 | ~$19,350 | Overkill for Q&A |
| GPT-4o | ~$3,410 | Similar quality, slightly cheaper |
| Gemini 2.0 Flash | ~$490 | Cheapest — validate quality on legal text |

---

## Part 8 — Cost Optimisation Strategies

Present these in proposals to show you've thought about cost control:

**1. Model tiering (biggest impact)**
```
Route queries to cheapest model that can handle them:
  Simple factual Q&A    → Haiku / Gemini Flash   (saves 75-90%)
  Complex reasoning     → Sonnet                 (balanced)
  Critical decisions    → Opus / o1              (use sparingly)

Implementation: classifier routes each query to right model tier
```

**2. Prompt caching**
```
Cache everything that stays the same across requests:
  System prompt, tool definitions, static context
  Savings: 80-90% on cached tokens
  Most effective when: system prompt >1,024 tokens, high query volume
```

**3. Context window management**
```
Conversation history grows indefinitely if not managed:
  After N turns, summarise history into ~200 tokens instead of keeping full log
  RAG: retrieve fewer, better chunks rather than many mediocre ones
  Output length: set max_tokens to prevent runaway output
```

**4. Batching (for async workloads)**
```
Batch API (Anthropic, OpenAI): 50% cost reduction on async batch jobs
  Suitable for: nightly report generation, bulk classification, document processing
  Not suitable for: real-time chat, latency-sensitive applications
```

**5. Embedding reuse**
```
Embed documents once — store in vector DB
  Never re-embed the same document
  Only re-embed when document content changes
  Embedding cost is typically <1% of total LLM cost anyway
```

---

## Part 9 — How to Present Cost in an RFP

**What to include:**

1. **Assumptions clearly stated** — if assumptions are wrong, estimates change
2. **Three scenarios** — low / expected / high usage
3. **Model alternatives** — show you considered cost vs. quality trade-offs
4. **Pass-through vs. your margin** — separate client-pays costs from your fees
5. **Cost controls** — what levers exist to reduce cost if needed
6. **Cost monitoring** — how the client will see and control spend

**Standard assumptions block (include in every proposal):**

```
COST ESTIMATION ASSUMPTIONS
────────────────────────────────────────────────────────────────
Users:                [N] active users
Queries per user/day: [N] (based on [source — interview / industry benchmark])
Working days/month:   22 days
Avg input tokens:     [N] per query (system prompt + context + message)
Avg output tokens:    [N] per query
Cache hit rate:       [N]% (system prompt cached)
Model:                [Model name and tier]
Growth factor:        [N]% monthly growth assumed

These estimates will be refined during Phase 1 (POC) based on actual usage data.
A cost monitoring dashboard will be delivered in Phase 2 so the client has
full visibility of spend and can adjust usage patterns accordingly.
────────────────────────────────────────────────────────────────
```

**Tip:** Never present a single number. Always present a range with assumptions. A single number looks made up; a range with assumptions looks rigorous.

---

[← Technical Proposal](REF-technical-proposal-rfp.md) | [← Solution Design](REF-solution-design-document.md) | [← Solution Discovery](REF-solution-discovery-rfp.md) | [← Back to ROADMAP](../ROADMAP.md)
