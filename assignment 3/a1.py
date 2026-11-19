
import json
import os
import random
from pathlib import Path

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "local-development-key")

ASSIGNMENT_ONE_FOLDER = Path(__file__).resolve().parent.parent / "assignment 1"
QUESTIONS_FILE = Path(__file__).with_name("questions.json")
MEDIA_FOLDER = ASSIGNMENT_ONE_FOLDER / "media"
NUM_QUESTIONS_PER_QUIZ = 5


def load_questions():
    """Load the question dictionary from the local JSON file."""
    with QUESTIONS_FILE.open("r", encoding="utf-8") as question_file:
        return json.load(question_file)


def get_answers(question_data):
    """Return answer choices for text and image questions."""
    if isinstance(question_data, dict):
        return question_data["answers"]
    return question_data


def select_questions(questions):
    """Choose five questions and include Assignment 1's image questions."""
    question_items = list(questions.items())
    number_to_select = min(NUM_QUESTIONS_PER_QUIZ, len(question_items))
    media_questions = [
        item
        for item in question_items
        if isinstance(item[1], dict) and item[1].get("media") is not None
    ]

    selected_questions = random.sample(
        media_questions, k=min(len(media_questions), number_to_select)
    )
    selected_names = [question for question, _ in selected_questions]
    other_questions = [
        item for item in question_items if item[0] not in selected_names
    ]
    selected_questions.extend(
        random.sample(
            other_questions, k=number_to_select - len(selected_questions)
        )
    )
    return random.sample(selected_questions, k=len(selected_questions))


def show_question(error=None):
    """Display the current question and its shuffled choices."""
    question_number = session["question_number"]
    question = session["question_order"][question_number]
    question_data = load_questions()[question]
    media = question_data.get("media") if isinstance(question_data, dict) else None
    media_filename = None
    if media is not None:
        media_filename = media["source"].split("/")[-1]

    return render_template(
        "quiz.html",
        question=question,
        question_number=question_number + 1,
        total_questions=len(session["question_order"]),
        options=session["answer_options"][question],
        media_filename=media_filename,
        error=error,
        show_progress=False,
        responsive=False,
    )


@app.route("/")
def index():
    return render_template(
        "index.html",
        show_leaderboard=False,
        responsive=False,
    )


@app.route("/start", methods=["POST"])
def start_quiz():
    questions = load_questions()
    if not questions:
        raise ValueError("The question file contains no questions.")

    selected_questions = select_questions(questions)
    session["question_order"] = [
        question for question, _ in selected_questions
    ]
    session["answer_options"] = {}
    for question, question_data in selected_questions:
        answers = get_answers(question_data)
        session["answer_options"][question] = random.sample(
            answers, k=len(answers)
        )
    session["question_number"] = 0
    session["score"] = 0
    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "question_order" not in session:
        return redirect(url_for("index"))
    if session["question_number"] >= len(session["question_order"]):
        return redirect(url_for("result"))

    if request.method == "POST":
        answer = request.form.get("answer")
        question = session["question_order"][session["question_number"]]
        options = session["answer_options"][question]
        if answer not in options:
            return show_question("Please choose one of the answer options.")

        correct_answer = get_answers(load_questions()[question])[0]
        if answer == correct_answer:
            session["score"] += 1

        session["question_number"] += 1
        if session["question_number"] >= len(session["question_order"]):
            return redirect(url_for("result"))
        return redirect(url_for("quiz"))

    return show_question()


@app.route("/result")
def result():
    if "question_order" not in session:
        return redirect(url_for("index"))
    if session["question_number"] < len(session["question_order"]):
        return redirect(url_for("quiz"))

    return render_template(
        "result.html",
        score=session["score"],
        max_questions=len(session["question_order"]),
        error=None,
        show_leaderboard=False,
        show_review=False,
        responsive=False,
    )


@app.route("/question-media/<path:filename>")
def question_media(filename):
    return send_from_directory(MEDIA_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
