# Topic 16: Prompt Caching

## Core Concept

Every API call sends all tokens to the model — there is no built-in server memory. If your system prompt is 5,000 tokens and you have a 20-turn conversation, you pay for those 5,000 tokens **20 times**. Caching lets you pay for them once.

Gemini stores the KV (key-value) computation for a stable prefix. On subsequent calls that send the same prefix, it skips re-processing and bills at the cached rate.

**Cost difference (gemini-2.0-flash):**
- Fresh input: $0.10 / MTok
- Cached input: $0.025 / MTok → **4x cheaper**

---

## Two Types of Caching

### 1. Implicit Caching (Automatic)
- Gemini detects repeated prefixes server-side and caches them automatically
- No code change required — you just send the same large prefix repeatedly
- **Frequency-dependent, not just token-dependent** — needs to observe the prefix being sent multiple times before deciding to cache
- `cached_content_token_count` in `usage_metadata` will be `None` if not triggered, `> 0` if it was a cache hit
- Free tier: unreliable — implicit caching may not trigger even above the token threshold
- Not suitable for production use cases where you need guaranteed cache hits

### 2. Explicit Caching (Manual with TTL)
- You call `client.caches.create()`, Gemini stores the content and returns a cache name
- Reference the cache by name in subsequent calls via `cached_content=cache.name`
- **Guaranteed cache hit** as long as TTL hasn't expired
- Minimum size: **4096 tokens** for gemini-2.0-flash (the API will error if below this)
- Default TTL: 1 hour. Minimum TTL: 60 seconds. Can be extended before expiry.
- You pay a small storage fee per cached token per hour — delete when done

---

## How to Read Token Counts

### Implicit calls (no explicit cache):
- `prompt_token_count` = ALL input tokens (fresh + any implicitly cached)
- `cached_content_token_count` = tokens served from implicit cache (None if no hit)

### Explicit cache calls:
- `prompt_token_count` = only the **fresh** (non-cached) tokens
- `cached_content_token_count` = tokens served from the explicit cache
- Total input = fresh (full price) + cached (4x cheaper) — do NOT subtract

```python
# Reading token costs correctly for an explicit cache call
cached = response.usage_metadata.cached_content_token_count or 0
fresh = response.usage_metadata.prompt_token_count  # fresh tokens only
```

---

## Explicit Cache API

```python
# Create
cache = client.caches.create(
    model="gemini-2.0-flash",
    config=types.CreateCachedContentConfig(
        contents=[types.Content(role="user", parts=[types.Part(text=LARGE_DOCUMENT)])],
        system_instruction=SYSTEM_INSTRUCTION,
        ttl="3600s",
        display_name="my-cache"
    )
)

# Use
response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(cached_content=cache.name),
    contents="Your question here"
)

# Manage
client.caches.list()
client.caches.update(name=cache.name, config=types.UpdateCachedContentConfig(ttl="7200s"))
client.caches.delete(name=cache.name)
```

---

## When to Cache

| Pattern | Cache type | Why |
|---|---|---|
| Large system prompt, many users | Implicit (auto) | High frequency → Google caches it |
| User uploads a PDF, asks questions | Explicit cache on upload | Guaranteed hit, document used multiple times |
| Codebase review with multiple passes | Explicit | Large fixed context, multiple reads |
| Batch processing with shared prompt | Explicit with TTL covering batch | Cache once, process all at cheap rate |
| Per-user unique conversation history | Don't cache | Dynamic content, not reusable |
| Dev/testing with large context | Explicit short TTL | Save costs during iteration |

---

## Key Learnings from Running the Code

- **Implicit caching did not trigger** even at 4,221 tokens — confirmed frequency-dependent, not just token-size-dependent. The free tier with 2 API calls was not enough signal.
- **Explicit cache created successfully** at 4,213 tokens of document content
- **Token split confirmed**: each question only used 10-13 fresh tokens; all 4,213 document tokens came from cache
- **Cache management works**: create → list → extend TTL → delete all verified in output
- **Minimum is 4096 for gemini-2.0-flash explicit cache** — learned this via the API error (`total_token_count=959, min_total_token_count=4096`)

---

## Framework Equivalent

All frameworks benefit from Gemini's implicit caching automatically (since they just send the same prefix). For explicit caching:
- **Google ADK**: use `CachedContent` with session-level configuration — ADK can reference caches across agents in a multi-agent system
- **Pydantic AI**: pass cache name through model settings
- **LangGraph**: inject `cached_content` into the model config at the graph level

---

## Connection to Other Topics

- **Topic 14 (State & Memory)**: Caching is not memory — it's a cost optimization on in-context state. The document is still re-sent logically; the server just skips re-computing it.
- **Topic 17 (Context Window Management)**: Caching and context management work together. Cache the stable prefix; manage (truncate/summarize) the growing dynamic history.
- **Topic 15 (Gemini API Basics)**: `usage_metadata` from Topic 15 is how you verify caching is working — `cached_content_token_count` is the key field.
