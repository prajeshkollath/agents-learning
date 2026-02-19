# Topic 18: Building a Prompt Chain in Python

## Core Concept

A prompt chain is a **fixed sequence of LLM calls** where your Python code passes the output of one call as input to the next. The LLM has no idea it's part of a chain — each call is independent, single-turn, fresh context. The chain, the gates, the data flow — all live in your code, not in the model.

This topic takes the concept from Topic 5 and implements it for real with the Gemini API.

---

## The Building Block: One Helper Function

Every chain is built from one reusable function:

```python
def call_gemini(system_prompt, user_message):
    response = client.models.generate_content(
        model=MODEL,
        config={"system_instruction": system_prompt},
        contents=user_message,
    )
    return response.text
```

The chain is just **repeated calls to this function** with different system prompts and different inputs. The glue between steps is f-strings.

---

## Each Step Gets Its Own System Prompt

Different persona per step, different instructions — same model:

| Step | Persona | Job |
|---|---|---|
| Extract | Content strategist | Identify key points |
| Draft | Blog writer | Write from key points |
| Critique | Senior editor | Find weaknesses |
| Polish | Senior writer | Rewrite with feedback |

**Why separate system prompts, not just different user prompts?**
- System prompt = job description (defines capability, reusable across pipelines)
- User message = today's task (the specific input)
- Keeps personas focused — the critic won't accidentally start rewriting

---

## Each Call is Independent (Not Multi-Turn)

```
Step 1: [System: Extract] + [User: topic]        → key_points
Step 2: [System: Draft]   + [User: key_points]    → draft
Step 3: [System: Critique]+ [User: draft]          → critique
Step 4: [System: Polish]  + [User: draft+critique] → final
```

No conversation history carried between steps. Each call starts from scratch. This means:
- No context window growth across the chain
- Can swap models per step if needed
- No role confusion ("am I the writer or the critic?")
- Full programmatic control between steps

---

## Gates: Programmatic Checks Between Steps

A gate is a **pure Python check** (no LLM call) between steps. If it fails, the chain stops — no wasted tokens on downstream steps.

### When to Gate

**Rule 1:** Gate after any step whose failure would waste expensive downstream work.

**Rule 2:** Gate where you can check programmatically — count items, validate JSON, check length, regex match.

If you need an LLM to judge quality, that's an eval (Topic 26), not a gate.

### Gate Examples from the Code

**Count gate:** Check that extraction produced enough key points:
```python
if point_count < 2:
    return "Chain stopped: extraction failed"
```

**JSON gate:** Validate that structured output is parseable:
```python
try:
    metadata = json.loads(cleaned)
except json.JSONDecodeError:
    return "Chain stopped: invalid JSON"
```

The JSON gate also handled markdown fencing (```` ```json ... ``` ````) that the model added despite instructions — a common real-world issue.

---

## Multi-Input Steps

Later steps can receive output from **any earlier step**, not just the previous one. All intermediate results are Python variables:

```python
# Step 4 gets output from BOTH step 2 and step 3
final = call_gemini(POLISH_SYSTEM,
    f"Original draft:\n{draft}\n\nEditor feedback:\n{critique}")
```

The critic only saw the draft (intentionally — the draft should stand on its own). The polisher saw both the draft and critique. You control exactly what each step sees.

---

## Four Patterns

| Pattern | Structure | Use case |
|---|---|---|
| Simple chain | call → call → call | Quick pipelines, prototyping |
| Gated chain | call → gate → call → call | Production pipelines with quality checks |
| Multi-input step | step3 uses output from step1 + step2 | Steps needing broader context |
| JSON gate | call(→JSON) → json.loads() → call | Structured data passing between steps |

---

## Error Handling

When one step fails, the chain stops and reports **which step** failed. This is a key advantage over one mega-prompt — with a single prompt, you have no idea where things went wrong.

Two approaches:
- **Fail fast** (what we built): Return error immediately
- **Retry**: Try the failed step again, possibly with a modified prompt

---

## From the Code Run

The 4-step blog pipeline produced:
1. **Extract**: 4 specific key points (accuracy, cost, debuggability, modularity)
2. **Gate**: Passed (4 >= 2)
3. **Draft**: A complete blog post covering all points
4. **Critique**: 5 specific improvements (add concrete example, acknowledge cost tradeoff, better analogy, split dense paragraph, mention tools)
5. **Polish**: Rewrote incorporating all 5 critiques — added a concrete prompt example, acknowledged the cost nuance, split the modularity section out

The critique → polish cycle is where chaining really shines. One model wrote it, another found weaknesses, then the final version addressed every weakness. No single prompt could reliably do all three roles.

---

## Connection to Other Topics

- **Topic 5**: The concept — now implemented in code
- **Topic 15**: The Gemini API calls are the building blocks
- **Topic 17**: Each step is a fresh call, so no context window concern per step
- **Topic 19 (next)**: Routing adds conditional paths — output determines which step runs next
- **Topic 20**: State management — using a dictionary to organize intermediate results across steps

---

[← Back to ROADMAP](../ROADMAP.md)
