# Orchestrator-Workers

## What It Is
- One LLM plans, others execute
- LLM decides the subtasks at runtime
- First pattern where steps aren't known in advance

## The Two Roles
### Orchestrator
- Receives high-level task
- Breaks into subtasks
- Decides number of workers
- Combines results
### Workers
- Each gets ONE subtask
- Works independently
- Returns result to orchestrator

## The Flow
- Orchestrator plans (LLM call)
- Your code parses the plan
- Your code loops and calls workers
- Orchestrator combines (LLM call)
- Structured output (JSON) is critical

## Worker Prompt Flexibility
### Level 1: Hardcoded
- Developer writes worker prompt
- Low flexibility, high control
- One use case only
### Level 2: Orchestrator Generates
- Orchestrator writes worker prompts
- High flexibility, low control
- Handles any request
### Level 3: Base + Dynamic
- Developer sets guardrails/role
- Orchestrator fills in specifics
- Most common in production
- Claude Code works this way

## The Tradeoff
- More orchestrator freedom = more general
- More orchestrator freedom = less predictable

## vs Other Patterns
- Chaining: developer decides steps, fixed
- Routing: predefined paths
- Parallelization: developer decides fan-out, fixed
- Orchestrator-Workers: LLM decides everything at runtime
