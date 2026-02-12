# Gemini API Basics

## Setup
### Install
- pip install google-genai
### API Key
- Google AI Studio — free tier
- Always use env var, never hardcode
- os.environ.get("GEMINI_API_KEY")

## Client
- genai.Client(api_key=...)
- Created once, reused for all calls
- ADK manages it automatically

## Basic Call
- client.models.generate_content()
- model="gemini-2.0-flash"
- contents= the user message
- response.text = shortcut to output

## Response Object
### Text
- response.text (shortcut)
- response.candidates[0].content.parts[0].text
### finish_reason
- STOP = model done (normal)
- MAX_TOKENS = hit limit
- TOOL_CALLS = wants to call a tool
### Token Usage
- response.usage_metadata.prompt_token_count
- response.usage_metadata.candidates_token_count
- Pydantic AI: result.usage()
- LangGraph: callback handler

## System Prompt
- Goes in config= block
- types.GenerateContentConfig(system_instruction=...)
- max_output_tokens — cap response length
- temperature 0-2 (Gemini range, not 0-1)
- ADK equivalent: LlmAgent(instruction=...)

## Multi-Turn
### Chat Helper
- client.chats.create()
- chat.send_message()
- Manages history internally
- chat.get_history() to inspect

### Raw Message History
- history = [] list
- Append user Content, call API with full list
- Append model response back
- This IS the agent loop pattern
- LangGraph: MessagesState
- ADK: session.history

## Key Insight
- Model has NO memory
- Every API call is stateless
- "Memory" = the history list you maintain
- You send the entire history every call
