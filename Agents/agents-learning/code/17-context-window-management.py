# =============================================================================
# TOPIC 17: Context Window Management
# =============================================================================
#
# HOW TO RUN:
#   1. pip install google-genai
#   2. Set your API key: set GEMINI_API_KEY=your_key  (Windows)
#                        export GEMINI_API_KEY=your_key (Mac/Linux)
#   3. Run: python 17-context-window-management.py
#
# WHAT THIS COVERS:
#   - Token counting (exact via API + rough estimation)
#   - Strategy 1: Truncation — drop oldest turns when over budget
#   - Strategy 2: Sliding window — keep only last N turns
#   - Strategy 3: Auto-summarization — compress old turns into a summary
#   - Hybrid approach — summary + sliding window combined
#
# KEY INSIGHT:
#   The context window is a hard limit. If you exceed it, the API rejects
#   your call. Even below the limit, more tokens = more cost + slower responses.
#   Managing what goes into the window is about: (1) not breaking, (2) saving
#   money, (3) keeping responses fast, and (4) preserving relevant context.
#
# FRAMEWORK EQUIVALENTS:
#   - LangChain: ConversationBufferWindowMemory (sliding window),
#                ConversationSummaryMemory (auto-summarize),
#                ConversationSummaryBufferMemory (hybrid)
#   - LangGraph: You manage state in graph nodes; checkpointing + reducers
#   - Pydantic AI: Manual — you manage message history yourself
#   - Google ADK: Session state + memory tools; context management is manual
#
# CONNECTION TO TOPIC 16 (Caching):
#   Caching saves money on the STABLE parts of the context.
#   Context management prevents OVERFLOW of the growing parts.
#   In production, you cache the system prompt + summary (stable prefix)
#   and manage the recent turns (dynamic, growing).
# =============================================================================

import os
from google import genai
from google.genai import types

# --- Setup ---
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY"))
MODEL = "gemini-2.0-flash"

print("=" * 70)
print("TOPIC 17: Context Window Management")
print("=" * 70)


# =============================================================================
# PART 1: TOKEN COUNTING — Know How Big Your Context Is
# =============================================================================
# Before you can manage the window, you need to measure what's in it.
# Two approaches:
#   1. Exact count via API (costs a round-trip, but precise)
#   2. Rough estimate (~4 chars per token, free, good for thresholds)
# =============================================================================

print("\n" + "=" * 70)
print("PART 1: Token Counting")
print("=" * 70)

# --- Exact token counting via API ---
# The count_tokens endpoint tells you exactly how many tokens a message uses.
# This does NOT generate a response — it just counts.
sample_text = "The quick brown fox jumps over the lazy dog. " * 50  # ~500 words

response = client.models.count_tokens(
    model=MODEL,
    contents=sample_text
)
exact_count = response.total_tokens
print(f"\nExact token count (via API): {exact_count}")
print(f"Character count: {len(sample_text)}")
print(f"Actual ratio: {len(sample_text) / exact_count:.1f} chars per token")

# --- Rough estimation ---
# Rule of thumb: ~4 characters per token for English text.
# This is fast (no API call) and good enough for "should I trim?" checks.
estimated_count = len(sample_text) // 4
print(f"\nEstimated token count (~4 chars/token): {estimated_count}")
print(f"Estimation error: {abs(exact_count - estimated_count)} tokens "
      f"({abs(exact_count - estimated_count) / exact_count * 100:.1f}%)")

# FRAMEWORK EQUIVALENT:
# LangChain: tiktoken library for OpenAI models, or model.get_num_tokens()
# All frameworks ultimately call the provider's count endpoint or use
# a local tokenizer. There's no magic — someone has to count.


# =============================================================================
# PART 2: TRUNCATION — Drop Oldest Turns
# =============================================================================
# The simplest strategy: when history is too long, chop from the front.
# Always keep the system prompt. Drop complete turn pairs (user+model).
#
# Pros: Dead simple, no extra API calls
# Cons: Old context is completely lost
# =============================================================================

print("\n" + "=" * 70)
print("PART 2: Truncation Strategy")
print("=" * 70)

SYSTEM_PROMPT = "You are a helpful coding tutor. Keep answers brief (1-2 sentences)."

# Simulate a conversation history — 8 turn pairs
conversation_history = [
    {"role": "user", "parts": [{"text": "What is a variable in Python?"}]},
    {"role": "model", "parts": [{"text": "A variable is a name that refers to a value stored in memory, like x = 5."}]},
    {"role": "user", "parts": [{"text": "What is a function?"}]},
    {"role": "model", "parts": [{"text": "A function is a reusable block of code defined with 'def' that performs a specific task."}]},
    {"role": "user", "parts": [{"text": "What is a class?"}]},
    {"role": "model", "parts": [{"text": "A class is a blueprint for creating objects, bundling data (attributes) and behavior (methods) together."}]},
    {"role": "user", "parts": [{"text": "What is inheritance?"}]},
    {"role": "model", "parts": [{"text": "Inheritance lets a child class reuse and extend the attributes and methods of a parent class."}]},
    {"role": "user", "parts": [{"text": "What is a decorator?"}]},
    {"role": "model", "parts": [{"text": "A decorator is a function that wraps another function to modify its behavior, using @syntax."}]},
    {"role": "user", "parts": [{"text": "What is a generator?"}]},
    {"role": "model", "parts": [{"text": "A generator is a function that yields values one at a time using 'yield', saving memory for large sequences."}]},
    {"role": "user", "parts": [{"text": "What is async/await?"}]},
    {"role": "model", "parts": [{"text": "Async/await lets you write non-blocking code that can pause (await) while waiting for I/O operations."}]},
    {"role": "user", "parts": [{"text": "What is a context manager?"}]},
    {"role": "model", "parts": [{"text": "A context manager handles setup/teardown automatically using 'with', like opening and closing files."}]},
]


def truncate_history(history, max_turns=4):
    """
    Keep only the last `max_turns` turn pairs from history.

    A turn pair = one user message + one model message = 2 list items.
    We always drop from the FRONT (oldest) and keep from the END (newest).

    WHY pairs? If you drop just the user message but keep the model response,
    the model sees an answer with no question — this confuses it.
    """
    max_messages = max_turns * 2  # each turn = user + model
    if len(history) > max_messages:
        dropped = len(history) - max_messages
        print(f"  Truncating: dropping {dropped // 2} oldest turn pairs")
        return history[-max_messages:]
    return history


# Show what truncation does
print(f"\nOriginal history: {len(conversation_history)} messages ({len(conversation_history) // 2} turns)")
truncated = truncate_history(conversation_history, max_turns=3)
print(f"After truncation (keep last 3 turns): {len(truncated)} messages")
print(f"Oldest remaining turn: '{truncated[0]['parts'][0]['text'][:50]}...'")

# Now use the truncated history to ask a new question
new_question = "Can you remind me what we discussed about variables?"

# With truncation, the model has NO idea about the variables discussion
# because those early turns were dropped
response = client.models.generate_content(
    model=MODEL,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
    ),
    contents=truncated + [{"role": "user", "parts": [{"text": new_question}]}]
)
print(f"\nQuestion: '{new_question}'")
print(f"Model's answer (with truncation — early context lost):")
print(f"  {response.text.strip()}")
print(f"  Tokens used: {response.usage_metadata.prompt_token_count} prompt, "
      f"{response.usage_metadata.candidates_token_count} response")

# FRAMEWORK EQUIVALENT:
# LangChain: ConversationBufferWindowMemory(k=3) does exactly this.
# It keeps the last k turns and drops the rest. Same tradeoff — simple but lossy.


# =============================================================================
# PART 3: SLIDING WINDOW — Keep Last N Turns
# =============================================================================
# Sliding window is conceptually the same as truncation with a fixed window.
# The key difference is the mindset: you DESIGN around a fixed window size
# rather than reacting when you hit a limit.
#
# In practice, truncation and sliding window are often the same code.
# The distinction matters more in how you think about your system design.
# =============================================================================

print("\n" + "=" * 70)
print("PART 3: Sliding Window Strategy")
print("=" * 70)

# Token-based sliding window (more precise than turn-based)
def sliding_window_by_tokens(history, system_prompt, max_total_tokens=500):
    """
    Keep as many recent turns as fit within max_total_tokens.

    WHY token-based instead of turn-based?
    Turn-based (keep last 3 turns) is simple but imprecise — turns vary wildly
    in length. One turn could be 10 tokens, another could be 5,000.
    Token-based gives you predictable cost and prevents window overflow.

    We use the rough estimate here (len/4) to avoid extra API calls.
    For production systems, you'd count tokens when adding each turn.
    """
    # Start from the most recent turn pair and work backward
    kept = []
    running_tokens = len(system_prompt) // 4  # system prompt always included

    # Walk backward through pairs (newest first)
    for i in range(len(history) - 2, -1, -2):
        user_msg = history[i]
        model_msg = history[i + 1]

        # Estimate tokens for this turn pair
        pair_tokens = (
            len(user_msg["parts"][0]["text"]) // 4 +
            len(model_msg["parts"][0]["text"]) // 4
        )

        if running_tokens + pair_tokens > max_total_tokens:
            break  # adding this pair would exceed budget

        running_tokens += pair_tokens
        kept = [user_msg, model_msg] + kept  # prepend to maintain order

    return kept, running_tokens


kept_history, token_estimate = sliding_window_by_tokens(
    conversation_history, SYSTEM_PROMPT, max_total_tokens=300
)

print(f"\nToken budget: 300 tokens")
print(f"Turns that fit: {len(kept_history) // 2}")
print(f"Estimated tokens used: {token_estimate}")
print(f"Oldest kept: '{kept_history[0]['parts'][0]['text'][:60]}...'")
print(f"Newest kept: '{kept_history[-2]['parts'][0]['text'][:60]}...'")


# =============================================================================
# PART 4: AUTO-SUMMARIZATION — Compress Old Turns
# =============================================================================
# Instead of throwing away old turns, we ask the LLM to summarize them.
# The summary replaces the detailed turns, preserving context in compressed form.
#
# Two flavors:
#   - Silent: code detects threshold, summarizes automatically, user never knows
#   - Prompted: you explicitly include "Summary so far: ..." in the prompt
#
# Tradeoff: costs an extra API call, but preserves context that truncation loses.
# =============================================================================

print("\n" + "=" * 70)
print("PART 4: Auto-Summarization Strategy")
print("=" * 70)


def summarize_history(history_to_summarize):
    """
    Send old conversation turns to the LLM and get a compact summary.

    WHY use the LLM to summarize?
    Because conversation context is messy — it has tangents, corrections,
    follow-ups. The LLM can extract what actually matters and compress it
    into a few sentences. No rule-based system can do this well.

    COST: This is an extra API call. It only pays off when the conversation
    is long enough that the token savings exceed the summarization cost.
    """
    # Format the history as readable text for the summarizer
    conversation_text = ""
    for msg in history_to_summarize:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation_text += f"{role}: {msg['parts'][0]['text']}\n"

    summary_response = client.models.generate_content(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=(
                "Summarize this conversation in 2-3 sentences. "
                "Focus on: what topics were covered, key facts established, "
                "and any decisions made. Be concise."
            ),
        ),
        contents=conversation_text
    )
    return summary_response.text.strip()


# Summarize the first 6 turn pairs (oldest), keep the last 2 verbatim
old_turns = conversation_history[:12]   # first 6 turn pairs to summarize
recent_turns = conversation_history[12:]  # last 2 turn pairs to keep verbatim

print(f"\nSummarizing {len(old_turns) // 2} old turn pairs...")
summary = summarize_history(old_turns)
print(f"\nGenerated summary:")
print(f"  \"{summary}\"")

# Now build the context with summary + recent turns
# The summary goes as the first user message (or you can put it in system prompt)
summarized_context = [
    {"role": "user", "parts": [{"text": f"[Previous conversation summary: {summary}]"}]},
    {"role": "model", "parts": [{"text": "Understood. I have context from our previous discussion."}]},
] + recent_turns

# Ask the same question — the model now has summary context about variables
response = client.models.generate_content(
    model=MODEL,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
    ),
    contents=summarized_context + [{"role": "user", "parts": [{"text": new_question}]}]
)
print(f"\nQuestion: '{new_question}'")
print(f"Model's answer (with summarization — old context preserved):")
print(f"  {response.text.strip()}")
print(f"  Tokens used: {response.usage_metadata.prompt_token_count} prompt, "
      f"{response.usage_metadata.candidates_token_count} response")

# FRAMEWORK EQUIVALENT:
# LangChain: ConversationSummaryMemory — does exactly this.
# It calls the LLM to summarize after each turn or after N turns.
# LangGraph: You'd implement this as a graph node that triggers on token count.
# Pydantic AI: Manual — you write this function yourself, same pattern.


# =============================================================================
# PART 5: HYBRID — Summary + Sliding Window (Production Pattern)
# =============================================================================
# The real-world pattern combines summarization with a sliding window:
#   [System prompt]           ← always present
#   [Summary of old turns]    ← compressed old context
#   [Last N turns verbatim]   ← recent, full-detail context
#   [New message]             ← current turn
#
# This gives you the best of both worlds:
#   - Recent context has full detail (for follow-up questions)
#   - Old context is preserved in compressed form (for callbacks)
#   - Total token count stays bounded
# =============================================================================

print("\n" + "=" * 70)
print("PART 5: Hybrid Strategy (Summary + Sliding Window)")
print("=" * 70)


class ConversationManager:
    """
    Manages a conversation with automatic summarization.

    This is the pattern production chat systems use. When history grows
    beyond a threshold, old turns get summarized and replaced.

    HOW IT WORKS:
    1. Every turn gets added to the full history
    2. Before each API call, check if history exceeds the threshold
    3. If yes: summarize the oldest turns, keep recent ones verbatim
    4. The context sent to the API is always: system + summary + recent + new

    FRAMEWORK EQUIVALENT:
    LangChain: ConversationSummaryBufferMemory(max_token_limit=500)
    This is EXACTLY what it does internally — same algorithm, packaged up.
    """

    def __init__(self, system_prompt, max_recent_turns=3, summarize_threshold=6):
        self.system_prompt = system_prompt
        self.max_recent_turns = max_recent_turns
        self.summarize_threshold = summarize_threshold  # trigger after this many turns
        self.full_history = []      # complete record (for debugging)
        self.summary = None         # compressed old context
        self.recent_turns = []      # last N turns, kept verbatim
        self.turn_count = 0

    def add_turn(self, user_message, model_response):
        """Record a complete turn pair."""
        self.full_history.append({"role": "user", "parts": [{"text": user_message}]})
        self.full_history.append({"role": "model", "parts": [{"text": model_response}]})
        self.recent_turns.append({"role": "user", "parts": [{"text": user_message}]})
        self.recent_turns.append({"role": "model", "parts": [{"text": model_response}]})
        self.turn_count += 1

        # Check if we need to summarize
        if len(self.recent_turns) // 2 > self.summarize_threshold:
            self._compress()

    def _compress(self):
        """Summarize old turns, keep only recent ones."""
        # Split: summarize all but the last max_recent_turns
        keep_count = self.max_recent_turns * 2
        to_summarize = self.recent_turns[:-keep_count]
        to_keep = self.recent_turns[-keep_count:]

        print(f"\n  [Auto-compressing: summarizing {len(to_summarize) // 2} turns, "
              f"keeping {len(to_keep) // 2} recent turns]")

        # If we already have a summary, include it in what we're summarizing
        if self.summary:
            summary_prefix = f"Previous summary: {self.summary}\n\n"
        else:
            summary_prefix = ""

        conversation_text = summary_prefix
        for msg in to_summarize:
            role = "User" if msg["role"] == "user" else "Assistant"
            conversation_text += f"{role}: {msg['parts'][0]['text']}\n"

        summary_response = client.models.generate_content(
            model=MODEL,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "Summarize this conversation in 2-3 sentences. "
                    "Capture the key topics, facts, and decisions. Be concise."
                ),
            ),
            contents=conversation_text
        )
        self.summary = summary_response.text.strip()
        self.recent_turns = to_keep
        print(f"  [New summary: \"{self.summary}\"]")

    def build_context(self, new_message):
        """
        Build the full context to send to the API.

        Structure:
          [summary turn pair, if exists]
          [recent turns verbatim]
          [new user message]
        """
        context = []

        # Add summary as context (if we have one)
        if self.summary:
            context.append({
                "role": "user",
                "parts": [{"text": f"[Conversation summary so far: {self.summary}]"}]
            })
            context.append({
                "role": "model",
                "parts": [{"text": "I recall our previous discussion. How can I help?"}]
            })

        # Add recent turns
        context.extend(self.recent_turns)

        # Add new message
        context.append({"role": "user", "parts": [{"text": new_message}]})

        return context

    def chat(self, user_message):
        """Send a message and get a response, with automatic context management."""
        context = self.build_context(user_message)

        response = client.models.generate_content(
            model=MODEL,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
            ),
            contents=context
        )

        model_text = response.text.strip()
        self.add_turn(user_message, model_text)

        return model_text, response.usage_metadata


# --- Run a multi-turn conversation that triggers auto-summarization ---
manager = ConversationManager(
    system_prompt="You are a helpful Python tutor. Keep answers to 1-2 sentences.",
    max_recent_turns=3,        # keep last 3 turns verbatim
    summarize_threshold=5      # summarize after 5 turns accumulate
)

questions = [
    "What is a variable?",
    "What is a list?",
    "What is a dictionary?",
    "How do I write a for loop?",
    "What is a function?",
    "What about lambda functions?",  # this should trigger summarization
    "What is a class?",
    "Now remind me — what did we say about variables at the start?",  # tests recall
]

for q in questions:
    print(f"\n  User: {q}")
    answer, usage = manager.chat(q)
    print(f"  Model: {answer}")
    print(f"  [Tokens: {usage.prompt_token_count} prompt, "
          f"{usage.candidates_token_count} response | "
          f"History: {manager.turn_count} total turns, "
          f"{len(manager.recent_turns) // 2} in window"
          f"{', has summary' if manager.summary else ''}]")


# =============================================================================
# PART 6: COMPARING THE STRATEGIES — Side by Side
# =============================================================================

print("\n" + "=" * 70)
print("PART 6: Strategy Comparison")
print("=" * 70)

print("""
Strategy          | Complexity  | Context Loss | Extra API Cost
------------------|-------------|--------------|----------------
Truncation        | Trivial     | Total        | None
Sliding Window    | Simple      | Total        | None
Summarization     | Moderate    | Partial      | 1 call/compress
Hybrid            | Moderate    | Minimal      | 1 call/compress

WHEN TO USE WHAT:
- Truncation/Sliding Window: Short conversations, cost-sensitive, context
  doesn't matter (e.g., one-shot Q&A bot)
- Summarization: Long conversations where users reference earlier context
  (e.g., tutoring, customer support)
- Hybrid: Production chat systems — best balance of cost and quality

REAL-WORLD EXAMPLES:
- ChatGPT: Uses a form of hybrid (sliding window + summary/compression)
- Claude: Uses context window management internally for long conversations
- Customer support bots: Often use sliding window (last 5-10 turns)
- Coding assistants: Prioritize recent code context, summarize older discussion
""")


# =============================================================================
# SUMMARY
# =============================================================================
print("=" * 70)
print("KEY TAKEAWAYS")
print("=" * 70)
print("""
1. PROBLEM: Context windows have hard limits. Even below limits, more
   tokens = more cost + slower responses.

2. TOKEN COUNTING: Use count_tokens() for precision, len//4 for estimates.

3. TRUNCATION: Drop oldest turns. Simple but loses all old context.

4. SLIDING WINDOW: Keep last N turns. Same as truncation with a fixed N.

5. SUMMARIZATION: Use the LLM to compress old turns into a summary.
   Preserves context but costs an extra API call per compression.

6. HYBRID (production pattern): Summary of old + verbatim recent turns.
   This is what LangChain's ConversationSummaryBufferMemory does.

7. CACHING + CONTEXT MANAGEMENT work together:
   Cache the stable prefix (system prompt, summary).
   Manage the growing part (conversation history).
""")
