# REF - AI SDKs, APIs, and Compatibility

**Purpose:** Reference for RFP preparations, solution discovery, and architecture decisions.

---

## The Core Rule

> **Each SDK is tied to one provider. The provider hosts the models. You pick the SDK based on which model you're building with.**

```
You write code
    ↓
SDK (library)
    ↓
Provider's API endpoint
    ↓
Model (LLM)
```

---

## Full Stack Map (Where Everything Sits)

```
┌─────────────────────────────────────────────────────────────────┐
│                        YOUR APPLICATION                         │
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                    FRAMEWORK LAYER (optional)                    │
│                                                                  │
│  Provider-agnostic          │  Provider-first                   │
│  ─────────────────          │  ─────────────                    │
│  LangChain                  │  Google ADK  ← (Gemini-first,     │
│  LlamaIndex                 │                Vertex-integrated) │
│  CrewAI                     │                                   │
│  AutoGen                    │                                   │
│  DSPy                       │                                   │
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                     PROVIDER SDK LAYER                           │
│                                                                  │
│  anthropic        google-genai       openai       mistralai     │
│  (Claude only)    (Gemini only)      (GPT only)   (Mistral only)│
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│               GATEWAY / AGGREGATOR LAYER (optional)              │
│                                                                  │
│  AWS Bedrock    Azure OpenAI    Vertex AI    Groq    Together AI │
│  (multi-model)  (OpenAI models) (multi-model)(fast)  (OSS models│
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                          MODEL LAYER                             │
│                                                                  │
│  Claude    Gemini    GPT-4o    Llama    Mistral    Cohere        │
└─────────────────────────────────────────────────────────────────┘
```

**Reading the map:**
- You always start at the top and go down
- Google ADK sits in the Framework layer but has a tighter coupling to Vertex AI/Gemini than other frameworks
- Gateways let you access multiple models through one entry point (multi-model row at the bottom)

**When to skip each layer:**

| Layer | Skip when | Use when |
|-------|-----------|----------|
| **Framework** | Learning internals (Phase 4), simple single-purpose app, full custom control needed | Building agents, multi-step workflows, any real product — frameworks handle the agent loop, tools, memory so you don't reinvent the wheel |
| **Gateway** | Single provider, talking directly to one API is sufficient | Multi-model requirement, client is AWS/Azure/GCP-native, compliance or data residency needed |

> "Optional" means technically skippable — not that you should skip them. For anything agent-like, use a framework. For multi-cloud or enterprise compliance, use a gateway.

---

## Provider SDK Map

| Provider | SDK / Library | Language Support | Models Available |
|----------|--------------|-----------------|-----------------|
| **Anthropic** | `anthropic` | Python, Node.js | Claude Opus 4.6, Sonnet 4.6, Haiku 4.5 |
| **Google** | `google-genai` | Python, Node.js | Gemini 2.0 Flash, Gemini 1.5 Pro, Gemini 1.5 Flash |
| **OpenAI** | `openai` | Python, Node.js | GPT-4o, GPT-4o mini, o1, o3 |
| **Meta (Llama)** | No official SDK — use via gateways | — | Llama 3, Llama 3.1, Llama 3.3 |
| **Mistral** | `mistralai` | Python, Node.js | Mistral Large, Mistral Small, Codestral |
| **Cohere** | `cohere` | Python, Node.js | Command R+, Command R |

---

## Gateway / Aggregator Services

These let you access **multiple providers through one SDK or endpoint** — important for enterprise RFPs where you want model flexibility without rewriting code.

### AWS Bedrock
- **What:** AWS-hosted AI gateway
- **SDK:** `boto3` (AWS Python SDK) or `amazon-bedrock-runtime`
- **Models available:** Claude (Anthropic), Llama (Meta), Mistral, Titan (Amazon), Cohere
- **Why use in RFP:** Client is AWS-native, wants single cloud bill, needs data residency in AWS
- **Key selling point:** Your data never leaves AWS infrastructure

### Azure OpenAI Service
- **What:** Microsoft-hosted OpenAI models + some others
- **SDK:** `openai` SDK (same as OpenAI, just point to Azure endpoint)
- **Models available:** GPT-4o, GPT-4o mini, o1, Whisper, DALL-E
- **Why use in RFP:** Client is Microsoft/Azure shop, existing Azure spend, enterprise compliance
- **Key selling point:** OpenAI models with Azure compliance, RBAC, VNet support

### Google Vertex AI
- **What:** Google Cloud-hosted AI gateway
- **SDK:** `google-cloud-aiplatform` (different from `google-genai`)
- **Models available:** Gemini (all versions), Claude (via Anthropic on Vertex), Llama, open-source models
- **Why use in RFP:** Client is GCP-native, needs managed MLOps alongside LLM
- **Key selling point:** Full ML pipeline (train → deploy → monitor) in one place

### Groq
- **What:** Inference-only provider (no training), extreme speed
- **SDK:** `groq` OR `openai` SDK (Groq is OpenAI-compatible)
- **Models available:** Llama 3.3, Mistral, Gemma (open-source models only)
- **Why use in RFP:** Latency-critical applications, real-time voice, streaming
- **Key selling point:** 10-50x faster inference than standard APIs

### Together AI / Fireworks AI
- **What:** Open-source model hosting
- **SDK:** `openai` SDK (both are OpenAI-compatible)
- **Models available:** Llama, Mistral, Mixtral, many fine-tuned variants
- **Why use in RFP:** Client wants open-source, fine-tuning control, cost reduction
- **Key selling point:** Run fine-tuned models without managing infrastructure

---

## The OpenAI-Compatible API Standard

Many providers implement the **same API format as OpenAI** — this is intentional, so you can reuse the OpenAI SDK by just changing the `base_url`.

```python
# Standard OpenAI
from openai import OpenAI
client = OpenAI(api_key="sk-...")

# Groq (OpenAI-compatible)
client = OpenAI(api_key="gsk_...", base_url="https://api.groq.com/openai/v1")

# Together AI (OpenAI-compatible)
client = OpenAI(api_key="...", base_url="https://api.together.xyz/v1")

# Azure OpenAI (OpenAI-compatible)
client = AzureOpenAI(azure_endpoint="https://your-resource.openai.azure.com/", ...)

# Ollama local models (OpenAI-compatible)
client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
```

**RFP implication:** If a solution uses OpenAI SDK with `base_url` abstracted, you can swap underlying model provider without rewriting application code. This is a genuine architectural flexibility argument.

---

## Framework Abstraction (One Step Higher)

Frameworks sit above SDKs and let you swap providers with a config change.

### Provider-Agnostic Frameworks

| Framework | What It Abstracts | Providers Supported |
|-----------|------------------|-------------------|
| **LangChain** | Everything (tools, memory, chains, retrieval) | All major providers |
| **LlamaIndex** | Primarily RAG/retrieval pipelines | All major providers |
| **CrewAI** | Multi-agent orchestration | All major providers |
| **AutoGen** | Multi-agent conversation | OpenAI, Azure, Groq, Ollama |
| **DSPy** | Prompt optimization pipelines | Most providers |

### Provider-First Frameworks

| Framework | Built By | Primary Model | Other Models | Tight Integration With |
|-----------|----------|--------------|-------------|----------------------|
| **Google ADK** | Google | Gemini (via `google-genai`) | Others via LiteLLM | Vertex AI, Google Cloud |

**Google ADK — Where It Fits:**

```
Your Code
    ↓
Google ADK          ← Framework layer (agent loops, tools, multi-agent, memory)
    ↓
google-genai SDK    ← Provider SDK layer (raw Gemini API calls)
    ↓
Gemini API
    ↓
Gemini models
```

**What ADK gives you over raw `google-genai` SDK:**
- Built-in agent loop (observe → think → act → repeat) — you don't write this yourself
- Tool registration and execution handling
- Multi-agent orchestration (coordinator + sub-agents)
- Session and memory management
- Vertex AI deployment out of the box

**ADK vs LangChain — the key difference:**

| | Google ADK | LangChain |
|---|---|---|
| **Provider coupling** | Gemini-first, Google ecosystem | Truly provider-agnostic |
| **Deployment** | Optimised for Vertex AI | Any cloud or on-prem |
| **Model swap** | Possible via LiteLLM, but not primary use case | First-class feature |
| **GCP integration** | Native (Cloud Storage, BigQuery, etc.) | Needs extra connectors |
| **RFP fit** | Client is GCP-native | Client needs flexibility / multi-cloud |

```python
# LangChain — swap provider by changing one line
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Application code is identical regardless of which you use
llm = ChatAnthropic(model="claude-sonnet-4-6")   # or
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")  # or
llm = ChatOpenAI(model="gpt-4o")
```

---

## Decision Matrix for RFP / Solution Discovery

| Client Situation | Recommended Approach | SDK / Gateway |
|-----------------|---------------------|---------------|
| AWS-native, strict data residency | Bedrock | `boto3` / Bedrock SDK |
| Azure enterprise, M365 integration | Azure OpenAI | `openai` SDK → Azure endpoint |
| GCP-native, needs MLOps | Vertex AI | `google-cloud-aiplatform` |
| Best reasoning / coding quality | Anthropic directly | `anthropic` SDK |
| Cost-sensitive, open-source OK | Groq + Llama / Together AI | `openai` SDK (compatible) |
| Need model flexibility long-term | Framework abstraction (LangChain) | Provider-agnostic |
| On-premise, no cloud | Ollama (local) | `openai` SDK (compatible) |
| Regulated industry (finance, health) | Azure OpenAI or Bedrock | Compliance-certified gateways |

---

## Key RFP Talking Points

**"Why not lock into one provider?"**
- Model capabilities shift fast — GPT-4o, Claude, Gemini leapfrog each other every few months
- Abstraction layer (framework or OpenAI-compatible) protects investment
- Price competition: same model on Groq vs OpenAI can differ 10x

**"Which model is best?"**
- For coding/reasoning: Claude Opus / Sonnet 4.6, GPT-4o, o1/o3
- For speed/cost: Gemini 2.0 Flash, GPT-4o mini, Haiku 4.5
- For document processing (large context): Gemini 1.5 Pro (1M tokens), Claude (200K)
- For open-source/self-hosted: Llama 3.3 70B via Groq or Ollama

**"What's the build cost difference?"**
- Anthropic/OpenAI direct: fastest to prototype, higher per-token cost
- Bedrock/Vertex: adds IAM complexity, but enterprise SLAs and compliance built-in
- Framework overhead: ~1-2 weeks initial setup, pays off at scale or multi-model

---

## Quick Reference: Context Window Sizes (as of early 2026)

| Model | Context Window | Notes |
|-------|---------------|-------|
| Claude Sonnet 4.6 | 200K tokens | ~150K words |
| Claude Opus 4.6 | 200K tokens | Best for complex reasoning |
| GPT-4o | 128K tokens | |
| Gemini 2.0 Flash | 1M tokens | Massive context, fast |
| Gemini 1.5 Pro | 2M tokens | Largest available |
| Llama 3.3 70B | 128K tokens | Open-source |

---

[← Back to Notes Index](../ROADMAP.md)
