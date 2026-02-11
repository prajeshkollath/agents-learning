# Agent Loops & Workflows

## The Agent Loop
### Observe
- Receive input: user request, tool results, errors
- This is what the LLM sees each turn
### Think
- Reason about what to do next
- Chain-of-thought generation
### Act
- Pick a tool and call it
- Reach out into the world
### Repeat or Stop
- Loop back to Observe with tool result
- Or return final answer if done

## How It Works (API Level)
### The stop_reason signal
- tool_use → agent has more work, keep looping
- end_turn → agent is done, stop
### The loop is ~10 lines of code
- Call API, check stop_reason, execute tool, feed result back
### Messages grow each iteration
- Assistant response + tool result appended every turn

## ReAct Pattern
### Reasoning + Acting
- The formal name for this loop
### Each turn is explicit
- Thought: what I'm thinking
- Action: what tool I'm using
- Observation: what I got back
### Claude Code uses ReAct
- You can see it reasoning before each tool call

## Stop Conditions
### Task complete
- LLM decides it's done (end_turn)
### Max iterations
- Hard limit in your code — always set one
### Context window full
- No room for more reasoning
### Error threshold
- Too many consecutive failures
### User cancels
- User intervenes and redirects

## Agent Loop vs Workflows
### Workflows (05-09)
- Code controls the loop
- Steps known upfront
- Predictable, reliable
### Orchestrator-Workers (08)
- The bridge between workflow and agent
- LLM plans, but code still runs the loop
### Agent Loop (11)
- LLM controls the loop
- Steps NOT known upfront
- Flexible, exploratory
### Combine both
- Agent loop at top level
- Uses workflow patterns inside each turn
- Chain, parallelize, evaluate as needed

## Common Pitfalls
- No max iterations → loops forever
- Too many tools → LLM confused about which to pick
- No error handling → retries same failure endlessly
- Context bloat → large tool results eat the window
- Overusing agents → use a workflow if steps are known
