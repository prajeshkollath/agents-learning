# Prompt Engineering

## System Prompts
### Definition
- Sets role, rules, context before user input
### Purpose
- Shape behavior and tone
- Assign role/persona
- Set input/output format
- Establish rules
### Analogy
- Like briefing an actor before stage
### Location
- Part of conversation context
- Invisible to user
- In Claude Code: agent files

## Few-Shot Prompting
### Definition
- Give examples of desired pattern
- LLM learns and follows pattern
### Types
- Zero-shot: no examples
- One-shot: 1 example
- Few-shot: 2-5 examples
### When to Use
- Need specific output format
- Edge cases better shown than explained
- Inconsistent zero-shot results
### Where Examples Go
- System prompt: for consistency
- User prompt: for flexibility
### Trade-off
- More examples = better accuracy
- More examples = higher token cost

## Chain-of-Thought
### Definition
- LLM shows reasoning steps
- Before final answer
### Analogy
- Like showing work in math class
### How to Trigger
- Zero-shot: "think step-by-step"
- Few-shot: show reasoning examples
### LLM Control
- You control: whether to use CoT
- LLM controls: how it reasons
- Uses own judgment, not your exact steps
### Output
- Default: reasoning + answer visible
- Optional: only final answer
### When to Use
- Math and logic problems
- Multi-step reasoning
- Need verifiable logic
- Costly mistakes possible

## Combining Techniques
### Power Move
- System prompt: set role and rules
- Few-shot: show example patterns
- Chain-of-thought: request reasoning
### Result
- Consistent behavior
- Specific format
- Verifiable logic

## Token Costs
### Stateless LLMs
- Every call sends full context
- Even in conversations
### Token Growth
- Turn 1: System + Q1
- Turn 2: System + Q1 + A1 + Q2
- Turn N: System + all history + Qn
### Reduction Strategies
- Summarization
- Sliding window
- Selective retention
- Smart truncation
