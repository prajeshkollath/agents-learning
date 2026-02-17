# Topic 17: Context Window Management

## Core Concept

Every model has a hard token limit (context window). Gemini 2.0 Flash has 1M tokens. When you exceed it, the API **rejects the call** — no partial response, no auto-truncation, nothing. Your code must prevent this from ever happening.

Even below the limit, more tokens = more cost + slower responses. Context window management is about **deciding what stays in, what gets cut, and what gets compressed**.

**Analogy:** A whiteboard in a meeting room. Limited space. Truncation = erasing oldest notes. Sliding window = keeping only the last N minutes of notes. Summarization = writing a compact bullet-point summary before erasing the detailed notes.

---

## Token Counting

Two approaches to measure what's in the window:

| Method | How | Cost | Precision |
|---|---|---|---|
| `client.models.count_tokens()` | API round-trip | Free but adds latency | Exact |
| `len(text) // 4` | Local estimate | Zero | ~12% off for English text |

From the code run: 2250 characters = 502 tokens (actual ratio: 4.5 chars/token). The ~4 estimate gave 562 — off by 12%. Good enough for "should I trim?" checks, not for precision.

---

## Three Strategies

### 1. Truncation (Simplest)

Drop the oldest messages when total exceeds a threshold. Always keep the system prompt. **Must drop complete turn pairs** (user + model together) — if you drop just the user message but keep the model response, the model sees an answer with no question.

- Pro: Dead simple, no extra API calls
- Con: Old context is completely lost

**From the code run:** After truncating to last 3 turns, the model was asked "remind me about variables?" and had no idea — it only knew about generators, async/await, and context managers.

### 2. Sliding Window (Refined Truncation)

Same as truncation but with a **fixed, predetermined** window size (e.g., "keep last N turns" or "keep turns that fit within X tokens").

The difference from truncation is mindset:
- Truncation: "I'm at 95% capacity — quick, drop old turns"
- Sliding window: "I always keep exactly the last 5 turns. Period."

In code, they often look identical. Token-based sliding window is more precise than turn-based because turns vary wildly in length.

### 3. Auto-Summarization (Smartest)

Use the LLM itself to compress older turns into a compact summary. Replace the detailed old messages with the summary. The model gets context about what happened earlier, but in compressed form.

**Two flavors:**
- **Silent summarization**: Code detects the threshold and summarizes automatically — the user never sees it happen
- **Prompted summarization**: Explicitly ask the model "summarize so far" and use the result

**Tradeoff:** Costs an extra API call each time you summarize. Only pays off when the conversation is long enough that compression savings exceed the summarization cost.

**From the code run:** Same "remind me about variables?" question — with summarization, the model correctly answered "variables are names that store values, dynamically inferred." The summary preserved that early context.

---

## The Hybrid Pattern (Production Systems)

Real systems combine summarization + sliding window:

```
[System prompt]                    - ALWAYS kept, never touched
[Summary of turns 1-20]           - summarized old context
[Turns 21-28 verbatim]            - sliding window of recent turns
[New user message]                 - current turn
```

This gives: full detail for recent context + compressed but present old context + stable instructions.

**From the code run:** The `ConversationManager` class triggered auto-compression at turn 6 (threshold of 5 turns). Summarized turns 1-3, kept 4-6 verbatim. At turn 8, asking about variables from turn 1 — the model recalled it from the summary. Prompt tokens stayed bounded (~220-274) instead of growing unboundedly.

**Framework equivalents:**
- LangChain: `ConversationSummaryBufferMemory(max_token_limit=500)` — does exactly this hybrid pattern internally
- LangGraph: Implement as a graph node that triggers on token count
- Pydantic AI / Google ADK: Manual — you write this function yourself

---

## When to Trigger Summarization

| Trigger | How it works |
|---|---|
| Turn count | "Every 10 turns, summarize the oldest 7" |
| Token count | "When total tokens > 4000, compress until under 2000" |
| Percentage | "When history exceeds 70% of window, summarize" |

No right answer — depends on use case. Tutoring bot summarizes aggressively (old Q&A detail doesn't matter). Legal assistant summarizes rarely (every detail could matter).

---

## What Happens When the Window is Full

The API **returns a hard error**. No partial response, no auto-truncation. Your code crashes or your try/except catches it.

Must also leave room for the response — if you fill the window to the brim with input, the model has no room to generate output.

```
1,000,000  token window
-   8,192  reserved for response
-  buffer  for safety
= ~990,000  your actual input budget
```

---

## How Products Handle This (Q&A Insight)

Products like Claude Code, ChatGPT, Copilot face the same problem. Claude Code uses **silent summarization** — it compresses older messages automatically as context approaches limits. The user never sees it happen.

With repeated compression, each round loses more detail:
```
Turns 1-50   -> Summary A (detailed)
Turns 1-100  -> Summary B (Summary A compressed again, loses nuance)
Turns 1-200  -> Summary C (fairly vague now)
```

Eventually the summary is so lossy it's not useful — that's when you start a new conversation. There's no magic; compression has diminishing returns.

**Other product strategies:** aggressive sliding window, tiered compression, RAG on own history (store old turns in vector DB, retrieve relevant ones), session reset.

---

## Summarization and Caching Interaction (Q&A Insights)

### Summarization Breaks the Cache Prefix

When you summarize and replace old turns, the bytes sent to the API change. The old implicit cache prefix (`[Sys][T1][T2]...`) no longer matches the new one (`[Sys][Summary]...`). The old cache entry becomes orphaned — it still exists on Google's servers until TTL expiry but nothing hits it.

This is a real tradeoff: before summarizing you have a well-cached long prefix. After summarizing, the cache restarts from scratch. In practice it's fine — the whole point of summarizing was to reduce tokens.

### Implicit Caching is One Prefix That Grows (Not Separate Entries)

Implicit caching doesn't cache individual turns separately. It caches **one prefix that extends**:
```
Call 1: Compute KV for [Sys][T1], store
Call 2: Reuse [Sys][T1], compute only [T2], store [Sys][T1][T2]
Call 3: Reuse [Sys][T1][T2], compute only [T3], extend
```

One entry that grows — not overwritten, extended. That's why it's called **prefix** caching. Works from the start, extending forward only.

### Implicit Cache Internals Are a Black Box

Google doesn't document eviction policy, TTL behavior, or size limits for implicit caching. Whether TTL resets on hit (likely, but unconfirmed), whether there's a size cap — unknown. You can't rely on implicit caching for anything guaranteed. Design as if it doesn't exist; treat savings as a pleasant surprise.

### Explicit Cache is Fixed at Creation

Explicit cache **never grows**. You create it once with specific content. Conversation turns are sent fresh every call — they're the dynamic part.

- TTL counts from creation, not from last use (can extend before expiry)
- All or nothing — no partial eviction
- Only ONE `cached_content` per API call — can't reference two caches

### Don't Cache Conversation Turns Explicitly

Caching each turn explicitly would mean: delete old cache, create new cache with updated content, every turn. Terrible idea — pays creation cost every turn, adds latency, wastes the old cache.

**The practical split:**
| Content type | Strategy |
|---|---|
| Large stable content (docs, system prompt) | **Explicit cache** |
| Growing conversation history | **Context management** (truncate/summarize) |
| Frequently repeated prefixes | **Implicit cache** (let Gemini handle it) |

### Summary as Fresh Tokens, Not Cached

If you have a document in explicit cache and also a conversation summary, the summary goes in the **fresh** portion — it's small (~100-200 tokens) and changes each time you re-summarize. Not worth caching. The API only allows one `cached_content` per call anyway.

---

## Caching + Context Management = Complementary Tools

```
Context window:
  [System prompt]           - CACHED (stable prefix, Topic 16)
  [Summary of old turns]    - FRESH (small, changes occasionally)
  [Recent turns verbatim]   - FRESH (changes every turn)
  [New message]             - FRESH
```

Cache the stable parts → save money (Topic 16). Manage the growing parts → prevent overflow (Topic 17). Total must still fit in the window — **caching saves money, not space**.

---

## Connection to Other Topics

- **Topic 14 (State & Memory)**: Context management is managing in-context state — what the model sees right now
- **Topic 16 (Prompt Caching)**: Caching and context management are complementary — cache stable parts, manage growing parts
- **Topic 21 (Memory Engineering)**: RAG on conversation history is the most sophisticated context strategy — store old turns externally, retrieve relevant ones per query
