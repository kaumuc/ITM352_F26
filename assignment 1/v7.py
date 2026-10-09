# Interactive quiz system, seventh version
# Make a dictionary with the questions and correct answers
# Allow the user to choose the option by its label
# Improve the look and usability. Keep track of correct answers.
# Randomize the order of the questions and the order of the answers for each question.
# Refactor the code to use functions

from string import ascii_lowercase
import json
import random
from pathlib import Path

NUM_QUESTIONS_PER_QUIZ = 5

def load_questions():
    """Read the question dictionary from questions.json."""
    question_path = Path(__file__).with_name("questions.json")
    with question_path.open("r", encoding="utf-8") as question_file:
        return json.load(question_file)


def select_questions(questions):
    """Choose up to the requested number of questions in random order."""
    num_questions = min(NUM_QUESTIONS_PER_QUIZ, len(questions))
    return random.sample(list(questions.items()), k=num_questions)


def ask_question(question_number, question, answers):
    """Display one question and return True if the user's answer is correct.

    Return None if input ends before the user chooses an answer.
    """
    correct_answer = answers[0]
    print(f"\nQuestion {question_number}: {question}")

    shuffled_answers = random.sample(answers, k=len(answers))
    labeled_answers = dict(zip(ascii_lowercase, shuffled_answers))

    for label, answer in labeled_answers.items():
        print(f"{label}. {answer}")

    while True:
        try:
            answer_label = input("Choice? ").strip().lower()
        except EOFError:
            print("\nInput ended. Quiz stopped.")
            return None

        if answer_label in labeled_answers:
            break
        print(f"Invalid choice. Please select one of {', '.join(labeled_answers.keys())}.")

    answer = labeled_answers[answer_label]

    if answer == correct_answer:
        print("Correct!")
        return True

    print(f"The answer is {correct_answer!r}, not {answer!r}.")
    return False


def run_quiz():
    """Load questions, ask a random selection, and print the final score."""
    questions = load_questions()
    if not questions:
        print("No questions available.")
        return

    selected_questions = select_questions(questions)
    num_correct = 0

    for question_number, (question, answers) in enumerate(selected_questions, start=1):
        is_correct = ask_question(question_number, question, answers)
        if is_correct is None:
            return
        if is_correct:
            num_correct += 1

    print(f"\nYou got {num_correct} out of {len(selected_questions)} correct.")


def main():
    run_quiz()


if __name__ == "__main__":
    main()