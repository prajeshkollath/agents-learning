# The Augmented LLM

## Base LLM Limitations
### Knowledge Cutoff
#### Only knows data up to training date
#### No access to recent events
### Stateless
#### Forgets after each conversation
#### No memory of previous interactions
### Text-Only Output
#### Can't execute code
#### Can't interact with APIs
#### Can't perform actions

## The Three Pillars

### 1. Retrieval (RAG)
#### What It Solves
##### Access to current information
##### Your private documents
##### Company knowledge bases
##### Real-time data
#### How It Works
##### User asks question
##### System searches documents
##### Retrieved chunks added to prompt
##### LLM answers with context
#### Analogy
##### Open-book exam
##### Look up facts when needed

### 2. Tools (Function Calling)
#### What It Solves
##### Execute actual code
##### Check live data
##### Perform calculations
##### Interact with APIs
#### How It Works
##### LLM requests tool call
##### Your code executes it
##### Result returned to LLM
##### LLM formulates answer
#### Key Insight
##### LLM decides WHICH tool
##### Your code EXECUTES it
#### Analogy
##### Manager delegating to specialists

### 3. Memory (Persistent State)
#### What It Solves
##### Remember past conversations
##### User preferences
##### Context across sessions
#### Types
##### Short-term (current conversation)
##### Summary memory (condensed)
##### Long-term (facts, preferences)
#### How It Works
##### Store after each conversation
##### Retrieve before new conversation
##### Add to prompt
#### Analogy
##### Assistant taking notes

## Architecture

### The LLM Layer (Claude API)
#### Receives text prompt
#### Generates text response
#### Requests tool calls
#### NO direct access to data/tools/memory

### The Orchestration Layer (Your Code)
#### Manages Retrieval
##### Searches documents
##### Adds to prompt
#### Executes Tools
##### Runs actual functions
##### Returns results
#### Handles Memory
##### Stores conversations
##### Retrieves context
#### Builds Prompts
##### Combines all context
##### Calls LLM API

### Where They Live
#### Retrieval = Your infrastructure
##### Vector DB or search system
#### Tools = Your code
##### Function definitions
##### Execution logic
#### Memory = Your database
##### SQL, Redis, file system

## Claude Code Implementation

### Tools (Full)
#### Built-in Tools
##### Read, Write, Edit
##### Bash commands
##### Glob, Grep
#### MCP Servers
##### Additional tools
##### External integrations

### Retrieval (Partial)
#### On-Demand Reading
##### Claude decides when to search
##### Uses Read/Grep/Glob tools
#### Not Automatic RAG
##### No vector search
##### No passive retrieval
#### Active vs Passive
##### Active: Claude chooses to search
##### Passive: Auto-searches on every query

### Memory (Partial)
#### Session Memory
##### Automatic
##### Temporary
#### Auto Memory Directory
##### Manual writing required
##### Persists across sessions
#### MCP Memory Server
##### True persistence
##### Requires intentional use

## Agent vs Orchestrator

### Claude Code (Unified)
#### Single-Agent System
##### Orchestrator = Agent
##### CLI tool + Claude API
#### Markdown "Agents"
##### Really: structured prompts
##### Different personas
##### Same underlying agent

### Multi-Agent Systems (Separated)
#### Orchestrator Role
##### Routes requests
##### Manages shared memory
##### Coordinates agents
##### Aggregates results
#### Agent Roles
##### Specialized LLM instances
##### Different tools/contexts
##### Independent operation
#### When to Separate
##### Multiple specialists needed
##### Parallel execution
##### Different models per task

## The Agent Spectrum

### 1. Simple Prompt
#### One-shot Q&A
#### No tools
#### No autonomy

### 2. Structured Prompt
#### Behavior template
#### Still conversational
#### No tools (just text)
#### Your markdown "agents"

### 3. Workflow
#### Chained LLM calls
#### Predetermined flow
#### No autonomy

### 4. True Agent
#### Autonomous decision-making
#### Uses tools
#### Loops (observe → think → act)
#### Goal-oriented
#### Claude Code is this

## What Makes an Agent
### Autonomy
#### Decides own steps
#### Not following a script
### Tool Use
#### Can DO things
#### Acts in the world
### Loops
#### observe → think → act → repeat
#### Multiple turns to complete task
### Goal-Oriented
#### Works until task complete
#### Not just responding

## Key Takeaways

### The LLM is Just an API
#### Text in, text out
#### Stateless
#### No direct access to anything

### Augmentation is YOUR Infrastructure
#### You build (or frameworks provide)
#### Retrieval, Tools, Memory
#### Runs before/after LLM calls

### Orchestrator is the Glue
#### Manages the loop
#### Executes tools
#### Handles context

### Two Architectures
#### Unified (Claude Code)
##### Orchestrator = Agent
#### Separated (Multi-Agent)
##### Orchestrator manages multiple agents
