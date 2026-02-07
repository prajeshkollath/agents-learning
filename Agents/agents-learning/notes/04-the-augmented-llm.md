# 04 - The Augmented LLM

**Topic:** Retrieval, tools, memory as add-ons to a base LLM

---

## The Core Problem

A **base LLM** is like a brilliant professor stuck in a jar:
- Has knowledge only up to its training cutoff date
- Can't access current information or your private documents
- Can only generate text, can't DO anything (run code, check APIs, send emails)
- Forgets everything after each conversation (stateless)

An **augmented LLM** = Base LLM + external capabilities to overcome these limitations.

---

## The Three Pillars of Augmentation

### 1. Retrieval (RAG - Retrieval Augmented Generation)

**What it solves:** LLM doesn't know about:
- Recent events (after training cutoff)
- Your company's internal documents
- Your personal files
- Current codebase state

**How it works:**
1. User asks a question
2. System searches relevant documents/database
3. Retrieved information is added to the prompt
4. LLM answers based on retrieved context

**Analogy:** Open-book exam - look up specific facts when needed instead of memorizing everything.

**Example:**
```
User: "What's in our Q4 sales report?"
→ System retrieves Q4 sales document
→ Adds to prompt
→ LLM answers with actual Q4 data
```

---

### 2. Tools (Function Calling / Tool Use)

**What it solves:** LLMs can only generate text. They can't:
- Execute actual code
- Check live data (weather, stock prices)
- Perform calculations reliably
- Interact with APIs or databases

**How it works (Two round-trips):**
1. User asks question requiring a tool
2. LLM requests tool call (e.g., "call calculator.multiply(4789, 8921)")
3. **Your code executes the tool** and returns result
4. LLM receives result and formulates final answer

**Analogy:** Manager delegating to specialists - can't do everything yourself, so delegate to tools.

**Key insight:** The LLM decides WHICH tool to call and WITH WHAT parameters, but YOUR CODE executes it.

---

### 3. Memory (Persistent State)

**What it solves:** Base LLMs are stateless - don't remember:
- Previous conversations
- User preferences
- Context from past sessions

**Types of memory:**
- **Short-term:** Current conversation history
- **Summary memory:** Condensed version of long conversations
- **Long-term:** Facts about user, preferences, key decisions

**How it works:**
1. After each conversation, store important information in a database
2. Before new conversation, retrieve relevant memory
3. Add memory to the prompt

**Analogy:** Personal assistant who takes notes during meetings and reviews them before the next meeting.

---

## Where Do These Components Live?

### System Architecture

```
┌─────────────────────────────────────┐
│    YOUR APPLICATION (Orchestrator)  │
│  ┌────────┐ ┌────────┐ ┌────────┐  │
│  │Retrieval│ │ Tools  │ │Memory  │  │
│  │ System │ │ System │ │System  │  │
│  └───┬────┘ └───┬────┘ └───┬────┘  │
│      │          │          │        │
│      └──────────┴──────────┘        │
│               ▼                     │
│        [Prompt Builder]             │
│               ▼                     │
└───────────────┼─────────────────────┘
                │ API Call
                ▼
     ┌──────────────────┐
     │   Claude API     │
     │  (Just the brain)│
     └──────────────────┘
```

### Key Understanding

**The LLM (Claude API):**
- Receives text prompt
- Generates text response
- Can REQUEST tool calls
- Has NO direct access to your data/tools/memory

**The Orchestration Layer (Your Code):**
- Manages retrieval (searches documents before calling LLM)
- Executes tools (runs actual functions when LLM requests them)
- Stores/retrieves memory (database operations)
- Builds the prompt with all context

**Crucial distinction:**
- LLM = The "brain" that thinks and decides
- Orchestrator = The "body" that acts in the world
- Retrieval/Tools/Memory = Infrastructure YOU build (or frameworks provide)

---

## Claude Code as an Augmented LLM

### How Claude Code Implements the Three Pillars

| Feature | Implementation | Type |
|---------|---------------|------|
| **Tools** | ✅ Built-in (Read, Write, Edit, Bash, Grep, Glob) + MCP servers | Full |
| **Retrieval** | ⚠️ On-demand file reading (Claude decides when to search) | Partial |
| **Memory** | ⚠️ Session memory + auto memory directory + MCP memory | Partial |

**Tools (Full Implementation):**
- Read, Write, Edit files
- Bash commands
- Glob (find files), Grep (search content)
- MCP servers for additional tools
- This is Claude Code's strength

**Retrieval (Partial - Active, not Passive):**
- No automatic RAG/vector search
- Claude uses Read/Grep/Glob tools to search when needed
- More intelligent (decides when to search) but requires thinking
- Not passive background retrieval

**Memory (Partial - Requires Intentional Use):**
- Session memory: automatic but temporary
- Auto memory directory: manual writing required
- MCP memory-bank: true persistence across sessions

**Claude Code = Orchestration Layer**
- It's the "application code" that manages tools, context, API calls
- The agent system that wraps Claude API

---

## Markdown "Agents" - What They Really Are

### Not Agents, But Agent Prompts

Your markdown files (planner.md, tutor.md, evaluator.md):
- ❌ NOT separate agent instances
- ✅ Structured prompts / behavior templates / personas
- ✅ Loaded into system prompt to guide behavior

**How they work:**
```
You: "Use the tutor agent"
→ Claude Code loads tutor.md into system prompt
→ Claude behaves according to tutor instructions
→ Still the same LLM, just different behavior
```

**They are:**
- Prompt engineering (structured prompts)
- Role definitions
- Operating procedures

**Analogy:**
- Claude Code = A human employee
- Markdown files = Job descriptions/instruction manuals
- The employee (agent) follows different job descriptions (personas)

---

## The Agent Spectrum

### 1. Simple Prompt
- One-shot question and answer
- No tools, no autonomy

### 2. Structured Prompt (Your markdown "agents")
- Follows a behavior template
- Still one conversation
- No tools (just text)

### 3. Workflow
- Multiple LLM calls chained together
- Predetermined flow
- No autonomy

### 4. Agent (Claude Code)
- **Autonomous** - decides its own steps
- **Uses tools** - can DO things in the world
- **Loops** - observe → think → act → repeat
- **Goal-oriented** - works until task complete

**What Makes Claude Code an Agent:**
- ✅ Has tools (file operations, bash, MCP)
- ✅ Can loop autonomously (multiple turns)
- ✅ Makes decisions (which tool to use, what to do next)
- ✅ Goal-oriented (works toward completing tasks)

---

## Orchestrator vs Agent

### In Claude Code (Unified System)

**Claude Code = Orchestrator + Agent combined**

```
Claude Code (The System)
├─ Orchestrator layer (CLI tool)
│  ├─ Manages conversation loop
│  ├─ Executes tools
│  ├─ Handles context/memory
│  └─ Routes to MCP servers
└─ Agent brain (Claude API)
   └─ Makes decisions, requests actions
```

- Single-agent system
- Orchestrator and agent are unified
- Markdown files = different personas for the same agent

### In Multi-Agent Systems (Separated)

**Orchestrator ≠ Agents**

```
Orchestrator (Your Code - Manager)
├─ Routes user requests
├─ Manages shared memory
├─ Coordinates between agents
├─ Aggregates results
│
├─→ Agent 1 (LLM instance - Researcher)
├─→ Agent 2 (LLM instance - Coder)
└─→ Agent 3 (LLM instance - Tester)
```

**When to separate:**
- Multiple specialized agents needed
- Each agent has different tools/context
- Parallel execution required
- Complex routing logic
- Different models for different tasks

**Example: Customer Support System**
```python
class Orchestrator:
    def handle_request(self, message):
        intent = self.routing_agent.classify(message)

        if intent == "order_issue":
            response = self.order_agent.handle(message)

            if response.needs_escalation:
                response = self.manager_agent.handle(message)

        self.shared_memory.store(message, response)
        return response
```

- Orchestrator = Your Python code managing the flow
- Agents = Separate LLM instances with specialized prompts

---

## Key Distinctions

### Retrieval vs Tools vs Memory

| Capability | What It Does | Example |
|-----------|-------------|---------|
| **Retrieval** | Brings external information INTO the prompt | "Here's what your wiki says..." |
| **Tools** | Lets LLM DO things in external world | "I've sent the email" |
| **Memory** | Preserves information ACROSS conversations | "As we discussed last Tuesday..." |

### Orchestrator in Different Systems

| System Type | Orchestrator Role | Agent Role |
|------------|------------------|-----------|
| **Single-agent** (Claude Code) | Built-in, unified with agent | The whole system |
| **Multi-agent** (Production) | Separate manager code | Individual LLM instances |

---

## Common Misconceptions

### ❌ "The LLM searches the internet and remembers everything on its own"

**Reality:**
- LLM doesn't search or remember autonomously
- Orchestration layer handles retrieval and memory
- LLM receives retrieved info in context
- LLM requests tools but doesn't execute them

### ❌ "Markdown agents are separate AI instances"

**Reality:**
- They're structured prompts/personas
- Same Claude instance, different behavior
- Loaded into system prompt, not separate agents

### ❌ "Claude Code has full RAG like production systems"

**Reality:**
- Has on-demand file reading (active retrieval)
- No automatic vector search/semantic retrieval
- Claude decides when to search using tools

---

## What's Next

**Phase 2:** Learn workflow patterns (chaining, routing, parallelization)
**Phase 3:** Deep dive into agent loops and building agents in Claude Code
**Phase 4:** Build retrieval, tools, and memory systems from scratch in Python
**Phase 6:** Build multi-agent systems with separated orchestrators

---

[← Back to ROADMAP](../ROADMAP.md)
