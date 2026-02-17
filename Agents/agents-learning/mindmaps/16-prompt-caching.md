# Prompt Caching

## Why Cache?
- API is stateless — full context sent every call
- 5k token system prompt × 20 turns = 100k tokens billed
- Fresh: $0.10/MTok → Cached: $0.025/MTok (4x cheaper)

## Two Types

### Implicit (Automatic)
- Gemini detects repeated prefixes server-side
- No code change needed
- Frequency-dependent not just token-size-dependent
- Free tier: unreliable — may not trigger
- Check: `cached_content_token_count` in usage_metadata
  - None = no hit
  - > 0 = cache hit

### Explicit (Manual + TTL)
- You control what gets cached and for how long
- `client.caches.create()` → returns cache name
- Reference with `cached_content=cache.name`
- Guaranteed hit within TTL
- Minimum: 4096 tokens (gemini-2.0-flash)
- Default TTL: 1 hour
- Small storage fee per hour → delete when done

## Token Counting (Important!)
- Implicit: `prompt_token_count` = ALL tokens; `cached_content_token_count` = cache hit
- Explicit: `prompt_token_count` = FRESH tokens ONLY; `cached_content_token_count` = cached
- Do NOT subtract: total cost = fresh (full price) + cached (cheap)

## Cache Management API
- Create: `client.caches.create()`
- List: `client.caches.list()`
- Extend TTL: `client.caches.update()`
- Delete: `client.caches.delete()`

## When to Use
- Large system prompt + many users → implicit
- Document upload → explicit on upload event
- Codebase review → explicit
- Batch processing → explicit covering full batch TTL
- Dev/testing → explicit short TTL
- Per-user history → do NOT cache (dynamic)

## Key Learnings from Code Run
- Implicit did not trigger at 4,221 tokens (free tier, only 2 calls)
- Explicit cached 4,213 tokens successfully
- Each Q used only 10-13 fresh tokens vs 4213 cached
- 4096 minimum discovered via API error

## Connections
- Topic 14 (Memory): caching ≠ memory — cost optimization on in-context state
- Topic 15 (Gemini API): usage_metadata is how you verify caching
- Topic 17 (Context Window): cache stable prefix + manage growing history
