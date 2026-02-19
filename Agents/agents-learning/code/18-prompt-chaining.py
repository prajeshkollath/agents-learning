# =============================================================================
# TOPIC 18: Building a Prompt Chain in Python
# =============================================================================
#
# HOW TO RUN:
#   1. pip install google-genai
#   2. Set your API key: set GEMINI_API_KEY=your_key  (Windows)
#                        export GEMINI_API_KEY=your_key (Mac/Linux)
#   3. Run: python 18-prompt-chaining.py
#
# WHAT THIS COVERS:
#   - Building a multi-step LLM pipeline where output flows from step to step
#   - Each step gets its own system prompt (persona/role)
#   - Gates: programmatic checks between steps (no LLM needed)
#   - Passing multiple earlier outputs to a later step
#   - Error handling: fail fast when a step breaks
#
# KEY INSIGHT:
#   A prompt chain is a FIXED sequence of LLM calls stitched together by YOUR
#   code. The LLM has no idea it's part of a chain — each call is independent.
#   The chain, the gates, the data flow — all of that lives in Python, not in
#   the model.
#
# FRAMEWORK EQUIVALENTS:
#   - LangChain: LCEL chains (prompt | model | parser), RunnableSequence
#   - LangGraph: Linear graph with nodes for each step, edges between them
#   - Pydantic AI: You write functions that call agent.run() sequentially
#   - Google ADK: SequentialAgent — runs a list of sub-agents in order
#
# =============================================================================

import os
from google import genai

# --- Setup -------------------------------------------------------------------

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL = "gemini-2.0-flash"


# =============================================================================
# HELPER: Single LLM call with a system prompt
# =============================================================================
# This is the building block of every chain. One function that takes a
# system prompt (the role) and a user message (the task), makes one API call,
# and returns the text response.
#
# Every step in a chain is just a call to this function with different prompts.
# The chain is NOT in the model — it's in the Python code that calls this
# function repeatedly and passes outputs forward.

def call_gemini(system_prompt, user_message):
    """Make a single Gemini API call with a system prompt and user message."""
    response = client.models.generate_content(
        model=MODEL,
        config={"system_instruction": system_prompt},
        contents=user_message,
    )
    return response.text


# =============================================================================
# EXAMPLE 1: Simple 2-Step Chain (No Gate)
# =============================================================================
# The simplest possible chain: Step 1 produces output, Step 2 uses it.
# No gate, no error handling — just to see the basic pattern.
#
# Chain: Extract key points → Write a summary from those points
#
# Why two steps instead of one "extract and summarize" prompt?
# Because the extract step's output is INSPECTABLE. If the key points are
# wrong, you know the problem is in step 1, not step 2. With one big prompt,
# you'd have no idea where things went wrong.

print("=" * 70)
print("EXAMPLE 1: Simple 2-Step Chain")
print("=" * 70)

# Each step has its own system prompt — its own "job description"
EXTRACT_SYSTEM = (
    "You are a content analyst. Given a topic, list 3-4 key points that "
    "should be covered in a short article. Output ONLY a numbered list of "
    "key points, nothing else."
)

SUMMARIZE_SYSTEM = (
    "You are a concise writer. Given a list of key points about a topic, "
    "write a 2-3 sentence summary that covers all the points. Output ONLY "
    "the summary paragraph."
)

topic = "Why Python is popular for AI development"

# Step 1: Extract key points
print(f"\nInput topic: {topic}")
print("\n--- Step 1: Extract Key Points ---")
key_points = call_gemini(EXTRACT_SYSTEM, f"Topic: {topic}")
print(key_points)

# Step 2: Summarize those points
# The output of step 1 (key_points) becomes the INPUT to step 2.
# This is the core mechanic of prompt chaining — f-string glue.
print("--- Step 2: Write Summary from Key Points ---")
summary = call_gemini(
    SUMMARIZE_SYSTEM,
    f"Topic: {topic}\n\nKey points:\n{key_points}"
)
print(summary)

# Notice: Step 2 gets BOTH the original topic AND step 1's output.
# This is common — later steps often need context from multiple earlier steps.


# =============================================================================
# EXAMPLE 2: Chain with a Gate
# =============================================================================
# Now we add a GATE — a programmatic check between steps. If the gate fails,
# the chain stops. No wasted API calls on downstream steps.
#
# Chain: Extract points → GATE (did we get enough?) → Draft blog post
#
# GATE PRINCIPLE: Gates are pure Python. No LLM call. They check things you
# can verify with code: count items, check format, validate length, parse JSON.
# If you need an LLM to judge quality, that's an eval (Topic 26), not a gate.

print("\n" + "=" * 70)
print("EXAMPLE 2: Chain with a Gate")
print("=" * 70)


def count_points(text):
    """Gate function: count numbered items in the extracted key points."""
    # Look for lines starting with a number (1. xxx, 2. xxx, etc.)
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    numbered = [line for line in lines if line and line[0].isdigit()]
    return len(numbered)


DRAFT_SYSTEM = (
    "You are a blog writer. Given a topic and key points, write a short "
    "blog post (3-4 paragraphs). Use a conversational, engaging tone. "
    "Make sure every key point is covered."
)

topic2 = "How prompt chaining makes LLM applications more reliable"

# Step 1: Extract
print(f"\nInput topic: {topic2}")
print("\n--- Step 1: Extract Key Points ---")
key_points2 = call_gemini(EXTRACT_SYSTEM, f"Topic: {topic2}")
print(key_points2)

# GATE: Check that we got at least 2 key points
point_count = count_points(key_points2)
print(f"\n--- Gate: Checking key point count ---")
print(f"Found {point_count} key points.")

if point_count < 2:
    # Gate FAILED — stop the chain immediately. Don't waste tokens on step 2.
    print("GATE FAILED: Not enough key points extracted. Chain stopped.")
else:
    # Gate PASSED — continue to step 2
    print("Gate passed. Continuing to draft...\n")

    # Step 2: Draft
    print("--- Step 2: Draft Blog Post ---")
    draft = call_gemini(
        DRAFT_SYSTEM,
        f"Topic: {topic2}\n\nKey points to cover:\n{key_points2}",
    )
    print(draft)


# =============================================================================
# EXAMPLE 3: Full 4-Step Pipeline (Blog Post Factory)
# =============================================================================
# The complete chain from the teaching: Extract → Gate → Draft → Critique → Polish
#
# This shows:
#   - 4 LLM calls, each with a different system prompt (persona)
#   - 1 gate between steps 1 and 2
#   - Step 4 receiving output from BOTH step 2 and step 3 (not just previous step)
#   - Full logging so you can inspect every intermediate result
#
# This is the pattern real production pipelines use. Content generation,
# code review bots, data processing — all follow this structure.

print("\n" + "=" * 70)
print("EXAMPLE 3: Full 4-Step Blog Post Pipeline")
print("=" * 70)

# --- System prompts: one per step, one persona per step ---

EXTRACT_SYSTEM_V2 = (
    "You are a content strategist. Given a topic, identify 3-4 key points "
    "that MUST be covered for the article to be useful. Output a numbered "
    "list only. Be specific — not 'benefits' but 'reduces debugging time "
    "by isolating failures to individual steps'."
)

DRAFT_SYSTEM_V2 = (
    "You are a technical blog writer. Write a short blog post (4-5 paragraphs) "
    "covering the given key points. Use clear language, one concrete example, "
    "and a strong opening sentence. Target audience: developers who've used "
    "LLMs but haven't built pipelines."
)

CRITIQUE_SYSTEM = (
    "You are a senior technical editor. Review the given blog post draft and "
    "list 3-5 SPECIFIC improvements. Focus on: clarity, missing nuance, "
    "weak examples, and flow. Do NOT rewrite — just list what to fix. "
    "Format: numbered list of actionable critiques."
)

POLISH_SYSTEM = (
    "You are a senior technical writer. Rewrite the draft incorporating ALL "
    "the editor's feedback. Keep the same structure and length but improve "
    "based on every critique. Output ONLY the final polished blog post."
)


def run_blog_pipeline(topic):
    """
    Run the full 4-step blog post pipeline.

    Returns the final polished post, or an error string if a gate fails.
    Every intermediate result is printed so you can inspect the chain.
    """
    print(f"\nInput topic: {topic}\n")

    # --- Step 1: Extract key points ---
    print("--- Step 1: Extract Key Points ---")
    key_points = call_gemini(EXTRACT_SYSTEM_V2, f"Topic: {topic}")
    print(key_points)

    # --- Gate: Did we get enough points? ---
    point_count = count_points(key_points)
    print(f"--- Gate: Found {point_count} key points ---")
    if point_count < 2:
        return f"CHAIN STOPPED at gate: only {point_count} key points extracted."
    print("Gate passed.\n")

    # --- Step 2: Draft blog post ---
    print("--- Step 2: Draft Blog Post ---")
    draft = call_gemini(
        DRAFT_SYSTEM_V2,
        f"Topic: {topic}\n\nKey points to cover:\n{key_points}",
    )
    print(draft)

    # --- Step 3: Critique the draft ---
    # The critic ONLY sees the draft — not the original topic or key points.
    # This is intentional: the draft should stand on its own. If the critic
    # needs to know the topic to understand the draft, the draft is unclear.
    print("--- Step 3: Critique the Draft ---")
    critique = call_gemini(CRITIQUE_SYSTEM, f"Blog post draft:\n\n{draft}")
    print(critique)

    # --- Step 4: Polish incorporating feedback ---
    # This step receives output from BOTH step 2 (draft) AND step 3 (critique).
    # Not just the previous step — we pass forward whatever the step needs.
    # All intermediate results are in Python variables, available anytime.
    print("--- Step 4: Polish Final Version ---")
    final = call_gemini(
        POLISH_SYSTEM,
        f"Original draft:\n\n{draft}\n\n"
        f"Editor feedback:\n\n{critique}\n\n"
        f"Rewrite the draft incorporating all feedback above.",
    )
    print(final)

    return final


# Run the full pipeline
final_post = run_blog_pipeline(
    "Why breaking LLM tasks into chains of smaller prompts beats one giant prompt"
)


# =============================================================================
# EXAMPLE 4: Chain with Structured Output (JSON Gate)
# =============================================================================
# A more realistic gate: the extraction step outputs JSON, and the gate
# validates that it's actually parseable JSON. This pattern is extremely
# common in production — you need structured output to pass to downstream
# code, and the gate ensures the LLM actually followed the format.

import json

print("\n" + "=" * 70)
print("EXAMPLE 4: Chain with JSON Gate")
print("=" * 70)

JSON_EXTRACT_SYSTEM = (
    "You are a data extraction assistant. Given a topic, output a JSON object "
    "with this exact structure:\n"
    '{"key_points": ["point 1", "point 2", "point 3"], "audience": "description", "tone": "description"}\n'
    "Output ONLY valid JSON, no markdown fencing, no explanation."
)

TARGETED_DRAFT_SYSTEM = (
    "You are a blog writer. Given structured metadata about a blog post "
    "(key points, target audience, tone), write a short blog post "
    "(3-4 paragraphs). Follow the metadata exactly."
)

topic4 = "Context windows and why they matter for LLM applications"

# Step 1: Extract as JSON
print(f"\nInput topic: {topic4}")
print("\n--- Step 1: Extract Structured Metadata (JSON) ---")
raw_json = call_gemini(JSON_EXTRACT_SYSTEM, f"Topic: {topic4}")
print(f"Raw output:\n{raw_json}")

# GATE: Is it valid JSON?
# This is the most common gate in production chains. LLMs sometimes add
# markdown fencing (```json ... ```) or explanation text around the JSON.
# The gate catches this so you don't get a crash in step 2.
print("\n--- Gate: Validating JSON ---")
try:
    # Strip potential markdown fencing the model might add despite instructions
    cleaned = raw_json.strip()
    if cleaned.startswith("```"):
        # Remove ```json and ``` fencing
        cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    metadata = json.loads(cleaned)
    print(f"Valid JSON! Keys: {list(metadata.keys())}")
    print(f"Key points: {metadata.get('key_points', 'MISSING')}")
    print(f"Audience: {metadata.get('audience', 'MISSING')}")
    print(f"Tone: {metadata.get('tone', 'MISSING')}")
    gate_passed = True
except json.JSONDecodeError as e:
    print(f"GATE FAILED: Invalid JSON — {e}")
    gate_passed = False

if gate_passed:
    # Step 2: Draft using the structured metadata
    # We format the metadata nicely for the model — it doesn't need raw JSON
    print("\n--- Step 2: Draft from Structured Metadata ---")
    formatted_input = (
        f"Topic: {topic4}\n"
        f"Key points to cover: {', '.join(metadata.get('key_points', []))}\n"
        f"Target audience: {metadata.get('audience', 'general')}\n"
        f"Tone: {metadata.get('tone', 'neutral')}"
    )
    draft4 = call_gemini(TARGETED_DRAFT_SYSTEM, formatted_input)
    print(draft4)
else:
    print("Chain stopped due to JSON gate failure.")


# =============================================================================
# SUMMARY OF PATTERNS
# =============================================================================
#
# Pattern 1 — SIMPLE CHAIN:
#   call() → call() → call()
#   Output of each step feeds into the next. No checks.
#
# Pattern 2 — GATED CHAIN:
#   call() → gate_check() → call() → call()
#   Programmatic check between steps. Stops chain on failure.
#
# Pattern 3 — MULTI-INPUT STEP:
#   step1_out = call()
#   step2_out = call(step1_out)
#   step3_out = call(step1_out + step2_out)   ← uses outputs from BOTH earlier steps
#
# Pattern 4 — JSON GATE:
#   call(output JSON) → json.loads() validation → call(use parsed data)
#   Forces structured output; gate ensures it's parseable before continuing.
#
# WHAT'S NEXT:
#   Topic 19 (Routing) adds CONDITIONAL paths — instead of a fixed A→B→C,
#   the output of one step determines WHICH step runs next. That's where
#   chains become dynamic workflows.
# =============================================================================
