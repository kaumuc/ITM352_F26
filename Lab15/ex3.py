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


def main() -> None:
    first_user_message = "My name is Kaumu."
    follow_up_question = "What is my name?"

    conversation = [{"role": "user", "content": first_user_message}]
    first_response = client.chat.completions.create(
        model=MODEL,
        messages=conversation,
    )
    first_reply = first_response.choices[0].message.content
    if first_reply is None:
        raise RuntimeError("The first model response did not contain text.")
    print(f"First reply: {first_reply}\n")

    messages_without_history = [
        {"role": "user", "content": follow_up_question},
    ]
    second_response = client.chat.completions.create(
        model=MODEL,
        messages=messages_without_history,
    )
    print(
        "Reply without history: "
        f"{second_response.choices[0].message.content}\n"
    )

    conversation.append({"role": "assistant", "content": first_reply})
    conversation.append({"role": "user", "content": follow_up_question})
    third_response = client.chat.completions.create(
        model=MODEL,
        messages=conversation,
    )
    print(
        "Reply with history: "
        f"{third_response.choices[0].message.content}"
    )


if __name__ == "__main__":
    main()