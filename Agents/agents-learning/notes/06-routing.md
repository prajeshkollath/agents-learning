# 06 - Routing

**Topic:** Classifying input to pick the right path

---

## What Is Routing?

Routing is classifying an input first, then sending it down the right path based on that classification. The router itself doesn't do the real work — it's a **traffic cop** that directs inputs to specialized handlers.

It lives in the **orchestrator code**, just like chaining.

**Analogy: Hospital triage desk** — a nurse assesses you and directs you to the right department. The nurse doesn't treat you, they classify and direct.

```
                    ┌─→ [Path A: Billing handler]
Input → [Classify] ─┼─→ [Path B: Technical support]
                    └─→ [Path C: General FAQ]
```

---

## How Routing Differs From Chaining

| Prompt Chaining | Routing |
|---|---|
| All inputs follow the **same** path | Inputs follow **different** paths |
| Linear: Step 1 → Step 2 → Step 3 | Branching: Classify → pick ONE path |
| Assembly line | Triage desk |

Routing happens **before** any chain. You classify first, then the chosen path might itself be a chain.

---

## Two Ways to Route

**1. LLM-based routing** — Ask the LLM to classify the input:

```python
classification = call_claude(
    "Classify this customer message into one of: billing, technical, general.\n"
    "Message: " + user_input
)

if classification == "billing":
    handle_billing(user_input)
elif classification == "technical":
    handle_technical(user_input)
else:
    handle_general(user_input)
```

**2. Code-based routing** — Use keywords, regex, or simple rules:

```python
if "invoice" in user_input or "charge" in user_input:
    handle_billing(user_input)
elif "error" in user_input or "crash" in user_input:
    handle_technical(user_input)
else:
    handle_general(user_input)
```

| | LLM Router | Code Router |
|---|---|---|
| **Accuracy** | High — understands intent | Lower — keyword matching |
| **Cost** | Uses tokens | Free |
| **Speed** | Slower (API call) | Instant |
| **Best for** | Ambiguous, natural language input | Clear, structured signals |

You can **combine both**: code checks first (cheap), and if unsure, fall back to the LLM (accurate).

---

## Model Routing (Cost Optimization)

Routing isn't just about picking which chain to run — it can also pick **which model** to use:

```
Input → [Classify complexity]
              ├─→ Simple question  → Haiku (fast, cheap)
              ├─→ Medium task      → Sonnet (balanced)
              └─→ Complex reasoning → Opus (powerful, expensive)
```

If 70% of inputs are simple, sending them all to the most powerful model wastes money. Route easy stuff to a cheap model, save the expensive one for when it's needed.

---

## Routing on Multiple Dimensions

A single router can decide several things at once:

| Dimension | Example |
|---|---|
| **Which chain** | Billing vs Technical vs FAQ |
| **Which model** | Haiku vs Sonnet vs Opus |
| **Which tools** | Needs database lookup vs no tools needed |
| **Human vs AI** | AI can handle it vs escalate to a person |

---

## Nested Routing

Routes can be nested — a first router picks the broad category, a second router within that category picks the specific handler:

```
Input → [Router 1: What department?]
              ├─→ Technical → [Router 2: What severity?]
              │                    ├─→ Critical → Escalate to human
              │                    └─→ Normal   → Auto-fix chain
              └─→ Billing   → [Router 2: What action?]
                                   ├─→ Refund   → Refund chain
                                   └─→ Question → FAQ chain
```

---

## Routing + Gates

The **router** picks the path, and **gates** (from Topic 05) within that path validate quality. They work at different levels — routing picks **which** path, gates check **quality** within a path.

---

## Common Pitfall: Over-Routing

If 90% of inputs need the same handling, don't build a router. Just use a single chain and handle edge cases with an `if` statement.

**Rule of thumb:** Route when paths are **genuinely different** — different prompts, different tools, different output formats.

---

## Where Routing Fits in Workflow Patterns

```
05 - Chaining:        Input → A → B → C            (sequential)
06 - Routing:         Input → Classify → pick path  (branching)
07 - Parallelization: Input → A, B, C simultaneously (fan-out)
08 - Orchestrator:    LLM decides the plan dynamically (agent-like)
```

Routing is the first pattern where the workflow **branches** instead of just flowing forward.

---

## Connection to Previous Topics

- **Topic 04 (Augmented LLM):** The router is part of the orchestrator layer. It decides which tools/prompts/chains to use.
- **Topic 05 (Chaining):** Each route can lead to its own chain. Routing picks which chain to run.
- **Claude Code** does this constantly — it classifies whether it needs to search, read, edit, or run a command. That's routing.

---

[← Back to ROADMAP](../ROADMAP.md)
