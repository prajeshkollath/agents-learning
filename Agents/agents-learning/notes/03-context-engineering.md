# 03: Context Engineering

## The Fundamental Problem

**LLMs have limited context windows but conversations have unlimited information.**

Every API call sends the entire conversation history. As conversations grow:
- Token costs increase linearly with each turn
- Eventually you hit the context window limit (200k, 500k tokens, etc.)
- Performance can degrade with extremely long contexts

**Context engineering** is how you manage this growth intelligently.

---

## The Three Core Strategies

### 1. Sliding Window

**Definition:** Keep only the last N conversation turns, discard everything older.

**Analogy:** Like a moving camera that only sees the current scene:
- You see the present clearly
- The past is completely forgotten
- Simple and predictable

**Example:**
```
Window size = 3 turns

Turn 1: "What's Python?"
Turn 2: "Explain lists"
Turn 3: "What about dictionaries?"
Turn 4: "How do I loop?" → Turn 1 gets dropped
Turn 5: "What's a function?" → Turn 2 gets dropped
```

**When to Use:**
- Short-term memory is sufficient
- Each turn is self-contained
- You want predictable token costs

**Trade-offs:**
- Simple to implement
- Fixed token cost ceiling
- BUT: Loses all history beyond the window
- Can forget important context from earlier turns

---

### 2. Selective Retention

**Definition:** Keep important information, drop filler. You decide what matters based on rules or patterns.

**Analogy:** Like packing for a trip:
- Keep essentials (passport, tickets, medicine)
- Drop nice-to-haves (extra shoes, books)
- YOU decide what's essential based on rules

**Three Approaches:**

#### A. Structured Fields (Manual)
Extract specific data into a structure you maintain:
```
User profile:
  - Name: Sarah
  - Role: Engineer
  - Preferences: Python, hates Java
  - Project context: Building a web scraper
```

**How:** Your code extracts and updates fields using pattern matching or parsing.

#### B. Pattern Matching (Rules-Based)
Define rules for what to keep:
```python
# Keep any message containing these keywords
important_patterns = ["error", "API key", "deadline", "user_id"]

# Drop conversational filler
drop_patterns = ["thanks", "ok", "got it", "sure"]
```

#### C. LLM Extraction (Dynamic)
Ask the LLM to extract important facts:
```
"Review this conversation and extract:
- User's goal
- Technical requirements
- Constraints or blockers
- Decisions made"
```

**When to Use:**
- Some information is critical, most is noise
- You can define what "important" means
- Need to preserve context across long conversations

**Trade-offs:**
- More control over what's kept
- Can retain critical info indefinitely
- BUT: Requires upfront design (what to keep?)
- Can miss context if rules are wrong

---

### 3. Summarization

**Definition:** Compress old conversation turns into a condensed summary, keep recent turns as-is.

**Analogy:** Like taking meeting notes:
- Old meetings → Summary: "Decided on tech stack, set deadline for March"
- Recent discussion → Full detail: Exact words and context
- Summaries lose nuance but capture key points

**How It Works:**
```
Turns 1-10 → [Summarize] → "User is building a chatbot. Stack: Python + FastAPI.
                             Main challenges: rate limiting, context management"

Turns 11-15 → Keep verbatim (recent context)
```

**When to Use:**
- Conversations are genuinely long and complex
- Need both history awareness AND recent detail
- Can afford the cost of summarization calls

**Trade-offs:**
- Balances history and detail
- Natural and human-like
- BUT: Summaries lose nuance and specifics
- Each summarization = extra LLM call (cost!)
- Can compound errors if summary is wrong

---

## Choosing the Right Strategy

| Strategy | Best For | Avoid When |
|----------|----------|------------|
| **Sliding Window** | Short-term tasks, self-contained turns | Need long-term memory |
| **Selective Retention** | Tracking specific facts/state across time | Don't know what to keep upfront |
| **Summarization** | Long, complex conversations with history dependencies | Need exact details from the past |

---

## Hybrid Approaches: Using All Three Together

Real-world agents often combine strategies:

**Example: Customer Support Agent**
```
1. Selective Retention:
   - User info: name, account_id, subscription tier
   - Open issues: [issue_123, issue_456]

2. Summarization:
   - Turns 1-20 → "User reported login issue, we reset password.
                   Then they had billing question, resolved via refund."

3. Sliding Window:
   - Keep last 5 turns verbatim (current conversation context)
```

**Why This Works:**
- **Structured fields** = Critical facts always available
- **Summary** = Historical context without full detail
- **Recent turns** = Full context for immediate conversation flow

---

## Important Distinction: Agent Prompts vs Orchestrator

**Agent Prompt:**
- Defines the agent's **behavior and role**
- "You are a helpful tutor. Use analogies. Check understanding."
- Stays constant, not part of "context engineering"

**Orchestrator/Context Manager:**
- Manages the **conversation history** sent to the agent
- Decides what to keep, drop, summarize
- Implements the context strategy (sliding window, retention, etc.)

**Key Insight:**
- The agent's **prompt** tells it HOW to behave
- The **orchestrator** decides WHAT context the agent sees
- Context engineering happens at the orchestrator level, NOT in the agent prompt

**Example:**
```
Orchestrator does:
- Summarizes turns 1-10
- Keeps user_id and project_name in structured fields
- Passes last 5 turns + summary + fields to agent

Agent receives:
- System prompt: "You're a coding tutor..."
- Structured context: {user_id, project_name}
- Summary of turns 1-10
- Full detail of turns 11-15
- Current user message

Agent doesn't know or care about the context strategy—it just responds
```

---

## The Token Cost Reality

**Without context engineering:**
```
Turn 1: 100 tokens
Turn 2: 100 + 150 = 250 tokens
Turn 3: 250 + 200 = 450 tokens
Turn 10: ~2000+ tokens per call
```

**With sliding window (last 3 turns):**
```
Every turn after Turn 3: ~450-500 tokens (stable!)
```

**With summarization:**
```
Turns 1-10: 2000 tokens → Summarize → 200 tokens
Turns 11-15: 800 tokens
Total per call: ~1000 tokens (vs 2000+)
```

Context engineering directly controls costs and enables longer conversations.

---

*See [ROADMAP.md](../ROADMAP.md) for full learning path.*
