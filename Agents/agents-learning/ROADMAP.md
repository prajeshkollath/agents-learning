# Agents & Workflows Learning Roadmap

> **Principle:** Build it raw first, understand the internals, then use frameworks.
> **Progression:** Concepts → Claude Code → Raw Python → Frameworks
> **Teaching note:** During Phase 4, each raw Python concept will be mapped to its framework equivalent in Pydantic AI, LangGraph, and Google ADK — so you see raw internals and framework abstractions side by side.
> **Phase 4 API:** Exercises use the Gemini API (google-genai SDK) via Google AI Studio free tier (Gemini 2.0 Flash). This also prepares directly for Google ADK in Phase 7.

---

## Phase 1: Foundations (Concepts Only)
- [x] 01 - Prompts vs Workflows vs Agents
- [x] 02 - Prompt engineering - system prompts, few-shot, chain-of-thought
- [x] 03 - Context engineering - what goes in the window, what stays out, token management
- [x] 04 - The augmented LLM - retrieval, tools, memory as add-ons to a base LLM

## Phase 2: Workflow Patterns (Concepts + Claude Code Exercises)
- [x] 05 - Prompt chaining - output of one becomes input of next
- [x] 06 - Routing - classifying input to pick the right path
- [x] 07 - Parallelization - running LLM calls simultaneously, then combining
- [x] 08 - Orchestrator-workers - one LLM plans, others execute
- [x] 09 - Evaluator-optimizer - one generates, another critiques in a loop

## Phase 3: Agents in Claude Code
- [x] 10 - What makes an agent (tool use, loops, autonomy)
- [x] 11 - Agent loops & workflows - observe → think → act → repeat
- [x] 12 - MCP servers as agent tools
- [x] 13 - Building simple agents via Claude Code configuration
- [x] 14 - State & memory - conversation history, summaries, persistent memory

## Phase 4: Python - Raw Building Blocks (No Frameworks)
- [ ] 15 - Claude API basics - raw SDK calls
- [ ] 16 - Prompt caching - cache_control, cost reduction, when and how to cache
- [ ] 17 - Context window management - truncation, sliding window, auto-summarize (silent + prompted)
- [ ] 18 - Building a prompt chain in Python
- [ ] 19 - Building a workflow with routing in Python
- [ ] 20 - State management - passing context between steps
- [ ] 21 - Memory engineering - conversation memory, summary memory, vector/RAG basics
- [ ] 22 - Building an agent loop from scratch in Python
- [ ] 23 - Tool use with the Claude API

## Phase 5: Guardrails & Evals (Python)
- [ ] 24 - Input guardrails - validation, injection detection, content filtering
- [ ] 25 - Output guardrails - format checking, hallucination detection, safety
- [ ] 26 - Evals - how to measure agent quality, benchmarking, test suites
- [ ] 27 - Error handling & fallbacks in agent systems

## Phase 6: Multi-Agent Systems (Python)
- [ ] 28 - Multi-agent patterns - delegation, debate, specialization
- [ ] 29 - Shared state between agents
- [ ] 30 - Handoffs and coordination

## Phase 7: Frameworks (Only After Understanding the Internals)
- [ ] 31 - Pydantic AI - type-safe agents, Python-native, lightweight framework
- [ ] 32 - Google ADK (Agent Development Kit) - Google's agent framework, Gemini-native
- [ ] 33 - LangChain / LangGraph overview - graph-based stateful workflows
- [ ] 34 - When to use which framework - decision guide

---

*Topics will be added as we go along.*
