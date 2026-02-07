# Prompt Chaining

## What It Is
### Multiple sequential LLM calls
### Output of one becomes input of next
### Chain lives in YOUR CODE, not in the LLM

## Why Chain Instead of One Prompt
### Each step is focused and verifiable
### Easy to debug — inspect output at each step
### Can add gates between steps

## The Pattern
### Input → LLM Call 1 → Output 1
### Output 1 → LLM Call 2 → Output 2
### Output 2 → LLM Call 3 → Final Output

## Gates (Checkpoints)
### Programmatic checks between steps
### Not LLM calls — pure code
### Decide: continue, stop, or retry
### Quality control without burning tokens

## Where It Lives
### Orchestrator code calls LLM multiple times
### Passes outputs forward
### Runs gate checks
### LLM has no idea it's part of a chain

## vs Few-Shot
### Few-shot: ONE call, examples inside prompt
### Chaining: MULTIPLE calls wired together in code
### Can use few-shot inside a chain step

## vs Agent Loops
### Chain: Fixed predetermined steps
### Agent: Dynamic, LLM decides next step
### Chain = workflow, Agent = autonomy
