# Routing

## What It Is
- Classify input, then pick the right path
- Traffic cop — directs, doesn't do the work
- Lives in the orchestrator code

## How to Route
### LLM-Based
- Ask LLM to classify
- High accuracy, understands intent
- Costs tokens, slower
### Code-Based
- Keywords, regex, rules
- Free and instant
- Lower accuracy
### Combined
- Code checks first (cheap)
- LLM fallback if unsure (accurate)

## What You Can Route On
### Which Chain
- Billing vs Technical vs FAQ
### Which Model
- Haiku for simple (cheap)
- Sonnet for medium (balanced)
- Opus for complex (powerful)
### Which Tools
- Needs DB lookup vs no tools
### Human vs AI
- AI handles it vs escalate

## Patterns
### Nested Routing
- First router picks broad category
- Second router picks specific handler
### Routing + Gates
- Router picks which path
- Gates check quality within path

## vs Chaining
- Chaining: same path for all inputs
- Routing: different paths based on classification

## Pitfall
- Don't over-route
- Only route when paths are genuinely different
