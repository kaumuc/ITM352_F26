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

BUSINESS_INFO = {
    "Business": "Aloha Bikes",
    "Business type": "Bike rental shop",
    "Location": "Waikiki",
}

system_context = (
    "You are a helpful assistant for Aloha Bikes. Use only the business "
    "information below. If a detail is not listed, say you do not know and "
    "suggest asking the shop.\n\nBusiness information:\n"
)

for label, detail in BUSINESS_INFO.items():
    system_context += f"- {label}: {detail}\n"

messages = [{"role": "system", "content": system_context}]

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