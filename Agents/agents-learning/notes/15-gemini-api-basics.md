# 15 - Gemini API Basics

**Topic:** Making raw API calls to Gemini using the google-genai SDK

---

## Setup

```bash
pip install google-genai
```

API key from [aistudio.google.com](https://aistudio.google.com) — free tier, Gemini 2.0 Flash.

**Always use environment variables for API keys — never hardcode in files that go to git.**

```bash
# Windows
set GEMINI_API_KEY=your_key_here
```

```python
import os
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")
```

---

## The Client

```python
from google import genai
client = genai.Client(api_key=API_KEY)
```

Created once, reused for all calls. Holds authentication.

| Framework | Equivalent |
|-----------|-----------|
| Pydantic AI | No explicit client — model specified per agent |
| LangGraph | `ChatGoogleGenerativeAI(model="gemini-2.0-flash")` |
| Google ADK | Client managed by ADK runner |

---

## Basic Call

```python
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="What is an API?"
)
print(response.text)
```

---

## The Response Object

```python
response.text                                          # shortcut to text
response.candidates[0].content.parts[0].text          # full path
response.candidates[0].finish_reason                   # why model stopped
response.usage_metadata.prompt_token_count             # input tokens
response.usage_metadata.candidates_token_count         # output tokens
response.usage_metadata.total_token_count              # total
```

### finish_reason values

| Value | Meaning |
|-------|---------|
| `STOP` | Model decided it was done — normal |
| `MAX_TOKENS` | Hit output token limit |
| `TOOL_CALLS` | Model wants to call a tool (Topic 23) |

`finish_reason` is the Gemini equivalent of Claude's `stop_reason` — it drives the agent loop decision.

| Framework | Token usage access |
|-----------|-------------------|
| Pydantic AI | `result.usage()` → `Usage(input_tokens=X, output_tokens=Y)` |
| LangGraph | Callback handler required |
| Google ADK | Via tracing/telemetry |

---

## System Prompt

```python
from google.genai import types

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a concise assistant.",
        max_output_tokens=100,
        temperature=0.7,   # Gemini uses 0-2 (not 0-1 like Claude)
    ),
    contents="What is machine learning?"
)
```

`system_instruction` goes in `config=`, separate from `contents=`. Applies to the whole conversation.

| Framework | System prompt equivalent |
|-----------|------------------------|
| Pydantic AI | `Agent("gemini-2.0-flash", system_prompt="...")` |
| LangGraph | `SystemMessage("...")` in messages list |
| Google ADK | `LlmAgent(instruction="...")` |

---

## Multi-Turn: Chat Helper

```python
chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(system_instruction="Be concise.")
)

response = chat.send_message("My name is Prajesh.")
response = chat.send_message("What's my name?")  # model remembers

history = chat.get_history()  # inspect the full messages list
```

The `chat` object manages the `messages` array internally. This is the in-context state from Topic 14 — each turn is appended and sent back on every call.

---

## Multi-Turn: Raw Message History

The chat helper is convenient but hides the messages list. The raw version shows exactly what happens under the hood — and is the foundation for the agent loop (Topic 22):

```python
history = []

def send_message_raw(user_text: str) -> str:
    history.append(types.Content(role="user", parts=[types.Part(text=user_text)]))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=history,         # send ALL turns every time
    )

    history.append(types.Content(role="model", parts=[types.Part(text=response.text)]))
    return response.text
```

**The model has no memory.** Every call is stateless. "Memory" is the history list you maintain and send back each time.

| Framework | Message history equivalent |
|-----------|--------------------------|
| Pydantic AI | Managed internally per run |
| LangGraph | `MessagesState` — the graph's state dict |
| Google ADK | `session.history` managed by ADK runner |

---

## Key Parameters

| Parameter | What It Does | Notes |
|-----------|-------------|-------|
| `model` | Which Gemini to use | `gemini-2.0-flash` = free tier |
| `system_instruction` | Sets role and behavior | In `config=` block |
| `contents` | User message(s) or history | String or list of Content objects |
| `max_output_tokens` | Caps response length | Always set to avoid runaway generation |
| `temperature` | Randomness | 0–2 for Gemini (0 = deterministic) |
| `tools` | Function calling | Topic 23 |

---

## Code File

See [code/15-gemini-api-basics.py](../code/15-gemini-api-basics.py) — 6 runnable sections covering all of the above.

---

## Connection to Previous Topics

- **Topic 11 (Agent Loop):** The raw message history pattern here IS the agent loop. `contents=history` is the observe step; appending the response is the state update.
- **Topic 14 (State & Memory):** The `history` list is in-context state. No history list = stateless call.
- **Topic 03 (Context Engineering):** `system_instruction`, `contents`, and `history` together form the context window.

---

[← Back to ROADMAP](../ROADMAP.md)
