# 12 - MCP Servers as Agent Tools

**Topic:** Where agent tools come from — and how a standard protocol connects them

---

## Why This Matters

In Topic 10, the definition of an agent was: LLM + **tools** + loop + autonomy. In Topic 11, we saw the loop. Now: where do those tools actually come from?

Somebody has to define the tools, connect them to the LLM, and make sure the LLM knows how to call them. MCP is how that happens.

---

## The Simple Definition

**MCP (Model Context Protocol)** is a standard way to give an LLM access to tools and data sources — without hardcoding each one.

Think of it as a **USB standard for AI tools**. Before USB, every device had its own proprietary connector. MCP is the universal plug — any LLM can connect to any tool provider through the same interface.

---

## The New Employee Analogy

Imagine you hire a new employee (the LLM). They're smart but don't know your company's systems. They need access to:
- The database
- The email system
- The project management tool
- The company wiki

You could write custom integration instructions for each one. Or you could give them a **single universal badge** that works on every system — and each system just publishes what actions it supports. That badge is MCP. Each system is an **MCP server**.

The employee doesn't need to know how each system works internally. They just see: "here are the actions I can take" and call them through the standard interface.

---

## The Three Key Pieces

| Piece | What It Is | In the Analogy |
|-------|-----------|----------------|
| **MCP Server** | A program that exposes tools/resources over the protocol | Each company system (database, email, wiki) |
| **MCP Client** | Connects to servers and surfaces tools to the LLM | The universal badge reader |
| **Host** | The application running the LLM (Claude Code, Claude Desktop, etc.) | The office building |

---

## How They Connect

```
Host (Claude Code)
  └── MCP Client (built into Claude Code)
        ├── connects to → MCP Server: memory-bank  (knowledge graph tools)
        ├── connects to → MCP Server: mindmap       (markdown → HTML conversion)
        ├── connects to → MCP Server: filesystem    (read/write/search files)
        └── connects to → MCP Server: (any other tool provider)
```

This project uses exactly this structure — the two MCP servers (`memory-bank` and `mindmap`) are live examples of agent tools being delivered via the protocol.

---

## What an MCP Server Exposes

An MCP server can expose three things:

| Type | What It Is | Example |
|------|-----------|---------|
| **Tools** | Functions the LLM can call | `create_entity`, `search_nodes`, `read_file` |
| **Resources** | Data the LLM can read | Files, database records, API responses |
| **Prompts** | Reusable prompt templates | System prompts, instruction sets |

---

## Connection to the Agent Loop

In Topic 11, the loop was:

```
OBSERVE → THINK → ACT (use tool) → OBSERVE → ...
```

MCP is what makes **ACT** possible at scale. Instead of hardcoding a fixed list of tools per agent, you connect MCP servers and the agent gets a dynamic, expandable toolset. Add a new MCP server = agent gets new capabilities immediately.

---

## Why a Standard Protocol?

Without MCP:
- Every tool integration is custom code
- Switching LLMs means rewriting all tool connectors
- Adding a new tool means updating every agent separately

With MCP:
- Tool providers write their server once
- Any MCP-compatible host (Claude Code, Claude Desktop, others) can use it
- The LLM sees a consistent interface regardless of what's underneath

---

## Real Examples in This Project

| MCP Server | Tools It Provides | Used By |
|------------|------------------|---------|
| `memory-bank` | `create_entities`, `search_nodes`, `read_graph`, `add_observations` | Documenter agent — stores learning progress |
| `mindmap` | `convert_markdown_to_mindmap` | Documenter agent — generates interactive HTML mindmaps |

Both are configured in Claude Code settings and available as tools in every conversation in this project.

---

## Common Misconceptions

- **"MCP is just an API"** — It's a protocol, not just an API. It defines how tools are discovered, described, and called — not just how HTTP requests work.
- **"MCP servers are only for external services"** — They can wrap anything: local files, databases, internal tools, third-party APIs.
- **"The LLM knows about MCP"** — The LLM just sees a list of tools with descriptions. It doesn't know or care that they came from MCP servers.

---

## Connection to Previous Topics

- **Topic 04 (Augmented LLM):** Retrieval, tools, memory are the augmentations. MCP is the standardized delivery mechanism for tools and retrieval.
- **Topic 10 (What Makes an Agent):** Tools are one of the three ingredients. MCP defines how those tools are packaged and delivered.
- **Topic 11 (Agent Loop):** The ACT phase calls tools. MCP is what those tools are and where they come from.

---

[← Back to ROADMAP](../ROADMAP.md)
