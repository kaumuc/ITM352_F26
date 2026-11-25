import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from mycontent import INFO, MENU, build_system_prompt

load_dotenv(Path(__file__).resolve().parent / ".env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODEL = "openrouter/free"

messages = [
    {
        "role": "system",
        "content": build_system_prompt(MENU, INFO),
    }
]

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