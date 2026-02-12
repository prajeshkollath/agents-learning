# State & Memory

## Core Problem
### Every API call is stateless
- Fresh LLM, no history
- State = what agent knows now
- Memory = what agent can access from before

## 3 Memory Types
### In-Context (State)
- The messages array
- Automatic — LLM sees all of it
- Limit: context window size
- Overflow strategies
  - Truncate oldest messages
  - Summarize old messages
  - Sliding window + summary

### External (Long-Term)
- Database, file, vector store
- Survives across sessions
- Manual retrieval required
- memory-bank MCP = live example

### In-Weights (Semantic)
- LLM training knowledge
- Can't change at runtime
- Fixed foundation

## Long-Term Memory Uses
### Personalization
- User preferences
- Communication style
- Past decisions
### Continuity
- Where we left off
- Ongoing task progress
### Domain Knowledge
- Codebase architecture
- Customer profiles
- Research notes
### Avoiding Repetition
- Errors already tried
- Questions already asked
### Multi-Agent Coordination
- Agent A writes, Agent B reads

## What to Store
### Rule-Based
- Hardcode storage triggers
- After session ends
- When preference stated
### LLM-Judged
- save_to_memory() tool
- Agent uses judgment
### Decision Filter
- Reusable in future? → store
- Moment-specific? → skip
- Sensitive/PII? → never store

## Retrieval Patterns
### Exact Lookup
- memory.get("user:prajesh:prefs")
- Structured, predictable data
### Semantic Search
- Query → vector embedding
- Find closest by meaning
- RAG pattern — Topic 19
### Structured Query
- Filter by type, time, category

## Memory Cycle
### Start of session
- Query relevant memories
- Inject top 3-5 into system prompt
### During session
- Agent uses context + memory
### End of session
- Summarize and write new learnings back

## Summarization Pattern
- Raw conversation → LLM summarizes
- Store summary, discard transcript
- Summary memory — covered in Topic 19
