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
- **Frequency-dependent, not just token-dependent** — needs to observe the prefix being sent many times before deciding to cache
- `cached_content_token_count` in `usage_metadata` will be `None` if not triggered, `> 0` if it was a cache hit
- Free tier: unreliable — implicit caching may not trigger even above the token threshold
- Not suitable for production use cases where you need guaranteed cache hits

**What counts as the "prefix":**
Implicit caching applies to **any stable prefix** — not just the system prompt. It applies to conversation turns too:
```
[system_instruction]   ← cached if stable and large enough
[turn 1 user]          ← cached once it's been stable across several calls
[turn 1 model]         ← cached once stable
[NEW TURN user]        ← always fresh — prefix ends here
```
The cached portion must be **byte-for-byte identical** across calls. Changing anything mid-history (even one token) busts the cache at that point and everything after it.

**Likelihood by call volume:**
| Calls with same prefix | Implicit cache triggers? |
|---|---|
| 2 calls | Probably not |
| 50 calls in a session | Likely |
| 1000 users/day with same prefix | Almost certainly |
| Free tier, low volume | Unreliable |

Google's implicit cache is tuned for high-volume production traffic — not personal dev accounts.

### 2. Explicit Caching (Manual with TTL)
- You call `client.caches.create()`, Gemini stores the content and returns a cache name
- Reference the cache by name in subsequent calls via `cached_content=cache.name`
- **Guaranteed cache hit** as long as TTL hasn't expired
- Default TTL: 1 hour. Minimum TTL: 60 seconds. Can be extended before expiry.
- You pay a small storage fee per cached token per hour — delete when done

**Minimum token requirements (hard platform limits — not configurable by you):**
| Model | Minimum for explicit caching |
|---|---|
| `gemini-2.0-flash` | 4,096 tokens |
| `gemini-1.5-flash` | 4,096 tokens |
| `gemini-1.5-pro` | 32,768 tokens |

These are Google-imposed floors. You cannot lower them. If your content is below the threshold, the API returns an error with the actual minimum — always check the error message rather than assuming the documented number.

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

**PDF upload scenario (exact flow):**
The same user uploads a PDF and asks multiple questions about it. The trigger is the upload event — not the first question:
```
User uploads PDF
  → your app detects upload
  → immediately calls client.caches.create(pdf_content)
  → Gemini stores it, returns cache.name
User asks question 1 → send: cached_content=cache.name + "Q1"
User asks question 2 → send: cached_content=cache.name + "Q2"
...
User asks question 20 → send: cached_content=cache.name + "Q20"
```
Without caching, every question re-sends the full PDF. With explicit cache, the PDF is paid once at creation; each question pays only for its own tokens.

**RAG caching pattern:**
Only worth doing if your knowledge base is small and fixed (e.g., a product manual always fully loaded into context). For typical RAG where different queries retrieve different chunks — retrieval is dynamic and per-chunk caching adds complexity that rarely pays off. Implicit caching handles frequently-retrieved shared chunks naturally.

---

## Key Learnings from Running the Code

- **Implicit caching did not trigger** even at 4,221 tokens — confirmed frequency-dependent, not just token-size-dependent. The free tier with 2 API calls was not enough signal.
- **Explicit cache created successfully** at 4,213 tokens of document content
- **Token split confirmed**: each question only used 10-13 fresh tokens; all 4,213 document tokens came from cache
- **Cache management works**: create → list → extend TTL → delete all verified in output
- **Minimum is 4096 for gemini-2.0-flash explicit cache** — learned this via the API error (`total_token_count=959, min_total_token_count=4096`)

---

## Who Controls Caching: Product vs Builder

This is an important layering distinction that came up when asking about GitHub Copilot:

| Layer | Who controls caching |
|---|---|
| GitHub Copilot using Claude | GitHub controls it — you don't |
| Claude Code (Claude Max subscription) | Anthropic/Claude Code handles it — you don't |
| Your own agent hitting Gemini API | **You control it** |
| Your own agent hitting Anthropic API | **You control it** (explicit `cache_control` needed) |

When you are a **user** of a product (Copilot, Claude Code), caching is the product's problem. When you are a **builder** hitting an API directly, caching is your responsibility.

GitHub Copilot almost certainly implements caching at scale (economics force it), but you have no visibility into or control over it.

---

## Framework Equivalent

**For Gemini (implicit):** all frameworks get it for free — Gemini handles it server-side regardless of which framework sends the request.

**For Gemini (explicit):** frameworks don't add explicit caching automatically. You create the cache and pass `cache.name` through the framework's model config.

**For Anthropic API:** caching is **always explicit** — you must add `cache_control: {"type": "ephemeral"}` markers to message content. Frameworks generally do not add these automatically.

```python
# Anthropic explicit caching — you must mark it yourself
{"type": "text", "text": "...large content...", "cache_control": {"type": "ephemeral"}}
```

**LangChain "semantic caching"** — this is a completely different concept. It caches entire LLM responses locally: if the same input is sent again, it returns the cached output without calling the API at all. This is not the same as Anthropic or Gemini prompt prefix caching.

---

## Connection to Other Topics

- **Topic 14 (State & Memory)**: Caching is not memory — it's a cost optimization on in-context state. The document is still re-sent logically; the server just skips re-computing it.
- **Topic 17 (Context Window Management)**: Caching and context management work together. Cache the stable prefix; manage (truncate/summarize) the growing dynamic history.
- **Topic 15 (Gemini API Basics)**: `usage_metadata` from Topic 15 is how you verify caching is working — `cached_content_token_count` is the key field.
