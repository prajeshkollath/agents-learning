---
title: Caching Strategies
created: 2026-07-01
updated: 2026-07-01
tags:
  - ai-agents
  - cost
  - performance
  - architecture
status: learning
aliases:
  - Prompt Caching
  - Semantic Caching
  - Caching
---

# Caching Strategies

> Reusing prior computation to cut **cost and latency** — chiefly **prompt caching**
> (the provider caches a stable prompt *prefix* so repeat requests skip re-processing
> it) and **semantic caching** (reuse a whole answer for a similar question). The
> single biggest input-side lever in [[Token Cost Optimization]].

## What it is

Agents resend a large, mostly-unchanged prompt every turn (system prompt, tool
schemas, history — see below). **Prompt caching** lets the provider store that stable
prefix and serve it at ~0.1× the input price on later calls, instead of re-billing it
in full each time. It also cuts latency (the cached prefix isn't re-processed).

## First: why is the whole history even being sent?

The LLM API is **stateless** — it remembers nothing between calls. Whatever agent you
build (raw API or a framework), *something on your side* holds the conversation and
**resends it every turn**:

```
messages = []                      # you (or the framework) own this list
messages.append(user_message)      # add the new turn
resp = llm(messages)               # send the WHOLE list
messages.append(resp)              # append assistant reply (incl. tool_use)
messages.append(tool_results)      # append tool results → next turn sends more
```

A framework "knows to send history" only because its **memory abstraction** (e.g.
LangChain `ConversationBufferMemory`, an agent's `messages` state) *is* this list,
managed for you ([[State Management]] · [[Agent Memory]]). There's no server-side
session — the growing prompt is exactly why caching matters.

## Prompt caching in practice

**It's opt-in — you turn it on; it is not automatic by default** (Anthropic; some
providers do implicit caching). You don't *implement* the cache — the provider runs
it — but you **decide what to cache and where the breakpoint goes.**

```python
# (a) Automatic placement — simplest: one flag, SDK caches the last cacheable block
client.messages.create(..., cache_control={"type": "ephemeral"})

# (b) Manual placement — mark the block ending the stable prefix
system=[{"type": "text", "text": BIG_PROMPT, "cache_control": {"type": "ephemeral"}}]
```

### What to cache — the stable prefix

Render order is `tools → system → messages`, so a breakpoint on the last system block
caches **tools + system** together. Cache the parts that repeat unchanged:

- **system prompt**, **tool definitions** (paid on every call — [[Tool Calling]]),
- large **fixed context** reused across calls: a long document, few-shot examples,
  reused RAG context.

Put **volatile** content (the user's question, timestamps) *after* the last
breakpoint so it never invalidates the cached part.

### When it's worth it — three conditions, all true

1. **Large enough** — minimum ~1024–4096 tokens (model-dependent); shorter prefixes
   *silently* don't cache (no error).
2. **Reused** — the same prefix hits ≥2 requests within the TTL (5-min default; 1-hour
   option). Break-even ≈ 2 requests for the 5-min cache.
3. **Stable** — byte-identical each time.

### The #1 gotcha — silent invalidation

Caching is a **prefix match**: one byte change *anywhere* in the prefix busts
everything after it. Keep volatile content out of the prefix:

- ❌ `datetime.now()` / a UUID / request ID in the system prompt → new prefix each call
- ❌ reordering tools, or `json.dumps()` without sorted keys → non-deterministic bytes
- ❌ adding/removing/reordering a **tool** mid-conversation (tools are at position 0)
- ✅ frozen system prompt, deterministic tool order, dynamic bits at the very end

### Pricing recap (per input bucket)

Uncached input **1×**, cache-**read** ~**0.1×**, cache-**write 1.25×** (5-min) / **2×**
(1-hour). A read is cheap; a write costs *more* than a normal token — a one-time
premium that pays off across later reads. Full bucket math in [[Cost Control]].

### Verify it's actually working

Check the response usage: **`cache_read_input_tokens > 0`** means a hit. Stuck at
zero across identical-prefix calls → a silent invalidator is at work. Frameworks vary
— some add `cache_control` for you, many don't; **don't assume, verify.**

## Semantic caching (a different idea)

Prompt caching reuses a *prefix* within one conversation. **Semantic caching** reuses
a *whole answer*: embed the incoming question, and if it's similar enough to a past
one, return the stored answer without calling the model at all. Great for FAQ-style
traffic; risky when answers are personalised or time-sensitive (stale hits).

## Likely issues
- **Assuming caching is automatic** → you never set `cache_control`, pay full price.
- **Silent invalidator in the prefix** → `cache_read_input_tokens` stays 0.
- **Caching a too-short prefix** → below the minimum, silently no-ops.
- **Semantic cache serving stale/wrong answers** → tune the similarity threshold; skip
  for personalised or fast-changing content.

## Tradeoffs
- **Write premium vs read savings** — caching only pays off when the prefix is read
  again enough times within the TTL; one-shot prompts shouldn't be cached.
- **Freshness vs reuse (semantic)** — looser matching reuses more but risks wrong hits.

## Example

A support agent caches its system prompt + tool schemas (paid once at 1.25×, then
~0.1× on every later turn) and puts the user's message after the breakpoint. Result:
a 40k-token prefix that used to cost full price each turn now costs ~0.1× — the single
biggest line-item cut, verified by `cache_read_input_tokens` climbing turn over turn.

## Q&A insights

- **"How does a framework know to send history?"** — It doesn't, magically. The API is
  stateless; the framework's memory abstraction *holds* the `messages` list and resends
  it every turn. Raw API → you hold it yourself. See [[State Management]].
- **"Do I have to cache manually?"** — You opt in (it's not on by default), but you
  don't build the cache — one `cache_control` flag enables it; the provider runs it.
  You choose *what* (the stable prefix: system + tools + fixed context) and *where* the
  breakpoint sits.
- **"When/what to cache?"** — When the prefix is large (≥ ~1–4k tokens), reused (≥2
  calls in the TTL), and byte-stable. Keep volatile content after the last breakpoint;
  verify with `cache_read_input_tokens > 0`.

## Related
- [[Token Cost Optimization]] — caching is its biggest single lever
- [[Cost Control]] — the per-bucket pricing (1× / 0.1× / 1.25×–2×)
- [[Context Building]] — trimming/compaction, the other way to shrink the prompt
- [[Tool Calling]] — tool schemas sit in the cacheable prefix; changing them busts it
- [[State Management]] · [[Agent Memory]] — where the resent history lives
- [[Latency Management]] · [[12 Production and Cost Engineering]] · [[AI Agents MOC]]
