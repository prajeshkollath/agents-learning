# Building Simple Agents

## The Three Layers
### Loop
- while stop_reason != end_turn
- ~10 lines of code
- Feeds results back into next API call

### Tool Definitions + Executor
- Python functions (what tools do)
- JSON schemas (how LLM knows to call them)
- The real work of building an agent

### System Prompt
- Role, rules, behavior
- Grants autonomy: "go figure it out"
- Claude Code: agents/*.md files

## Claude Code vs Raw Python
### Claude Code
- Loop: built in
- Tools: MCP servers + built-in
- Prompt: markdown files
- You only configure behavior

### Raw Python
- Loop: you write it
- Tools: Python functions + JSON schemas
- Prompt: system= string
- You build the full runtime

## Agent vs Chatbot Prompt
### Chatbot
- Answer this question
- One turn
- No tools, no loop

### Agent
- Here's a goal + tools + rules
- Multi-turn loop
- Grants autonomy to decide steps

## Claude Code Configuration
### CLAUDE.md
- Always loaded
- Project-wide context and rules

### agents/*.md files
- Loaded on demand
- Role-specific behavior
- Role, Responsibilities, Rules, Handoff

## Framework Landscape
### Pydantic AI
- Type-safe, Python-native
- Lightweight
- Clean DX

### Claude Agent SDK
- Anthropic-made
- Claude-native handoffs
- Multi-agent support

### LangGraph
- Graph-based workflows
- Stateful
- Most complex

## Why Raw Python First
- All frameworks hide the same 3 layers
- Can't debug what you can't see
- Foundation before abstraction
