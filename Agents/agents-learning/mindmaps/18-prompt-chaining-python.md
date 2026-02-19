# Building a Prompt Chain in Python

## Building Block
### One helper function: call_gemini(system, user)
### Each call is independent, single-turn
### No conversation history between steps
### The chain is in Python, not in the model

## Each Step Gets Its Own System Prompt
### System prompt = job description (persona)
### User message = today's task (input)
### Different persona per step (writer, critic, editor)
### Reusable across pipelines

## Data Flow Between Steps
### f-string glue: output of one → input of next
### Later steps can use ANY earlier output (not just previous)
### All intermediate results are Python variables

## Gates (Programmatic Checks)
### Pure Python, no LLM call
### Gate after steps where failure wastes downstream tokens
### Count gate: enough items extracted?
### JSON gate: valid parseable output?
### Gate fails → chain stops immediately

## Four Patterns
### Simple chain: call → call → call
### Gated chain: call → gate → call
### Multi-input step: step3 uses step1 + step2 output
### JSON gate: structured output + validation

## Why Not One Big Prompt?
### Can't inspect intermediate results
### Can't add quality checks mid-process
### Can't swap models per step
### Role confusion (writer vs critic)

## Why Not Multi-Turn?
### Context window grows across steps
### No programmatic control between steps
### Each step only needs specific input, not full history

## Error Handling
### Fail fast: stop and report which step failed
### Retry: re-run failed step with modified prompt
### Key advantage: know exactly WHERE things broke
