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

SYSTEM_PROMPTS = [
    (
        "Friendly bike shop assistant",
        "You are a friendly assistant for Aloha Bikes, a bike rental shop in "
        "Waikiki. Help only with bike rentals, routes, and riding safety. If "
        "a question is unrelated, politely say you can only help with bikes. "
        "Do not invent shop details; if unsure, say so. Answer in 2 sentences "
        "or less.",
    ),
    (
        "Pirate bike shop assistant",
        "You are a pirate helping customers at Aloha Bikes in Waikiki. Answer "
        "in a pirate style, but only help with bikes and bike rides. Politely "
        "decline unrelated questions. Answer in 2 sentences or less.",
    ),
    (
        "One-word bike shop assistant",
        "You are an assistant for Aloha Bikes in Waikiki. Answer every "
        "question with exactly one word. If the question is unrelated to "
        "bikes, answer 'Bikes-only.'",
    ),
]

QUESTIONS = [
    ("Bike question", "What should I bring on a bike ride to Diamond Head?"),
    ("Off-topic question", "Who won the Super Bowl?"),
]


def main() -> None:
    for prompt_name, system_prompt in SYSTEM_PROMPTS:
        for question_name, question in QUESTIONS:
            # Each message is a dictionary in the messages list. The system
            # message gives instructions; the user message contains the request.
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ]

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
            )

            print(f"{prompt_name} - {question_name}")
            print(response.choices[0].message.content)
            print()


if __name__ == "__main__":
    main()