# 14 - State & Memory

**Topic:** How agents remember — within a session and across sessions

---

## The Core Problem

Every Claude API call is stateless by default. A fresh LLM with no history. So how does an agent "remember" what it did 5 turns ago? How does it carry information between sessions? That's what state and memory solve.

**State** = what the agent knows *right now*, in this conversation.
**Memory** = what the agent can access from *before* — past sessions, stored facts, documents.

---

## The Three Types of Memory

Think of a doctor:

| Memory Type | Doctor Analogy | In an Agent |
|------------|---------------|-------------|
| **In-context (working)** | Everything in your head during the appointment | The `messages` array in the context window |
| **External (episodic)** | Your patient file — what happened last visit | A database, vector store, or file the agent reads |
| **In-weights (semantic)** | Medical school knowledge — baked in | The LLM's training data (can't change at runtime) |

---

## Memory Type 1: In-Context (State)

This is the `messages` array you keep appending to in the agent loop. Every tool call, result, and response — added to the list and sent back on the next API call.

```python
messages = [
    {"role": "user",      "content": "Find the bug"},
    {"role": "assistant", "content": "I'll search..."},
    {"role": "user",      "content": "<tool result>"},
    {"role": "assistant", "content": "Found it in auth.py"},
    ...
]
```

The agent "remembers" turn 1 in turn 5 because turn 1 is still in the list. It's not really memory — it's **state passed explicitly**.

**Limit:** The context window. After enough turns, old messages get cut off and the agent starts forgetting.

### Handling Overflow

| Strategy | How It Works |
|----------|-------------|
| **Truncate** | Drop oldest messages — simple but agent loses early context |
| **Summarize** | Compress old messages into a summary, keep recent ones |
| **Sliding window** | Always keep last N messages + a running summary at the top |

---

## Memory Type 2: External (Long-Term)

Anything the agent reads from *outside* the context window:
- A file on disk
- A database record
- A vector search result
- A key-value store

In this project, the `memory-bank` MCP server is external memory. The Documenter writes to it after each topic; the next conversation reads it — bridging sessions.

### Applications of Long-Term Memory

- **User preferences** — "always respond in Spanish", preferred style, past decisions
- **Continuity** — where we left off last session, ongoing task progress
- **Domain knowledge built over time** — codebase architecture, customer profiles, research notes
- **Avoiding repetition** — errors already tried, questions already asked, work already done
- **Multi-agent coordination** — Agent A writes findings, Agent B reads them without sharing a conversation

---

## Memory Type 3: In-Weights

The LLM's training knowledge — Python syntax, history, reasoning. You can't update this at runtime. Treat it as a fixed foundation.

---

## How to Decide What to Store

Two approaches, most systems use both:

### Approach 1: Rule-Based (You Decide Upfront)
Hardcode the storage logic in the agent's instructions:
- "After every session, write a summary to memory."
- "When the user states a preference, store it."
- "When a task completes, record the outcome."

Good for predictable, structured events.

### Approach 2: LLM-Judged (Agent Decides)
Give the agent a `save_to_memory(content, reason)` tool and instruct it to use judgment. The LLM decides: *"The user just told me they're building a fintech app — worth saving."*

Good for open-ended conversations where you can't predict what matters.

### The Decision Filter

```
Is this information...
  ├─ Reusable in future sessions?     → store it
  ├─ Specific to this moment only?    → keep in context, don't store
  ├─ Already stored?                  → update, don't duplicate
  ├─ Too noisy / low-value?           → discard
  └─ Sensitive (passwords, PII)?      → never store
```

---

## Retrieval: Getting the Right Memory

### State (In-Context) — Automatic
Already in the `messages` array. The LLM sees it all on every call. No retrieval needed.

### Long-Term Memory — 3 Retrieval Patterns

| Pattern | How | When to Use |
|---------|-----|-------------|
| **Exact lookup** | `memory.get("user:prajesh:preferences")` | Structured, predictable data |
| **Semantic search** | Vector embedding search by meaning | Open-ended: "what do I know about X?" |
| **Structured query** | Filter by type, time, category | Recent memories, typed records |

### Semantic Search (Vector/RAG)

```
Query: "What does the user know about agent tools?"
  ↓
Convert query to vector embedding
  ↓
Find closest stored memories by cosine similarity
  ↓
Return: Topic 12 notes, MCP server observations, tool use concepts
```

Covered in depth in Topic 19 (memory engineering).

---

## The Full Memory Cycle

```
Session starts
    ↓
1. Query memory: "What's relevant to this user/task?"
    ↓
2. Inject top 3-5 results into system prompt (selectively, not everything)
    ↓
3. Agent works with retrieved memory + live context
    ↓
4. Session ends → write new learnings back to memory store
```

### The Injection Pattern

```python
system_prompt = f"""
You are a helpful assistant.

## What you remember about this user:
{retrieved_memories}

## Current task:
{user_request}
"""
```

The LLM treats retrieved memories like any other context — it doesn't know how they were fetched.

---

## The Summarization Pattern

Long conversations can't be stored raw — too noisy. The standard pattern:

```
Raw conversation (100 messages)
    ↓
LLM summarizes: "Key decisions: X, Y. User preference: Z."
    ↓
Store the summary, discard the raw transcript
```

This is **summary memory** — built in Topic 19.

---

## State vs Memory: Summary

| | State (In-Context) | Long-Term Memory |
|--|-------------------|-----------------|
| **Where** | `messages` array | External store |
| **Retrieval** | Automatic | Manual (lookup/search) |
| **Limit** | Context window | Practically unlimited |
| **Survives session?** | No | Yes |
| **Speed** | Instant | Lookup latency |

---

## Connection to Previous Topics

- **Topic 11 (Agent Loop):** The `messages` array IS the state. Every append to it is state management.
- **Topic 12 (MCP Servers):** `memory-bank` MCP server is the external memory store in this project.
- **Topic 04 (Augmented LLM):** Memory was listed as one of the three augmentations. This topic shows exactly how it works.
- **Topic 19 (coming):** Memory engineering — conversation memory, summary memory, vector/RAG built in Python.

---

[← Back to ROADMAP](../ROADMAP.md)
