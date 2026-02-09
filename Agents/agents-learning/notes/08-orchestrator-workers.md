# 08 - Orchestrator-Workers

**Topic:** One LLM plans, others execute

---

## What Is the Orchestrator-Workers Pattern?

One LLM call (the orchestrator) breaks a task into subtasks, and other LLM calls (the workers) execute each subtask. The orchestrator then combines the results.

**Analogy: Project manager and their team** — the PM doesn't write code. They look at requirements, break them into tasks, assign them to specialists, and assemble the final deliverable.

```
Task → [Orchestrator: "Break this into subtasks"]
            ↓
       Subtask list: [A, B, C]
            ↓
       ┌─→ [Worker: Do A] ─┐
       ├─→ [Worker: Do B] ─┼─→ [Orchestrator: Combine results]
       └─→ [Worker: Do C] ─┘
```

---

## What Makes This Different From All Previous Patterns

| Pattern | Who decides the steps? | Steps known in advance? |
|---|---|---|
| **Chaining** | Developer (hardcoded) | Yes |
| **Routing** | Code/LLM classifier | Yes (paths are predefined) |
| **Parallelization** | Developer (hardcoded) | Yes |
| **Orchestrator-Workers** | **LLM** (at runtime) | **No** — depends on the input |

This is the first pattern where the **LLM itself decides what work needs to happen**.

---

## The Two Roles

**Orchestrator** (the planner):
- Receives the high-level task
- Breaks it into subtasks
- Decides how many workers are needed
- Combines worker results into the final output

**Workers** (the executors):
- Each gets ONE focused subtask
- Works independently
- Returns result to orchestrator
- Doesn't know about other workers

---

## Everything Happens in Your Code

The orchestrator call is just another LLM call in your code. Your code calls the orchestrator, parses its response, loops through subtasks, calls workers, then calls the orchestrator again to combine.

```python
# Step 1: Orchestrator plans
plan = call_claude(orchestrator_prompt.format(task=task))
subtasks = json.parse(plan)  # YOUR CODE parses

# Step 2: Workers execute (YOUR CODE loops)
results = []
for subtask in subtasks:
    result = call_claude(worker_prompt.format(subtask=subtask))
    results.append(result)

# Step 3: Orchestrator combines
final = call_claude(combine_prompt.format(sections=results))
```

The LLM never calls itself. Your code is always the one making calls.

---

## Structured Output Is Critical

The orchestrator prompt must say something like "Return ONLY a JSON array". Your code needs to **parse** the orchestrator's response to know what workers to spin up. If the LLM returns freeform text, your code can't loop through it.

You'd want a **gate** (from Topic 05) here to verify the orchestrator returned valid JSON before proceeding.

---

## Three Levels of Worker Prompt Flexibility

### Level 1: Hardcoded Worker Prompt
```python
worker_prompt = "You are a blog writer. Write this section: {subtask}"
```
Fixed system. Only writes blogs. Orchestrator just decides **what sections**.

### Level 2: Orchestrator Generates Worker Prompts
The orchestrator returns **both the subtask AND the instructions** for each worker:
```json
[
  {"task": "Write intro", "instructions": "You are a blog writer. Write an engaging opening..."},
  {"task": "Refactor auth", "instructions": "You are a Python developer. Refactor this module..."}
]
```
Same system handles any request. Most flexible.

### Level 3: Base Role + Dynamic Task (Most Common in Production)
Developer sets **guardrails/role**, orchestrator fills in the **specifics**:
```python
base_prompt = "You are a helpful assistant. Follow safety guidelines."
# Orchestrator only decides the tasks
call_claude(base_prompt + "\n\nYour task: " + subtask)
```

| Level | Who writes worker prompts? | Flexibility | Control |
|---|---|---|---|
| **1** | Developer (hardcoded) | Low | High |
| **2** | Orchestrator LLM | High | Low |
| **3** | Both (base + dynamic) | Medium | Medium |

**Claude Code is Level 3** — Anthropic set the base system prompt and guardrails, but the orchestrator dynamically decides what to read, edit, and test.

---

## The Tradeoff

- **Hardcoded workers** = predictable, testable, limited
- **LLM-generated workers** = flexible, general, harder to control

More orchestrator freedom = more general-purpose, but less predictable.

---

## Connection to Previous Topics

- **Topic 05 (Chaining):** The orchestrator-workers flow IS a chain (plan → execute → combine), but the middle steps are dynamic.
- **Topic 06 (Routing):** Level 2 orchestrators effectively route subtasks to different worker types.
- **Topic 07 (Parallelization):** Workers can run in parallel since they're independent. Parallelization is a tool the orchestrator can use.

---

[← Back to ROADMAP](../ROADMAP.md)
