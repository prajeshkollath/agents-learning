# What Makes an Agent

## Three Ingredients
### Tool Use
- Can take actions in the world
- Read files, search, run code, query DBs
- Without tools, LLM can only generate text
### A Loop
- Observe → Think → Act → repeat
- Not a fixed number of iterations
- Agent decides when to stop
### Autonomy
- LLM decides what tool to use next
- LLM decides when it's done
- Code doesn't hardcode these decisions

## Agent vs Workflow
- Workflow: your code controls the flow
- Agent: the LLM controls the flow
- Orchestrator-workers was the bridge

## The Spectrum
- Pure LLM: basic chat, no tools, you drive
- LLM + tools: some agentic behavior
- Full agent: loop, tools, autonomy

## How to Get Agentic Behavior
### Pre-built agent apps
- Claude Code, Copilot, ChatGPT with tools
- Company built the loop
### Agent frameworks
- Claude Agent SDK, LangChain
- Framework built the loop, you configure
### Raw API + your code
- You build the loop yourself
- ~30-40 lines of Python
- Best for understanding internals

## Key Insights
- API alone = just an LLM, not an agent
- Adding MCP tools doesn't make something an agent
- The loop was already there, MCP adds more tools
- Build raw first, then use frameworks
