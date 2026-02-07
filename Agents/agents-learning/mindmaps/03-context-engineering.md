# Context Engineering

## The Problem
### Limited Context Windows
- LLMs have token limits
- 200k, 500k tokens max
### Unlimited Conversations
- History grows with each turn
- Token cost increases linearly
### Result
- Eventually hit limits
- Costs become prohibitive
- Need smart management

## Core Strategies

### 1. Sliding Window
#### Definition
- Keep last N turns only
- Discard everything older
#### Analogy
- Moving camera
- Sees only current scene
- Past completely forgotten
#### When to Use
- Short-term memory sufficient
- Self-contained turns
- Predictable token costs needed
#### Trade-offs
- Simple implementation
- Fixed cost ceiling
- BUT: loses all old history
- May forget important context

### 2. Selective Retention
#### Definition
- Keep important info
- Drop filler content
- Rules-based decisions
#### Analogy
- Packing for trip
- Keep essentials
- Drop nice-to-haves
#### Approaches
##### Structured Fields
- Manual extraction
- Maintain specific data
- Name, role, preferences
- Project context
##### Pattern Matching
- Rule-based filtering
- Keep keywords: error, deadline
- Drop filler: thanks, ok
##### LLM Extraction
- Ask LLM for key facts
- Goals, requirements, decisions
- Dynamic extraction
#### When to Use
- Critical vs noise distinction
- Can define importance rules
- Need long-term memory
#### Trade-offs
- More control
- Retain critical info
- BUT: needs upfront design
- Can miss context if wrong

### 3. Summarization
#### Definition
- Compress old turns
- Keep recent turns full
- Lose detail, keep essence
#### Analogy
- Meeting notes
- Old meetings: summary
- Recent: full detail
#### How It Works
- Old turns → summary
- Recent turns → verbatim
- Balance history and detail
#### When to Use
- Long complex conversations
- Need history awareness
- Can afford summarization cost
#### Trade-offs
- Balances history + detail
- Natural approach
- BUT: loses nuance
- Extra LLM calls
- Compounds errors

## Choosing Strategy
### Decision Matrix
#### Sliding Window
- Best: short-term tasks
- Avoid: need long-term memory
#### Selective Retention
- Best: tracking specific facts
- Avoid: unknown importance upfront
#### Summarization
- Best: complex with history
- Avoid: need exact past details

## Hybrid Approaches
### Combine All Three
#### Example Structure
- Selective retention: user info, issues
- Summarization: old conversation summary
- Sliding window: last 5 turns verbatim
### Why It Works
- Structured fields: critical facts
- Summary: historical context
- Recent turns: immediate flow
### Real-World Usage
- Customer support agents
- Long-running projects
- Complex multi-turn tasks

## Implementation Architecture
### Agent Prompts
#### Purpose
- Define behavior and role
- Set tone and style
- Establish rules
#### Stays Constant
- Not part of context engineering
- System-level instruction
### Orchestrator
#### Purpose
- Manages conversation history
- Implements context strategy
- Decides what agent sees
#### Operations
- Summarize old turns
- Extract structured fields
- Apply sliding window
- Pass curated context
### Key Distinction
- Agent prompt: HOW to behave
- Orchestrator: WHAT context to see
- Engineering at orchestrator level

## Token Cost Impact
### Without Engineering
- Turn 1: 100 tokens
- Turn 2: 250 tokens
- Turn 10: 2000+ tokens
- Linear growth
### With Sliding Window
- Stabilizes after window size
- Fixed cost per turn
- Example: 450-500 tokens always
### With Summarization
- Old turns compressed
- 2000 tokens → 200 token summary
- Recent turns: full detail
- Major savings
### Bottom Line
- Direct cost control
- Enable longer conversations
- Scale sustainably
