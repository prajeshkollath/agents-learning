# 10 - What Makes an Agent

**Topic:** Tool use, loops, autonomy

---

## What Is an Agent?

An LLM running in a loop that can use tools, observe results, and decide its own next step — until it determines the task is complete.

**Analogy:**
- Workflows = GPS with a fixed route (you programmed the directions)
- Agent = human driver (sees the road, makes decisions, takes detours, decides when they've arrived)

---

## The Three Ingredients

### 1. Tool Use
The agent can take actions — read files, search the web, query databases, run code. Without tools, the LLM can only generate text. It can't DO anything.

### 2. A Loop
The agent runs in a cycle: Observe → Think → Act → Observe → Think → Act... Not a fixed number of iterations. The agent decides when to stop.

### 3. Autonomy
The agent decides **what** tool to use next, **when** to use it, and **when** it's done. Your code doesn't hardcode these decisions.

---

## Agent vs Workflow

| | Workflow | Agent |
|---|---|---|
| **Who controls the flow?** | Your code | The LLM |
| **Steps predetermined?** | Yes | No |
| **Tool selection** | Hardcoded | LLM chooses |
| **When to stop** | Code decides | LLM decides |
| **Predictability** | High | Lower |
| **Flexibility** | Lower | High |

Orchestrator-workers (Topic 08) was the bridge — the orchestrator planned dynamically, but your code still controlled the loop. A true agent controls the loop itself.

---

## The Spectrum

```
Pure LLM ←─────────────────────────→ Full Agent

ChatGPT          ChatGPT          Copilot         Claude Code
(basic chat)     (with tools)     (agent mode)
   ↑                ↑                 ↑               ↑
   No tools      Has tools,       Full loop,      Full loop,
   No loop       some loop        autonomy,       autonomy,
   You drive     Semi-auto        tools, MCP      tools, MCP
```

---

## API vs Agent App vs Framework

| What you use | What you get | Agent? |
|---|---|---|
| Claude API (basic) | Raw LLM, single call | No |
| Claude API + your loop code | Agent you built yourself | Yes — you built it |
| Agent frameworks (SDK) | Pre-built loop, you configure | Yes — framework built it |
| Claude Code / Copilot | Pre-built agent app | Yes — company built it |

The API gives you the brain. The agent loop, tools, and autonomy are built by **someone** — you, a framework, or the app maker.

---

## Adding Tools (MCP) Doesn't Make Something an Agent

Copilot and Claude Code were already agents before adding MCP tools. They already had the loop and autonomy. MCP just gave them **more tools** — making them more capable agents, not making them agents in the first place.

---

## Basic Chat Apps Are Just LLMs

Accessing ChatGPT/Gemini/Claude in a basic chat interface (no tools, no browsing) = just an LLM. You type, it responds, done. **You** are the loop — you decide to ask again. The LLM has no tools and no autonomy.

---

## Why Build Raw Before Using Frameworks?

- When frameworks break, you can **debug** because you understand the internals
- You can tell when a framework is **overkill** and raw code is simpler
- You can **evaluate** frameworks critically instead of blindly trusting them
- Building a basic agent loop from scratch is ~30-40 lines of Python — it's an exercise, not a project

---

## Connection to Previous Topics

- **Topic 04 (Augmented LLM):** Tools, retrieval, memory are the augmentations. An agent uses all of them autonomously.
- **Topics 05-09 (Workflow Patterns):** Workflows have fixed flows controlled by code. Agents control their own flow.
- **Topic 08 (Orchestrator-Workers):** The bridge — LLM plans dynamically but code still runs the loop. Agents go one step further.

---

[← Back to ROADMAP](../ROADMAP.md)
