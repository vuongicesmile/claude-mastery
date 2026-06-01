# Module 08 — Claude API & SDK

## 🔑 Setup

```bash
pip install anthropic          # Python
npm install @anthropic-ai/sdk  # TypeScript/JavaScript
```

```python
import anthropic
client = anthropic.Anthropic(api_key="sk-ant-...")
```

## 💬 Basic Chat

```python
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain async/await in Python"}
    ]
)
print(message.content[0].text)
```

## 📡 Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a poem"}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## 🛠 Tool Use (Function Calling)

```python
tools = [{
    "name": "get_weather",
    "description": "Get current weather for a city",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name"}
        },
        "required": ["city"]
    }
}]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Da Lat?"}]
)

# Handle tool call
if response.stop_reason == "tool_use":
    tool_use = next(b for b in response.content if b.type == "tool_use")
    city = tool_use.input["city"]
    
    # Call your actual weather API
    weather = call_weather_api(city)
    
    # Send result back
    final = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=tools,
        messages=[
            {"role": "user", "content": "Weather in Da Lat?"},
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool_use.id, "content": weather}]}
        ]
    )
```

## 💾 Prompt Caching (SAVE 90% COST)

```python
# Without cache: every call re-processes the system prompt
# With cache: processed once, cached for 5 minutes

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[{
        "type": "text",
        "text": "You are a helpful assistant. " + LARGE_CONTEXT,
        "cache_control": {"type": "ephemeral"}  # ← cache this!
    }],
    messages=[{"role": "user", "content": user_question}]
)

# Check cache performance
print(response.usage.cache_creation_input_tokens)  # first call
print(response.usage.cache_read_input_tokens)       # subsequent calls
```

## 🧠 Extended Thinking

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # how much to think
    },
    messages=[{"role": "user", "content": "Solve this complex problem..."}]
)

# Get thinking + answer
for block in response.content:
    if block.type == "thinking":
        print("THINKING:", block.thinking)
    elif block.type == "text":
        print("ANSWER:", block.text)
```

## 📁 Files API

```python
# Upload a file
with open("document.pdf", "rb") as f:
    file = client.beta.files.upload(
        file=("document.pdf", f, "application/pdf")
    )

# Use in message
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "document", "source": {"type": "file", "file_id": file.id}},
            {"type": "text", "text": "Summarize this document"}
        ]
    }]
)
```

## 🔢 Batch API (Process 1000s of requests)

```python
# Create batch
batch = client.messages.batches.create(
    requests=[
        {"custom_id": f"req-{i}", "params": {
            "model": "claude-haiku-4-5",
            "max_tokens": 100,
            "messages": [{"role": "user", "content": f"Question {i}"}]
        }}
        for i in range(1000)
    ]
)

# Check status
batch = client.messages.batches.retrieve(batch.id)
print(batch.processing_status)  # "in_progress" or "ended"

# Get results
for result in client.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        print(result.custom_id, result.result.message.content[0].text)
```

## 🏗 Build a Simple AI App

```python
# ai_assistant.py — production-ready pattern
import anthropic
from functools import lru_cache

@lru_cache
def get_client():
    return anthropic.Anthropic()

SYSTEM_PROMPT = """
You are a helpful coding assistant specialized in Python and FastAPI.
Always provide working code examples.
Always add error handling.
"""

def chat(user_message: str, history: list = None) -> str:
    client = get_client()
    
    messages = history or []
    messages.append({"role": "user", "content": user_message})
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"}
        }],
        messages=messages,
    )
    
    reply = response.content[0].text
    messages.append({"role": "assistant", "content": reply})
    
    return reply, messages

# Usage
reply, history = chat("How do I add JWT auth to FastAPI?")
reply2, history = chat("Show me the refresh token logic", history)
```
