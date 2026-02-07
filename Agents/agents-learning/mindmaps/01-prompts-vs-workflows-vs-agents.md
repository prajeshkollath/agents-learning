# Prompts vs Workflows vs Agents

## Prompt
### Single LLM call
### One input, one output
### No orchestration
### You control everything

## Workflow
### Multiple LLM calls
### Code controls the flow
#### Routing is predetermined
#### Steps are defined upfront
### Shared state between steps
### Each step gates the next
#### Validation
#### Routing
### Predictable flow

## Agent
### LLM controls the flow
### Decides next step dynamically
### Chooses tools autonomously
### Decides when to stop
### Unpredictable flow

## Who Controls the Flow?
### Prompt: Developer writes the input
### Workflow: Developer's code orchestrates
### Agent: The LLM orchestrates itself
