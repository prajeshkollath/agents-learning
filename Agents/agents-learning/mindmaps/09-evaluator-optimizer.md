# Evaluator-Optimizer

## What It Is
- One LLM generates, another critiques
- Loop until output is good enough
- Writer and editor analogy

## The Two Roles
### Generator
- Produces initial output
- Revises based on feedback
### Evaluator
- Reviews against criteria
- Gives specific actionable feedback
- Decides when to stop

## vs Gates
- Gate: pass/fail, binary, code-based
- Evaluator: qualitative feedback, LLM-based
- Gate retries blindly, evaluator says what to fix

## Separate Call, Not Separate Model
- Same model works fine (e.g. Sonnet for both)
- Key: different prompt, fresh context
- Avoids anchoring bias from self-critique
### Can Mix Models
- Cheap generator + smart evaluator (save cost)
- Smart generator + cheap evaluator (easy checks)

## Critical: Max Iterations
- Always set a limit
- Without it, loop runs forever

## Use Cases
- Code generation and review
- Writing drafts and revision
- Translation and back-translation
- Data extraction and verification

## Phase 2 Complete: All 5 Patterns
- Chaining: sequential
- Routing: branching
- Parallelization: fan-out
- Orchestrator-Workers: dynamic planning
- Evaluator-Optimizer: feedback loop
