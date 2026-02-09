# 09 - Evaluator-Optimizer

**Topic:** One generates, another critiques in a loop

---

## What Is the Evaluator-Optimizer Pattern?

One LLM generates output, and another LLM critiques it — then the generator revises based on the critique. This loops until the output is good enough.

**Analogy: Writer and editor** — the writer produces a draft, the editor gives feedback ("intro is weak, add data"), the writer revises, the editor reviews again until satisfied.

```
[Generator] → Draft → [Evaluator] → Feedback
     ↑                                  │
     └──── Revise based on feedback ────┘

     (loops until evaluator says "good enough")
```

---

## Gate vs Evaluator-Optimizer

| Gate (Topic 05) | Evaluator-Optimizer |
|---|---|
| **Pass/fail** — binary check | **Qualitative feedback** — what to fix |
| Code-based (is it valid JSON?) | LLM-based (is the writing good?) |
| Stops or retries blindly | Tells the generator **what to improve** |
| No loop intelligence | Loop gets smarter with each iteration |

A gate says "no." An evaluator says "no, and here's why, and here's what to fix."

---

## The Two Roles

**Generator** (the optimizer):
- Produces the initial output
- Receives feedback from the evaluator
- Revises its output based on that feedback

**Evaluator** (the critic):
- Reviews the generator's output against criteria
- Provides specific, actionable feedback
- Decides when the output is good enough to stop

---

## The Loop in Code

```python
max_iterations = 3
draft = call_claude(generator_prompt.format(task=task))

for i in range(max_iterations):
    evaluation = call_claude(evaluator_prompt.format(
        output=draft,
        criteria="Check for bugs, edge cases, clarity"
    ))

    if "APPROVED" in evaluation:
        break

    draft = call_claude(revision_prompt.format(
        previous=draft,
        feedback=evaluation
    ))

return draft
```

**Critical:** Always set a **max iterations** limit. Without it, the loop could run forever.

---

## "Separate LLM Call" — Not Necessarily a Separate Model

The evaluator is a **separate API call with a different prompt**, not necessarily a different model. You can use the same model (e.g., Sonnet for both). What matters is:

- **Different prompts** — one creates, the other critiques
- **Fresh context** — evaluator doesn't see the generator's "thinking", just the output
- **No anchoring bias** — the evaluator isn't biased by having generated the output

### But You CAN Use Different Models

| Strategy | Generator | Evaluator | Why |
|---|---|---|---|
| Same model | Sonnet | Sonnet | Simple, works well |
| Cheap gen, smart eval | Haiku | Sonnet | Save cost on drafts, invest in quality |
| Smart gen, cheap eval | Opus | Haiku | When generation is hard but checking is easy |

---

## Why Not Self-Critique in the Same Call?

Asking the same LLM to generate AND critique in one context causes **anchoring** — it's biased toward thinking its own output is good. A separate call with a fresh context and critic-specific prompt produces more honest evaluation.

Like asking a writer to proofread their own essay vs having a separate editor do it.

---

## Where This Pattern Shows Up

- **Code generation** — generate code, review for bugs, revise
- **Writing** — draft, critique, revise
- **Translation** — translate, back-translate to check, revise
- **Data extraction** — extract, verify against source, correct

---

## How All 5 Workflow Patterns Fit Together

```
05 - Chaining:            A → B → C                 (sequential steps)
06 - Routing:             Classify → pick path        (branching)
07 - Parallelization:     A, B, C at once → combine   (fan-out)
08 - Orchestrator-Workers: LLM plans → workers execute (dynamic planning)
09 - Evaluator-Optimizer:  Generate → critique → loop  (feedback loop)
```

These compose together. A real system might route input, use orchestrator-workers to plan, parallelize workers, run each through an evaluator-optimizer loop, and chain results into a final output.

---

[← Back to ROADMAP](../ROADMAP.md)
