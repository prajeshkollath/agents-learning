# 07 - Parallelization

**Topic:** Running LLM calls simultaneously, then combining

---

## What Is Parallelization?

Running multiple LLM calls at the same time, then combining their results. Instead of waiting for each call to finish before starting the next, you fire them all off together.

**Analogy: Pizza kitchen** — three people work simultaneously (dough, toppings, sauce), then combine everything and put it in the oven. Nobody waits for the other.

```
              ┌─→ [LLM Call A] ─┐
Input ────────┼─→ [LLM Call B] ─┼─→ [Combine] → Output
              └─→ [LLM Call C] ─┘
```

---

## Two Patterns

### 1. Sectioning

Split the work — each call does a **different task** on the **same input**:

```
"Analyze this document" →
    ├─→ [Analyze tone]
    ├─→ [Extract key facts]
    └─→ [Check for bias]

    → Combine all three into one report
```

**Why:** Speed. The tasks are independent, so no reason to wait.

### 2. Voting

Same prompt, multiple times — aggregate for **reliability**:

```
"Is this email spam?" →
    ├─→ [LLM Call 1] → "Yes"
    ├─→ [LLM Call 2] → "Yes"
    └─→ [LLM Call 3] → "No"

    → Majority vote: "Yes" (2 out of 3)
```

**Why:** Reduce variance. LLM outputs aren't deterministic — voting smooths out errors.

---

## Sectioning vs Voting

| | Sectioning | Voting |
|---|---|---|
| **Each call does** | A different task | The same task |
| **Why parallel?** | Speed — tasks are independent | Reliability — reduce variance |
| **Combine how?** | Merge results together | Majority vote or best-of-N |
| **Analogy** | Pizza kitchen — different stations | Panel of judges — same question |

---

## Where It Lives

In the **orchestrator code**, same as chaining and routing. The LLM doesn't know it's one of three parallel calls.

```python
import asyncio

async def analyze_document(doc):
    tone, facts, bias = await asyncio.gather(
        call_claude("Analyze the tone: " + doc),
        call_claude("Extract key facts: " + doc),
        call_claude("Check for bias: " + doc)
    )
    return f"Tone: {tone}\nFacts: {facts}\nBias: {bias}"
```

---

## Key Rule

You can only parallelize tasks that **don't depend on each other**. If Call B needs Call A's output, that's chaining, not parallelization.

---

## When to Use Which Pattern

| Pattern | Use When |
|---|---|
| **Chaining** | Steps depend on each other |
| **Routing** | Input needs ONE specific path |
| **Parallelization** | Multiple independent tasks on the same input |

---

## Combining Patterns

Patterns compose together:
- **Route first, then parallelize** within a route
- **Parallelize, then chain** — run 3 calls in parallel, combine results, chain into next step
- **Parallelize with gates** — each parallel branch has its own quality checks

---

## Connection to Previous Topics

- **Topic 05 (Chaining):** Sequential. Parallelization is simultaneous. You can chain after parallelization.
- **Topic 06 (Routing):** Routing picks ONE path. Parallelization runs MULTIPLE paths at once.
- **Claude Code** does this — fires off multiple tool calls in parallel when they're independent.

---

[← Back to ROADMAP](../ROADMAP.md)
