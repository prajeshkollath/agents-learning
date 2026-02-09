# Parallelization

## What It Is
- Run multiple LLM calls at the same time
- Combine results after all complete
- Lives in the orchestrator code

## Two Patterns
### Sectioning
- Each call does a different task
- Same input, different jobs
- Combine by merging results
- Why: Speed
### Voting
- Each call does the same task
- Same input, same job, multiple times
- Combine by majority vote or best-of-N
- Why: Reliability

## Key Rule
- Only parallelize independent tasks
- If B needs A's output, that's chaining

## Combining with Other Patterns
### Route then Parallelize
- Pick the path, then fan out within it
### Parallelize then Chain
- Fan out, combine, then pass to next step
### Parallelize with Gates
- Each branch has its own quality checks

## vs Other Patterns
- Chaining: sequential, steps depend on each other
- Routing: picks ONE path
- Parallelization: runs MULTIPLE paths at once
