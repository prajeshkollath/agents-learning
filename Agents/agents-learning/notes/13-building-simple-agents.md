# 13 - Building Simple Agents

**Topic:** What you actually need to build an agent — with or without Claude Code

---

## The Core Insight

Claude Code is an **agent runtime** — it has the loop, tool executor, and MCP client already built. When you use it, you only configure behavior via markdown prompts.

Without Claude Code, **you are the runtime**. You build the loop and the tools yourself.

---

## The Three Layers Every Agent Needs

```
┌─────────────────────────────────┐
│  1. The Loop                    │  ← while stop_reason != end_turn
│  2. Tool Definitions + Executor │  ← JSON schema + Python functions
│  3. System Prompt               │  ← role, rules, behavior
└─────────────────────────────────┘
          calls ↓
       Claude API (the LLM)
```

| Layer | In Claude Code | In Raw Python |
|-------|---------------|---------------|
| Loop | Built in | You write ~10 lines |
| Tools | MCP servers + built-in tools | Python functions + JSON schemas |
| System Prompt | `agents/*.md` + `CLAUDE.md` | A string passed to `system=` |

---

## The Contractor Analogy

Hiring a contractor (the LLM). You give them:
- **Job description** (system prompt) — what they do, how they work, what they won't do
- **Tools and access** (tools + MCP) — keys to the building, DB access
- **Briefing documents** (context) — background reading

Same contractor, different job descriptions = different agents. The intelligence is the same; the *configuration* shapes behavior.

---

## Agent Configuration in Claude Code

An agent in Claude Code is just a markdown file:

```
agents/
  planner.md     ← Planner agent
  tutor.md       ← Tutor agent
  evaluator.md   ← Evaluator agent
  documenter.md  ← Documenter agent
```

Each file defines: **Role**, **Responsibilities**, **Rules**, **Handoff**.

### Two-Layer Context

```
CLAUDE.md        ← always loaded; project-wide context and rules
agents/*.md      ← loaded on demand when you invoke an agent
```

`CLAUDE.md` is the project-level system prompt. Agent files add role-specific behavior on top.

---

## What Makes a Prompt an "Agent" Prompt

A chatbot prompt: *"Answer this question helpfully."*

An agent prompt: *"Here's your goal. Here are your tools. Here are the rules. Go figure it out."*

The difference is **autonomy** — the prompt grants the LLM permission and direction to decide its own steps, use tools, and iterate until done.

| Ingredient | Chatbot | Agent |
|-----------|---------|-------|
| LLM | Yes | Yes |
| Tools | Maybe | Yes |
| Loop | No (one turn) | Yes (multi-turn) |
| Autonomy | No | Yes — "go figure it out" |

---

## Building an Agent in Raw Python

The loop (from Topic 11) + tools together form the runtime:

```python
messages = [{"role": "user", "content": user_request}]

while True:
    response = claude.messages.create(
        model="claude-sonnet-4-5",
        system="You are a helpful agent...",   # layer 3: system prompt
        tools=available_tools,                  # layer 2: tool definitions (JSON)
        messages=messages
    )

    if response.stop_reason == "end_turn":
        break

    tool_result = execute_tool(response)        # layer 2: tool executor
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_result})  # layer 1: loop
```

The loop is ~10 lines. The **tools are the real work** — each tool is:
1. A Python function (what it does)
2. A JSON schema (description of name, parameters, purpose — so the LLM knows how to call it)

---

## The Framework Landscape

All frameworks solve the same problem: **abstracting the loop + tools**. They differ in style and complexity:

| Framework | Made By | Style | Complexity |
|-----------|---------|-------|-----------|
| **Pydantic AI** | Pydantic team | Type-safe, Python-native, lightweight | Low |
| **Claude Agent SDK** | Anthropic | Claude-native, handoffs, multi-agent | Medium |
| **LangGraph** | LangChain Inc | Graph-based stateful workflows | High |

```
Raw Python  <  Pydantic AI ≈ Agent SDK  <  LangGraph
(control)      (lightweight)               (power)
```

Pydantic AI and Agent SDK are closer siblings — both lightweight, Python-native, focused on clean agent definitions. LangGraph is a full workflow orchestration engine.

### Why Learn Raw Python First

Every framework is hiding the same three layers. If you don't know what the loop looks like, you can't debug why a framework agent is looping forever. If you don't know what a tool definition is, you can't fix a tool the LLM is calling wrong.

Raw Python → frameworks is the right order. Frameworks first is building on a foundation you can't see.

---

## Roadmap Connection

- **Phase 4 (Topics 15-21):** Build the loop, tools, chains, and memory in raw Python
- **Phase 7:** Pydantic AI (29) → Agent SDK (30) → LangGraph (31) → When to use what (32)

---

## Connection to Previous Topics

- **Topic 10 (What Makes an Agent):** LLM + tools + loop + autonomy. This topic shows exactly how each ingredient is provided — prompt, JSON schemas, while loop.
- **Topic 11 (Agent Loop):** The while loop shown here IS the agent loop from Topic 11, now in context.
- **Topic 12 (MCP Servers):** In Claude Code, MCP servers provide the tools layer. In raw Python, you write Python functions instead.

---

[← Back to ROADMAP](../ROADMAP.md)
