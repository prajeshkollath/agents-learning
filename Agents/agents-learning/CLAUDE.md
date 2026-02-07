# Agents & Workflows Learning Project

## Project Overview
This is a hands-on learning project for understanding AI agents, workflows, prompts, context engineering, guardrails, and evals. The learner (Prajesh) builds understanding from fundamentals to frameworks.

## Repository
**GitHub:** https://github.com/prajeshkollath/agents-learning.git

## Principle
Build it raw first, understand the internals, then use frameworks.
Progression: Concepts → Claude Code → Raw Python → Frameworks.

## Learning Roadmap
See [ROADMAP.md](ROADMAP.md) for the full 31-topic, 7-phase plan.

## Project Structure
```
agents-learning/
  ROADMAP.md           - Learning roadmap with progress tracking
  LEARNING-GUIDE.md    - How to use notes, mindmaps, and diagrams effectively
  agents/              - Agent prompt files (Planner, Tutor, Evaluator, Documenter)
  notes/               - Detailed study notes per topic
  mindmaps/            - Markdown mindmaps (for MCP conversion)
  diagrams/            - Mermaid diagrams
  code/                - Exercises and code built while learning
```

## Agent System

This project uses 4 agents that form a learning cycle:

```
Planner → Tutor → Evaluator ─┐
   ↑                          │
   └──── (gaps found) ────────┘

Documenter captures everything throughout
```

### Agents
- **Planner** (`agents/planner.md`) - Plans topics, creates roadmaps, sequences learning
- **Tutor** (`agents/tutor.md`) - Teaches concepts simply, uses analogies and examples
- **Evaluator** (`agents/evaluator.md`) - Tests understanding, identifies gaps
- **Documenter** (`agents/documenter.md`) - Creates notes, diagrams, mindmaps

### How to Use
Invoke an agent by saying:
- "Use the planner agent" or "Act as planner"
- "Use the tutor agent" or "Teach me about X"
- "Use the evaluator agent" or "Quiz me on X"
- "Use the documenter agent" or "Document what we learned"

### Shared Context
All agents should read:
1. `ROADMAP.md` for current progress
2. `notes/` for what has been documented
3. The current conversation for recent discussion

### Rules
- The Tutor only teaches topics the Planner has queued
- The Evaluator reports gaps back so the Planner can adjust
- The Documenter only records the learner's own understanding, not generic content
- No web research unless the learner explicitly asks for it
- Start simple, add complexity only when the learner is ready

### Agent Invocation Guidelines
- **Always let agents follow their own prompts** - When invoking an agent, avoid overriding their defined behavior with specific instructions that conflict with their prompt
- **Agent prompts define behavior** - Each agent's markdown file defines what it should do. Let it follow that checklist/workflow
- **Updating agent behavior** - If the user requests additional work or different behavior from an agent:
  1. First, check if it makes sense to add to the agent's prompt for future consistency
  2. Ask the user: "Should we update the [agent name] agent's prompt to include this for future interactions?"
  3. Only add ad-hoc instructions if it's a one-time exception
- **Consistency over customization** - Better to have well-defined agent prompts than to customize behavior on each invocation
