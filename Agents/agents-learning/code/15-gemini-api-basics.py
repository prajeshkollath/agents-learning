# =============================================================================
# TOPIC 15: Gemini API Basics — Raw SDK Calls
# =============================================================================
#
# HOW TO RUN:
#   1. pip install google-genai
#   2. Get a free API key from https://aistudio.google.com → "Get API key"
#   3. Replace YOUR_API_KEY below (or set env var GEMINI_API_KEY)
#   4. Run: python 15-gemini-api-basics.py
#
# WHAT THIS COVERS:
#   - Making a basic API call to Gemini
#   - Reading the response object (text, tokens, finish reason)
#   - Adding a system prompt
#   - Multi-turn conversations
# =============================================================================

import os
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# SECTION 1: Create the client
# WHY: The client is your connection to the Gemini API. You create it once
#      and reuse it for all calls. It holds your authentication.
# -----------------------------------------------------------------------------

# Load key from environment variable (safer than hardcoding)
# Set it first: Windows → set GEMINI_API_KEY=your_key  |  Mac/Linux → export GEMINI_API_KEY=your_key
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")
client = genai.Client(api_key=API_KEY)

# FRAMEWORK EQUIVALENT:
#   Pydantic AI: model is specified per-agent, no explicit client
#   LangGraph:   llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
#   Google ADK:  client is managed by the ADK runner


# -----------------------------------------------------------------------------
# SECTION 2: The simplest possible API call
# WHY: This is the foundation. One input (contents), one output (response).
#      Everything else builds on top of this.
# -----------------------------------------------------------------------------

print("=== SECTION 2: Basic Call ===")

response = client.models.generate_content(
    model="gemini-2.0-flash",   # free tier model — fast and capable
    contents="What is an API? Answer in one sentence."
)

# The response object has many fields — .text is the shortcut to the text
print(response.text)


# -----------------------------------------------------------------------------
# SECTION 3: Reading the full response object
# WHY: In production you need more than just text — you need to know why the
#      model stopped, and how many tokens you used (for cost and rate limits).
# -----------------------------------------------------------------------------

print("\n=== SECTION 3: Response Object ===")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Name three programming languages."
)

# The text output
print("Text:", response.text)

# finish_reason tells you WHY the model stopped generating:
#   "STOP"       = model decided it was done (normal)
#   "MAX_TOKENS" = hit the output token limit
#   "TOOL_CALLS" = model wants to call a tool (used in Topic 23)
print("Finish reason:", response.candidates[0].finish_reason)

# Token usage — important for cost tracking and context window management
print("Input tokens: ", response.usage_metadata.prompt_token_count)
print("Output tokens:", response.usage_metadata.candidates_token_count)
print("Total tokens: ", response.usage_metadata.total_token_count)

# FRAMEWORK EQUIVALENT for token usage:
#   Pydantic AI: result.usage()  → Usage(input_tokens=X, output_tokens=Y)
#   LangGraph:   requires callback handler setup
#   Google ADK:  available via tracing/telemetry


# -----------------------------------------------------------------------------
# SECTION 4: Adding a system prompt
# WHY: The system prompt sets the role and rules for the model.
#      It's separate from the user message — applies to the whole conversation.
#      This is how you configure behavior without repeating instructions every turn.
# -----------------------------------------------------------------------------

print("\n=== SECTION 4: System Prompt ===")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a sarcastic assistant who answers everything with exactly one dry sentence.",
        max_output_tokens=100,  # cap the response length
        temperature=0.7,        # 0 = deterministic, 2 = very creative (Gemini uses 0-2)
    ),
    contents="What is machine learning?"
)

print(response.text)

# FRAMEWORK EQUIVALENT for system prompt:
#   Pydantic AI: Agent("gemini-2.0-flash", system_prompt="...")
#   LangGraph:   SystemMessage("...") in the messages list
#   Google ADK:  LlmAgent(instruction="...")


# -----------------------------------------------------------------------------
# SECTION 5: Multi-turn conversation using the chat object
# WHY: Real applications are multi-turn. The chat object manages the messages
#      array for you — it appends each turn automatically so the model always
#      has the full history. This is the in-context state from Topic 14.
# -----------------------------------------------------------------------------

print("\n=== SECTION 5: Multi-Turn Chat ===")

# Create a chat session — this holds the message history internally
chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful assistant. Be concise."
    )
)

# Turn 1
response = chat.send_message("My name is Prajesh and I'm learning about AI agents.")
print("Turn 1:", response.text)

# Turn 2 — the model remembers turn 1 because the chat object sent it again
response = chat.send_message("What am I learning about?")
print("Turn 2:", response.text)

# Turn 3
response = chat.send_message("And what's my name?")
print("Turn 3:", response.text)

# You can inspect the full message history the model is seeing
print("\n--- Message history ---")
for message in chat.get_history():
    role = message.role
    text = message.parts[0].text if message.parts else ""
    print(f"  [{role}]: {text[:80]}...")


# -----------------------------------------------------------------------------
# SECTION 6: Multi-turn WITHOUT the chat helper (raw messages)
# WHY: The chat object is convenient but hides the messages array. Here you
#      build it manually — exactly how agent loops work under the hood.
#      Frameworks do this same thing; they just wrap it.
# -----------------------------------------------------------------------------

print("\n=== SECTION 6: Raw Message History (No Chat Helper) ===")

# Build the conversation history manually as a list of Content objects
history = []

def send_message_raw(user_text: str) -> str:
    """Send a message and update history manually."""
    # Add user turn to history
    history.append(types.Content(
        role="user",
        parts=[types.Part(text=user_text)]
    ))

    # Call the API with full history
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=history,  # send ALL turns, not just the latest
    )

    # Add model response to history so next call includes it
    history.append(types.Content(
        role="model",
        parts=[types.Part(text=response.text)]
    ))

    return response.text

print(send_message_raw("My favourite language is Python."))
print(send_message_raw("What's my favourite language?"))  # model remembers

# WHY THIS MATTERS: This is the exact pattern used in the agent loop (Topic 22).
# The loop appends tool results to this same history list and calls the API again.

# FRAMEWORK EQUIVALENT for message history:
#   Pydantic AI: managed internally
#   LangGraph:   MessagesState — the graph's state dict holds the messages list
#   Google ADK:  session.history managed by the ADK runner


# -----------------------------------------------------------------------------
# THINGS TO TRY:
# - Change the system_instruction in Section 4 and observe how the tone shifts
# - In Section 5, ask something that requires memory of turn 1 ("what did I say?")
# - In Section 6, print len(history) after each turn to see it growing
# - Set temperature=0 and run Section 4 multiple times — does it give identical answers?
# - Set max_output_tokens=10 and see what finish_reason becomes
# -----------------------------------------------------------------------------
