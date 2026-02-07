# 02: Prompt Engineering - System Prompts, Few-Shot, Chain-of-Thought

## Why Prompt Engineering Matters

**How you ask matters as much as what you ask.** The same LLM can give genius-level output or complete garbage depending on how you structure your prompt. Prompt engineering is about learning patterns that consistently get better results.

---

## 1. System Prompts

### Definition
Sets the rules, role, and context for the LLM *before* the user ever says anything.

### Analogy
Like briefing an actor before they go on stage:
- **Without system prompt**: Actor improvises with no script or character
- **With system prompt**: "You're a wise mentor. Stay calm, use analogies, never rush."

### Where System Prompts Go
- Part of the conversation context
- Invisible to the user but shapes every response
- In Claude Code, agent files (like `tutor.md`) are system prompts

### Example
```
System: You are a patient tutor. Explain concepts using everyday analogies.
        Start simple, build up complexity gradually.

User: "Explain quantum computing"
LLM: [gives explanation with relatable analogies, checks understanding]
```

### Key Point
System prompts let you:
- Shape behavior and tone
- Assign a role or persona
- Set expectations for input/output format
- Establish rules the LLM should follow

---

## 2. Few-Shot Prompting

### Definition
Giving the LLM a few examples of the input-output pattern you want, then asking it to follow that pattern.

### The Spectrum

| Type | Description | Example |
|------|-------------|---------|
| **Zero-shot** | Just instructions, no examples | "Translate this to French" |
| **One-shot** | One example | "Hello → Bonjour. Now translate 'Goodbye'" |
| **Few-shot** | Multiple examples (2-5) | Show 3 translation examples, then ask for a new one |

### Example: Structured Data Extraction

**Zero-shot:**
```
Extract sentiment and product from this feedback.
Input: "The new phone is amazing but the battery dies too fast"
```

**Few-shot:**
```
Extract sentiment and product from feedback:

Example 1:
Input: "Love the laptop, super fast!"
Output: {"product": "laptop", "sentiment": "positive"}

Example 2:
Input: "The headphones broke after one week"
Output: {"product": "headphones", "sentiment": "negative"}

Now do this one:
Input: "The new phone is amazing but the battery dies too fast"
```

The LLM learns the pattern and output format from examples.

### Where Do Examples Go?

**Option 1: In the System Prompt** (best for consistency)
- Examples are always there, applied to every request
- Good when the format/task is always the same

**Option 2: In the User Prompt** (best for flexibility)
- You control examples per request
- Good when examples change based on context

### When to Use Few-Shot
- Need a specific output format (JSON, table, specific style)
- Task has edge cases better shown than explained
- Zero-shot results are inconsistent

### Token Cost Trade-off
- More examples = better accuracy
- More examples = more tokens = higher cost + slower response
- **Rule of thumb**: Start with 2-3 examples, add more only if results are inconsistent

---

## 3. Chain-of-Thought (CoT)

### Definition
Asking the LLM to show its reasoning steps before giving the final answer.

### Analogy
Like showing your work in math class:
- **Without CoT**: "What's 23 × 17?" → "391" (right or wrong, can't verify)
- **With CoT**: "What's 23 × 17? Show your work." → Shows calculation steps (reasoning visible and verifiable)

### Example: Logic Problem

**Without CoT:**
```
User: Sarah has 3 apples. She gives half to John, then buys 5 more. How many?
LLM: 6.5 apples
```

**With CoT:**
```
User: Sarah has 3 apples. She gives half to John, then buys 5 more.
      How many? Think step-by-step.

LLM: Let me think through this:
     1. Sarah starts with 3 apples
     2. Gives half to John = 1.5 apples
     3. Sarah has: 3 - 1.5 = 1.5 apples left
     4. Buys 5 more apples
     5. Final: 1.5 + 5 = 6.5 apples

     Answer: 6.5 apples
```

### How to Trigger Chain-of-Thought

**Method 1: Zero-Shot CoT** (explicit instruction)
- "Think step-by-step"
- "Show your reasoning"
- "Let's think through this carefully"

**Method 2: Few-Shot CoT** (examples with reasoning)
```
Example: "If a train travels 60 mph for 2 hours, how far?"
Reasoning:
- Speed = 60 mph
- Time = 2 hours
- Distance = Speed × Time = 60 × 2 = 120 miles
Answer: 120 miles

Now solve: "If a car travels 80 mph for 3 hours, how far?"
```

### Does the LLM Follow Your Steps?

**No—it uses its own judgment!**
- You show the PATTERN of step-by-step reasoning
- The LLM applies its own logic to the new problem
- You control WHETHER to use CoT, the LLM controls HOW it reasons

### Will the LLM Display Its Reasoning?

**By default: Yes.** The reasoning appears in the response text.

To get only the final answer:
```
"Think through this step-by-step internally, then give ONLY the final answer"
```

Or use structured format:
```
"Output format:
Reasoning: [your steps]
Answer: [final answer only]"
```

### When to Use CoT

✓ **Use for:**
- Math and logic problems
- Multi-step reasoning (planning, analysis, debugging)
- Tasks where mistakes are costly
- When you need to verify reasoning, not just the answer

✗ **Skip for:**
- Simple, direct questions ("What's the capital of France?")
- When you need fast answers without explanation
- Token cost is a concern (reasoning uses more tokens)

---

## Combining the Techniques

**Pro move:** Use all three together!

```
System Prompt: "You're a math tutor. Always show your work."
Few-Shot: [2 examples of step-by-step solutions]
User Prompt: "Now solve this problem step-by-step: [problem]"
```

| Technique | What It Does | When to Use |
|-----------|--------------|-------------|
| **System Prompt** | Sets role, rules, tone | Always—foundation for behavior |
| **Few-Shot** | Shows examples of desired pattern | Need specific format or handle edge cases |
| **Chain-of-Thought** | Makes LLM show reasoning | Complex tasks, need verifiable logic |

---

## Important: LLMs Are Stateless

### The Token Growth Problem

Every API call sends the **entire context**, even in conversations:

**Conversation turns:**
- Turn 1: System + Q1
- Turn 2: System + Q1 + A1 + Q2
- Turn 3: System + Q1 + A1 + Q2 + A2 + Q3

**Token cost grows linearly** with each turn!

### Conversation vs Isolated Calls

| Aspect | Isolated Calls | Conversation |
|--------|----------------|--------------|
| Memory between calls | None | Yes (via history) |
| How memory works | You manually pass context | API/SDK manages history |
| Token cost per call | System + current message | System + ALL history + current |
| Token cost over time | Constant | **Grows** with each turn |

### Key Insight
- Conversations don't save tokens—they just make context management easier in code
- You're still paying for the entire history on every turn
- Eventually you hit context limits or cost becomes prohibitive

### Token Reduction Strategies (Preview of Topic 03)

1. **Summarization**: Compress old conversation into a summary
2. **Sliding window**: Keep only last N turns
3. **Selective retention**: Keep important parts, drop filler
4. **Smart truncation**: System automatically manages context (what Claude Code does)

---

*See [ROADMAP.md](../ROADMAP.md) for full learning path.*
