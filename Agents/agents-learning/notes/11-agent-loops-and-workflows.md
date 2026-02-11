# 11 - Agent Loops & Workflows

**Topic:** Observe → Think → Act → Repeat — how agents actually run

---

## The Agent Loop, Up Close

Topic 10 established that an agent = LLM + tools + loop + autonomy. Now we crack open the loop and see how it actually works.

**Analogy: A detective working a case.** They examine evidence (observe), form a theory (think), go interview someone or pull records (act), then look at the new evidence and repeat. No script tells them what to do at step 4 — each step informs the next. They stop when they've solved the case.

```
     ┌──────────────────────────────────┐
     │                                  │
     ▼                                  │
  OBSERVE ──→ THINK ──→ ACT ───────────┘
  (see result)  (reason)  (use tool)
     │
     └──→ DONE (when task is complete)
```

---

## The Four Phases of the Loop

### 1. Observe
The agent receives information — the user's request, tool results from the last action, error messages, new context. This is the **input** to the LLM at each turn.

### 2. Think
The agent reasons about what it sees. What does this result mean? What's left to do? What should I try next? This is the LLM's generation — its chain-of-thought.

### 3. Act
The agent picks a tool and calls it. Read a file, run a command, search the web, write code. This is a **tool use** — the agent reaches out into the world.

### 4. Repeat or Stop
The agent loops back to Observe (see the tool result) or decides it's done and returns a final answer to the user.

---

## How It Works at the API Level

When you call the Claude API, the response comes back with a `stop_reason`:
- `"tool_use"` → Claude wants to use a tool. Execute it, feed the result back, call again.
- `"end_turn"` → Claude is done. It's returning its final answer.

**That's the entire loop mechanism.** Keep calling the API as long as `stop_reason == "tool_use"`. When it says `"end_turn"`, stop.

```python
messages = [{"role": "user", "content": user_request}]

while True:
    response = claude.messages.create(
        model="claude-sonnet-4-5-20250929",
        tools=available_tools,
        messages=messages
    )

    if response.stop_reason == "end_turn":
        print(response.content)  # Final answer
        break

    # Execute the tool Claude requested
    tool_use = get_tool_call(response)
    tool_result = execute_tool(tool_use.name, tool_use.input)

    # Feed result back for the next iteration
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_result})
```

~10 lines. That's an agent loop.

---

## ReAct: The Formal Name

This observe/think/act loop has a formal name: **ReAct** (Reasoning + Acting). Each turn, the agent explicitly reasons, then acts:

```
Thought:     I need to find the config file
Action:      search_files("config")
Observation: Found config.yaml at /app/config.yaml

Thought:     Now I need to read it to check the DB settings
Action:      read_file("/app/config.yaml")
Observation: host: localhost, port: 5432

Thought:     I have all the info. Done.
Action:      (none — return final answer)
```

Claude Code works exactly this way — you can see it reasoning before each tool call.

---

## Stop Conditions

How does the agent know when to stop?

| Condition | Who Decides |
|---|---|
| Task complete | The LLM (returns `end_turn`) |
| Max iterations hit | Your code (hard limit) |
| Context window full | System (no room for more) |
| Too many errors | Your code (error threshold) |
| User cancels | The user |

**Critical:** Always enforce a **max iteration limit**. Without it, an agent can loop forever — burning tokens and money.

```python
MAX_TURNS = 30

for turn in range(MAX_TURNS):
    response = call_claude(messages)
    if response.stop_reason == "end_turn":
        break
    # ... process tool call ...
else:
    print("Reached max turns without completing.")
```

---

## Agent Loop vs Workflow Patterns

How does the agent loop relate to everything from Topics 05-09?

| Pattern | Who controls the loop? | Steps known upfront? |
|---|---|---|
| Chaining (05) | Your code | Yes |
| Routing (06) | Your code | Yes (per path) |
| Parallelization (07) | Your code | Yes |
| Orchestrator-Workers (08) | LLM plans, code loops | Partially |
| Evaluator-Optimizer (09) | Your code | Yes |
| **Agent Loop (11)** | **The LLM** | **No** |

**The key shift:** In workflows, your code decides the structure. In an agent loop, the LLM decides. You give it tools and a goal — it figures out the rest.

---

## When Agent Loop vs When Workflow

**Use a workflow** when you know the steps, the task is repeatable, and you want predictability.

**Use an agent loop** when you can't predict what steps are needed, the task is exploratory, or different inputs need completely different approaches.

**Combine both:** Real systems do. Claude Code is an agent loop at the top level, but inside each turn it might effectively chain (read → edit → test) or parallelize (search multiple places at once). The agent decides which workflow pattern to apply.

```
Agent Loop (outer)
  └── decides to: chain(read → edit → test)
  └── decides to: parallelize(search A, search B)
  └── decides to: evaluate(check if tests pass)
```

---

## The Context Window Is the Agent's Memory

Each iteration, the full conversation history goes back to the LLM:

- **Early observations are still visible** — the agent remembers what it found 10 steps ago
- **The context grows every iteration** — each tool call + result adds tokens
- **Context limits are real** — after enough iterations, old context gets compressed or dropped

This is why max iterations matter for more than just cost — eventually the agent loses coherence because it can't hold everything in context.

---

## Claude Code as a Real Agent Loop

When you ask Claude Code to "fix this bug":

```
Turn 1:  THINK:   I need to find where the error occurs
         ACT:     grep for the error message

Turn 2:  OBSERVE: Found it in auth.py line 42
         THINK:   I need to read that file
         ACT:     read auth.py

Turn 3:  OBSERVE: Missing a null check
         THINK:   I'll add the check
         ACT:     edit auth.py

Turn 4:  OBSERVE: File edited successfully
         THINK:   I should run tests
         ACT:     run pytest

Turn 5:  OBSERVE: All tests pass
         THINK:   Bug fixed, tests pass — done
         ACT:     (return final answer)
```

Five turns. No code told it those exact five steps — the LLM decided each one based on what it observed. A different bug might take 2 turns or 15.

---

## Common Pitfalls

1. **No max iterations** — Agent loops forever. Always set a limit.
2. **Too many tools** — More tools = more confusion about which to pick. Keep the toolset focused.
3. **No error handling** — Agent retries the same failing action endlessly. Detect repeated failures.
4. **Context bloat** — Every tool result stays in context. Large results eat up the window. Truncate or summarize.
5. **Overusing agents** — If you know the steps, just use a workflow. Agents are for when you genuinely don't know.

---

## Connection to Previous Topics

- **Topic 10 (What Makes an Agent):** Introduced the loop as one of three ingredients. Now we've shown exactly how it works — the observe/think/act cycle, the API signals, the stop conditions.
- **Topics 05-09 (Workflow Patterns):** Workflows are the **building blocks** agents use. An agent doesn't replace workflows — it decides when to use each one.
- **Topic 08 (Orchestrator-Workers):** The closest workflow to an agent. Difference: in orchestrator-workers, your code runs the loop. In an agent, the LLM runs the loop.
- **Topic 04 (Augmented LLM):** Tools, retrieval, memory are the augmentations. The agent loop is the engine that decides when and how to use each one.

---

[← Back to ROADMAP](../ROADMAP.md)
