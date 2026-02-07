# 01: Prompts vs Workflows vs Agents

## The Control Spectrum

```
Prompt ──────────────── Workflow ──────────────── Agent
(you control)          (code controls)            (LLM controls)
```

## Definitions

### Prompt
- Single LLM call
- One input, one output
- No orchestration

### Workflow
- Multiple **LLM calls** orchestrated by **code**
- Routing and steps are **predetermined** by the developer
- Shared state passed between steps
- Each step can gate the next (validation, routing)
- The LLM calls don't have to be agents -- they can be simple prompt-in/text-out

### Agent
- The **LLM itself** decides what to do next
- Chooses which tools to call and when to stop
- Flow is **dynamic and not predetermined**

## What is "Shared State" in Workflows?

**Definition:** The data/information that gets passed from one workflow step to the next.

**Analogy:** Like a relay race baton:
- Each runner (workflow step) receives the baton (the state)
- The baton has notes from previous runners
- Each runner adds their own notes before passing it on
- The final runner has all the accumulated information

**Example Workflow:**
1. Step 1: Translate Spanish → English
2. Step 2: Summarize the English text
3. Step 3: Format as bullet list

**Shared state includes:**
- Original Spanish text
- Translated English text (passed to step 2)
- Summary (passed to step 3)
- Metadata: user ID, timestamp, language

**Key Point:** In workflows, YOUR CODE decides what state to pass forward. In agents, the LLM's conversation history is the state, and the LLM decides what to do with it.

## Key Distinction: Who Decides the Next Step?

| Aspect               | Workflow              | Agent                  |
|-----------------------|-----------------------|------------------------|
| Who decides next step?| Your code             | The LLM                |
| Flow predictable?     | Yes                   | No                     |
| Steps known upfront?  | Yes                   | No                     |
| Example               | "Translate, then summarize, then format" | "Figure out how to fix this bug" |

## Common Misconception

> "A workflow is agents running in sequence or parallel"

**Correction:** A workflow chains **LLM calls** (not agents). If the components were agents deciding their own flow, that becomes a **multi-agent system**, which is a more advanced pattern.

---

*See [ROADMAP.md](../ROADMAP.md) for full learning path.*
