# Agents & Workflows Learning Roadmap

> **Principle:** Build it raw first, understand the internals, then use frameworks.
> **Progression:** Concepts → Claude Code → Raw Python → Frameworks

---

## Phase 1: Foundations (Concepts Only)
- [x] 01 - Prompts vs Workflows vs Agents
- [x] 02 - Prompt engineering - system prompts, few-shot, chain-of-thought
- [x] 03 - Context engineering - what goes in the window, what stays out, token management
- [x] 04 - The augmented LLM - retrieval, tools, memory as add-ons to a base LLM

## Phase 2: Workflow Patterns (Concepts + Claude Code Exercises)
- [x] 05 - Prompt chaining - output of one becomes input of next
- [ ] 06 - Routing - classifying input to pick the right path
- [ ] 07 - Parallelization - running LLM calls simultaneously, then combining
- [ ] 08 - Orchestrator-workers - one LLM plans, others execute
- [ ] 09 - Evaluator-optimizer - one generates, another critiques in a loop

## Phase 3: Agents in Claude Code
- [ ] 10 - What makes an agent (tool use, loops, autonomy)
- [ ] 11 - Agent loops & workflows - observe → think → act → repeat
- [ ] 12 - MCP servers as agent tools
- [ ] 13 - Building simple agents via Claude Code configuration
- [ ] 14 - State & memory - conversation history, summaries, persistent memory

## Phase 4: Python - Raw Building Blocks (No Frameworks)
- [ ] 15 - Claude API basics - raw SDK calls
- [ ] 16 - Building a prompt chain in Python
- [ ] 17 - Building a workflow with routing in Python
- [ ] 18 - State management - passing context between steps
- [ ] 19 - Memory engineering - conversation memory, summary memory, vector/RAG basics
- [ ] 20 - Building an agent loop from scratch in Python
- [ ] 21 - Tool use with the Claude API

## Phase 5: Guardrails & Evals (Python)
- [ ] 22 - Input guardrails - validation, injection detection, content filtering
- [ ] 23 - Output guardrails - format checking, hallucination detection, safety
- [ ] 24 - Evals - how to measure agent quality, benchmarking, test suites
- [ ] 25 - Error handling & fallbacks in agent systems

## Phase 6: Multi-Agent Systems (Python)
- [ ] 26 - Multi-agent patterns - delegation, debate, specialization
- [ ] 27 - Shared state between agents
- [ ] 28 - Handoffs and coordination

## Phase 7: Frameworks (Only After Understanding the Internals)
- [ ] 29 - Claude Agent SDK
- [ ] 30 - LangChain / LangGraph overview
- [ ] 31 - When to use frameworks vs raw code

---

*Topics will be added as we go along.*
