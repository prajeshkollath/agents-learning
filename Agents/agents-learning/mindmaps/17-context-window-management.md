# Context Window Management

## Why It Matters
### Hard token limit per model
### Exceeding = API error (no partial response)
### More tokens = more cost + slower responses
### Your code must prevent overflow

## Token Counting
### Exact: count_tokens() API
### Estimate: len(text) // 4
### ~4.5 chars/token for English
### Estimate good for thresholds, not precision

## Strategy 1: Truncation
### Drop oldest turns when over budget
### Always keep system prompt
### Must drop complete turn pairs
### Simple but total context loss

## Strategy 2: Sliding Window
### Keep last N turns (fixed rule)
### Turn-based or token-based
### Token-based more precise (turns vary in length)
### Same loss as truncation, just more predictable

## Strategy 3: Summarization
### LLM compresses old turns into summary
### Silent: auto-triggered, user never sees
### Prompted: explicit summarize request
### Costs extra API call per compression
### Preserves old context in compressed form

## Hybrid Pattern (Production)
### System prompt (always kept)
### Summary of old turns (compressed)
### Recent turns verbatim (sliding window)
### New message (current)
### LangChain: ConversationSummaryBufferMemory

## Summarization Triggers
### By turn count
### By token count
### By percentage of window
### Depends on use case

## Window Full = Hard Error
### API rejects the call
### Must reserve room for response
### Your code is the safety net

## Interaction with Caching
### Summarization breaks cache prefix
### Implicit cache: one prefix that grows (extends, not overwrites)
### Explicit cache: fixed at creation, never grows
### Cache saves money, not space
### Summary goes as fresh tokens (small, changes often)
### One cached_content per API call only

## Products Handle It Too
### Claude Code: silent summarization
### Repeated compression loses detail over time
### Eventually start new conversation
### RAG on history is most sophisticated (Topic 21)
