import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent / ".env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODEL = "openrouter/free"

DEFAULT_SYSTEM_CONTEXT = "You are a helpful assistant for Aloha Bikes."
system_context = input(
    "Enter system context, or leave blank for the default: "
).strip()
if not system_context:
    system_context = DEFAULT_SYSTEM_CONTEXT

messages = [
    {
        "role": "system",
        "content": system_context,
    }
]

# The list starts with one system message. Each turn adds a user and assistant message.
while True:
    user_text = input("You: ")

    if user_text.strip().lower() == "quit":
        print("Goodbye!")
        break

    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    assistant_reply = response.choices[0].message.content
    if assistant_reply is None:
        raise RuntimeError("The model response did not contain text.")

    print(f"Assistant: {assistant_reply}")
    messages.append({"role": "assistant", "content": assistant_reply})
    print(f"Messages in history: {len(messages)}")