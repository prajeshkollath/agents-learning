# MCP Servers as Agent Tools

## Why MCP
### The Problem
- Tools need to be defined, connected, and described to the LLM
- Without a standard: every tool integration is custom code
- Switching LLMs = rewriting all connectors

### The Solution
- MCP = Model Context Protocol
- Universal standard for connecting LLMs to tools and data
- USB analogy: one standard plug, any device

## Three Key Pieces
### MCP Server
- Exposes tools, resources, prompts over the protocol
- Examples: memory-bank, mindmap, filesystem

### MCP Client
- Connects to servers
- Surfaces available tools to the LLM
- Built into Claude Code

### Host
- Application running the LLM
- Claude Code, Claude Desktop, etc.

## What Servers Expose
### Tools
- Functions the LLM can call
- create_entity, search_nodes, read_file

### Resources
- Data the LLM can read
- Files, DB records, API responses

### Prompts
- Reusable prompt templates

## Connection to Agent Loop
### ACT Phase
- MCP tools are what the agent calls during ACT
- Add MCP server = agent gets new capabilities instantly

### Dynamic Toolsets
- No hardcoded tool lists
- Expandable at runtime

## This Project's MCP Servers
### memory-bank
- Tools: create_entities, search_nodes, read_graph
- Used by: Documenter to store learning progress

### mindmap
- Tools: convert_markdown_to_mindmap
- Used by: Documenter to generate HTML mindmaps

## Key Insight
- LLM doesn't know or care about MCP
- It just sees a list of tools with descriptions
- MCP handles the plumbing underneath
