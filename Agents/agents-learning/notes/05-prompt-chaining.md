# 05 - Prompt Chaining

**Topic:** Output of one LLM call becomes input of the next

---

## What Is Prompt Chaining?

Breaking a complex LLM task into **multiple sequential API calls**, where each call's output becomes part of the next call's input.

The chain lives in **your code** (the orchestrator). The LLM just sees one prompt each time — it has no idea it's part of a bigger chain.

**Core insight:** The intelligence is in the LLM, but the workflow is in your code.

---

## Why Not Just One Big Prompt?

| Single Prompt | Prompt Chain |
|---|---|
| LLM tries to do everything at once | Each step is focused and verifiable |
| Hard to debug — where did it go wrong? | Easy to inspect output at each step |
| Can't add quality checks mid-process | Can add **gates** between steps |

---

## The Basic Pattern

```
Input → [LLM Call 1] → Output 1
                          ↓
         Output 1 → [LLM Call 2] → Output 2
                                      ↓
                     Output 2 → [LLM Call 3] → Final Output
```

**Analogy: Assembly line** — each station does ONE focused job and passes its output to the next. No single station needs to know how to build the whole car.

---

## Gates (Checkpoints)

A **gate** is a programmatic check (not an LLM call) between chain steps that decides whether the output is good enough to continue.

```
Input → [Generate] → Gate: Is output valid JSON?
                        ├── Yes → [Next step]
                        └── No  → Stop or retry
```

Gates give you quality control without burning tokens on another LLM call.

---

## Where Does the Chain Live?

**In your code. 100%.** The orchestrator handles:
- Calling the LLM multiple times
- Passing outputs forward between steps
- Running gate checks
- Deciding whether to continue or stop

```python
# YOUR CODE does the chaining — not the LLM

response1 = call_claude("Extract key topics from this article: " + article)

# Gate (pure code, no LLM)
if len(response1) == 0:
    return "No topics found"

response2 = call_claude("Summarize each topic: " + response1)

response3 = call_claude("Create a tweet thread: " + response2)
```

The LLM doesn't know it's step 2 of 3. It just sees a prompt and responds.

---

## Prompt Chaining vs Few-Shot

| | Few-Shot | Prompt Chaining |
|---|---|---|
| **How many LLM calls?** | ONE | Multiple |
| **Purpose** | Teach format/behavior via examples | Decompose complex task into steps |
| **Where it lives** | Inside a single prompt | Across multiple prompts in code |
| **Analogy** | Showing someone an example before a task | Assembly line with multiple stations |

You can use few-shot *inside* a chain step. They work at different levels.

---

## Chains vs Agent Loops

| Prompt Chain | Agent Loop |
|---|---|
| **Fixed** sequence of steps | **Dynamic** — agent decides next step |
| Predetermined flow | Autonomous decisions |
| Easier to reason about | More flexible |
| Better for known tasks | Better for open-ended tasks |

Prompt chaining = **workflow** (you define the steps).
Agent loop = **agent** (LLM decides what comes next).

---

## Concrete Example: Code Review Bot

```
Step 1: "Analyze this code and list all potential issues"
    → Output: List of issues

Step 2: "For each issue, suggest a specific fix"
    → Input: List of issues from Step 1

Gate: Are there any critical-severity issues?
    → If no critical issues: skip to Step 4

Step 3: "For critical issues, provide detailed explanations"

Step 4: "Format everything into a markdown report"
    → Final Output
```

---

## Connection to Previous Topics

- **Topic 04 (Augmented LLM):** The orchestrator layer from Topic 04 is what runs the chain. The chain IS the orchestrator's logic.
- **Claude Code** already chains internally — when it searches, reads, analyzes, and fixes, each tool call's output informs the next. But that's an **agentic chain** (dynamic), not a predetermined workflow chain.

---

[← Back to ROADMAP](../ROADMAP.md)
