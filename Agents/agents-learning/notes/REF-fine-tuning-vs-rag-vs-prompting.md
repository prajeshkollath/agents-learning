# REF - Fine-Tuning vs RAG vs Prompting

**Purpose:** Answer the most common technical architecture question in AI RFPs — "Should we fine-tune a model on our data, use RAG, or just prompt engineer?"

---

## The Three Approaches — What They Are

```
PROMPTING                   RAG                          FINE-TUNING
─────────────               ──────────────               ────────────────
You craft instructions      You retrieve relevant        You retrain the model
to guide the model's        information and give         on your data so it
behaviour at query time.    it to the model              learns new behaviour.
                            at query time.

"Tell the model HOW         "Give the model WHAT         "Change WHAT the
to behave"                  it needs to know"            model knows/does"

No data changes model.      No data changes model.       Data changes the model.
Happens at runtime.         Happens at runtime.          Happens before deployment.
```

---

## Decision Tree — Which One to Use

```
Does the model already know enough about your domain?
├── YES → Prompting is enough. Start here. Always.
│
└── NO → What's missing?
          │
          ├── Missing FACTS / KNOWLEDGE (your docs, policies, products, data)
          │         → RAG
          │           The model doesn't need to memorise it —
          │           just retrieve and read it at query time.
          │
          ├── Missing BEHAVIOUR / STYLE (how it responds, tone, format, task type)
          │         → Fine-tuning
          │           You want the model to DO things differently,
          │           not just know more facts.
          │
          └── Missing BOTH?
                    → RAG first (for knowledge) + Prompting (for behaviour)
                    → Fine-tune only if RAG + prompting still falls short
```

**The golden rule:**
> Try prompting first. If that's not enough, add RAG. Fine-tune only as a last resort — it's expensive, slow, and locks you in.

---

## Detailed Comparison

| | Prompting | RAG | Fine-Tuning |
|---|-----------|-----|-------------|
| **What it changes** | How model behaves at runtime | What info the model sees | The model's weights (permanent) |
| **When it works** | Model already has relevant knowledge | Facts/docs are the gap | Behaviour/style/task-type is the gap |
| **Data required** | None | Your documents / knowledge base | Labelled training examples (hundreds to thousands) |
| **Cost to implement** | Negligible | Low-Medium (vector DB + ingestion) | High (compute + data prep + iteration) |
| **Time to implement** | Hours | Days-Weeks | Weeks-Months |
| **Keeps up with new data** | ✅ Instant (just update prompt) | ✅ Update vector DB | ❌ Must retrain |
| **Model stays up to date with provider updates** | ✅ Automatic | ✅ Automatic | ❌ Must re-fine-tune on new base model |
| **Explainability** | High (you see the prompt) | High (retrieved sources visible) | Low (why did it say that?) |
| **Risk of hallucination** | Same as base model | Lower (grounded in retrieved docs) | Can introduce new hallucinations |
| **Vendor lock-in** | Low | Low | High (fine-tuned weights tied to provider) |
| **Suitable for production** | ✅ | ✅ | ✅ (with caveats) |

---

## Prompting — When It's Enough

Prompting alone works when:
- The model already knows the domain (general business, coding, writing, analysis)
- You need to control format, tone, persona, or output structure
- The task is well-defined and consistent
- You want fast iteration and low cost

**What good prompting looks like:**
```
System prompt covers:
  Role:       "You are an expert contract analyst..."
  Task:       "Your job is to extract key terms from contracts..."
  Format:     "Always respond in JSON with these fields: {party, value, dates}"
  Constraints:"Only extract information explicitly stated. Never infer."
  Examples:   One or two example inputs and ideal outputs (few-shot)
```

**When prompting alone fails:**
- Model doesn't know your proprietary data (products, policies, clients)
- Model consistently gets domain-specific tasks wrong despite good prompts
- Context window fills up with examples needed to guide it

---

## RAG — When to Add It

RAG solves the **knowledge gap** — the model is capable but doesn't know your specific information.

**Use RAG when:**
- You have internal documents, policies, product specs, knowledge bases
- Data changes frequently (new products, updated policies, recent news)
- You need the model to cite its sources
- You want to control exactly what the model can and cannot reference
- Data is too large to fit in the context window

**What RAG does NOT fix:**
- Model that can't perform the task type (RAG gives knowledge, not capability)
- Behavioural issues like wrong tone or format (use prompting for that)
- The model consistently reasoning incorrectly (fine-tune for that)

**RAG architecture recap:**
```
Query → search vector DB → retrieve top N chunks
     → add chunks to prompt → model answers grounded in your docs
```

**Cost of RAG vs Fine-Tuning:**
```
RAG setup:       £5K-30K (vector DB, ingestion pipeline, retrieval tuning)
RAG ongoing:     £50-500/month (vector DB hosting + extra input tokens)

Fine-tuning:     £20K-100K+ (data prep, training compute, evaluation, iteration)
Fine-tuning ongoing: £500-5K/month (hosting fine-tuned endpoint, re-training cadence)
```

---

## Fine-Tuning — When It's Actually Needed

Fine-tuning changes **how the model behaves**, not just what it knows.

**Genuine use cases for fine-tuning:**
- You need a very specific output format the model consistently gets wrong despite prompting
- You're building a domain-specific task where the base model lacks the reasoning pattern (e.g., medical diagnosis reasoning, legal clause analysis)
- Latency: fine-tuned smaller model can match quality of larger base model at lower cost and faster speed
- You have thousands of labelled examples of the exact task you want the model to do
- The system prompt would need to be extremely long (>10,000 tokens) to capture all the rules — fine-tuning encodes those rules into weights

**Fine-tuning does NOT help when:**
- You just want the model to know your company's documents (use RAG)
- Your data changes frequently (model won't know about updates)
- You have fewer than a few hundred labelled examples
- You want the model to cite its sources (fine-tuning doesn't give sourcing)

**Types of fine-tuning:**
```
Full fine-tuning:     Retrain all weights. Expensive. Rarely needed.
LoRA / QLoRA:         Efficient fine-tuning. Most practical option.
                      Trains a small adapter layer, not the full model.
RLHF:                 Reinforcement learning from human feedback.
                      Used by providers (OpenAI, Anthropic) — rarely DIY.
Instruction tuning:   Train model to follow specific instruction formats.
```

**Fine-tuning availability by provider:**

| Provider | Fine-Tuning Available | Models | Cost |
|----------|----------------------|--------|------|
| OpenAI | ✅ Yes | GPT-4o mini, GPT-3.5 | Per token for training + hosting |
| Google | ✅ Yes | Gemini 1.5 Flash, Pro | Via Vertex AI |
| Anthropic | ❌ No (as of early 2026) | — | Not available via API |
| Together AI | ✅ Yes | Llama, Mistral | Training + hosting |
| AWS Bedrock | ✅ Yes (Continued Pre-Training) | Select models | Via Bedrock |

> **Important:** Claude cannot be fine-tuned via API. If fine-tuning is a hard requirement, this affects model choice.

---

## The Combination Approach

Real production systems often combine all three:

```
LAYER 1 — Prompting (always)
  System prompt defines role, format, constraints, reasoning style

LAYER 2 — RAG (when knowledge gap exists)
  Retrieved context gives the model your proprietary knowledge

LAYER 3 — Fine-tuning (when behaviour gap persists after layers 1+2)
  Model trained on your specific task patterns
```

**Example: Legal contract analysis tool**
```
Prompting:    "You are a legal analyst. Extract clauses in this JSON format.
               Flag any non-standard terms. Never infer — only extract."
RAG:          Retrieve relevant precedent cases + company contract standards
Fine-tuning:  [Optional] If model still mis-identifies clause types, fine-tune
              on 500 labelled contract examples showing correct clause classification
```

---

## How to Recommend in an RFP

**Default recommendation (covers 80% of cases):**
> "We recommend a RAG-based architecture with carefully engineered prompts. This gives the model access to your knowledge base without the cost, time, and lock-in of fine-tuning. Fine-tuning will be evaluated after Pilot if RAG + prompting does not meet the quality targets."

**When to recommend fine-tuning upfront:**
- Client has thousands of labelled examples of the specific task
- Latency is critical AND quality requirement is high (fine-tuned small model can beat large base model)
- Task is highly specialised and base model demonstrably fails after RAG + prompting

**When to push back on client requests to fine-tune:**
- "We want to fine-tune on our documents" → That's what RAG is for. Fine-tuning on documents doesn't give sourcing and goes stale.
- "We want the model to know our brand voice" → System prompt covers this. Not a fine-tuning use case.
- "Fine-tuning will make it more accurate" → Not necessarily. RAG + prompting often outperforms fine-tuning for knowledge tasks.

---

## RFP Questions on This Topic

**"Should we fine-tune a model on our data?"**
> "It depends on what's missing. If the model lacks knowledge of your documents and policies, RAG is the right approach — it's faster, cheaper, keeps data current, and cites sources. Fine-tuning is for behavioural gaps — when the model can't perform the task type correctly despite good prompting. We recommend starting with RAG + prompting, measuring quality in the Pilot, and fine-tuning only if a specific performance gap persists."

**"Why not fine-tune instead of RAG? Wouldn't it be more accurate?"**
> "Fine-tuning encodes a snapshot of your data into the model — it goes stale the moment your documents update, requires retraining to incorporate new information, and loses the ability to cite sources. RAG keeps knowledge current in real-time, provides source attribution, and costs a fraction of fine-tuning to implement and maintain."

**"Anthropic/OpenAI won't let us fine-tune — is that a problem?"**
> "For the majority of use cases, no. RAG + prompting achieves production-grade quality without fine-tuning. If fine-tuning is a hard requirement, we can use GPT-4o mini or Gemini 1.5 Flash (both support fine-tuning) or open-source models (Llama via Together AI) where you have full control."

---

[← Back to Index](REF-INDEX.md) | [← Back to ROADMAP](../ROADMAP.md)
