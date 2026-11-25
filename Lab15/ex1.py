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

# messages is a list of dictionaries. Each dictionary maps string keys
# ("role" and "content") to string values. This structure makes it easy to
# construct and send messages programmatically to an LLM.
messages = [
    {
        "role": "user",
        "content": "Suggest a name for a shave ice shop in Honolulu.",
    }
]

response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
)

print(response.choices[0].message.content)

# My hypothesis: The answers are different because the model can choose
# different words each time instead of always giving the exact same response.