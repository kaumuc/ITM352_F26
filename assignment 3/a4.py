"""Part 4: add responsive styling to the quiz, leaderboard, and review pages."""

import json
import os
import random
from pathlib import Path

from flask import (
    Flask,
    jsonify,
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
EXPLANATIONS_FILE = Path(__file__).with_name("explanations.json")
LEADERBOARD_FILE = Path(__file__).with_name("leaderboard.json")
MEDIA_FOLDER = ASSIGNMENT_ONE_FOLDER / "media"
NUM_QUESTIONS_PER_QUIZ = 5
# AI note: I asked AI how to enable mobile styling in shared templates. It taught me
# to use a flag to load the responsive stylesheet in this version.
RESPONSIVE = True


def load_questions():
    with QUESTIONS_FILE.open("r", encoding="utf-8") as question_file:
        return json.load(question_file)


def load_explanations():
    with EXPLANATIONS_FILE.open("r", encoding="utf-8") as explanation_file:
        return json.load(explanation_file)


def get_answers(question_data):
    if isinstance(question_data, dict):
        return question_data["answers"]
    return question_data


def select_questions(questions):
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


def load_scores():
    with LEADERBOARD_FILE.open("r", encoding="utf-8") as score_file:
        return json.load(score_file)


def save_scores(scores):
    with LEADERBOARD_FILE.open("w", encoding="utf-8") as score_file:
        json.dump(scores, score_file, indent=2)
        score_file.write("\n")


def get_top_scores():
    scores = load_scores()
    # AI note: I asked AI how to show only the top ten. It taught me to sort scores
    # high-to-low and keep the first ten.
    return sorted(scores, key=lambda result: result["score"], reverse=True)[:10]


def show_question(error=None):
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
        progress_value=question_number,
        options=session["answer_options"][question],
        media_filename=media_filename,
        error=error,
        show_progress=True,
        responsive=RESPONSIVE,
    )


@app.route("/")
def index():
    return render_template(
        "index.html",
        show_leaderboard=True,
        responsive=RESPONSIVE,
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
    session["review"] = []
    session.pop("last_answer", None)
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
        is_correct = answer == correct_answer
        if is_correct:
            session["score"] += 1

        explanation = load_explanations()[question]
        review = session["review"]
        review.append(
            {
                "question": question,
                "chosen_answer": answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "explanation": explanation,
            }
        )
        session["review"] = review
        session["question_number"] += 1
        session["last_answer"] = {
            "question": question,
            "chosen_answer": answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": explanation,
        }
        return redirect(url_for("feedback"))

    return show_question()


@app.route("/feedback")
def feedback():
    if "last_answer" not in session:
        return redirect(url_for("quiz"))

    return render_template(
        "feedback.html",
        **session["last_answer"],
        progress_value=session["question_number"],
        total_questions=len(session["question_order"]),
        responsive=RESPONSIVE,
    )


@app.route("/next", methods=["POST"])
def next_question():
    if "question_order" not in session:
        return redirect(url_for("index"))
    if session["question_number"] >= len(session["question_order"]):
        return redirect(url_for("result"))
    session.pop("last_answer", None)
    return redirect(url_for("quiz"))


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
        show_leaderboard=True,
        show_review=True,
        responsive=RESPONSIVE,
    )


@app.route("/review")
def review():
    if "question_order" not in session:
        return redirect(url_for("index"))
    if session["question_number"] < len(session["question_order"]):
        return redirect(url_for("quiz"))

    missed_questions = [
        answer for answer in session["review"] if not answer["is_correct"]
    ]
    return render_template(
        "review.html",
        missed_questions=missed_questions,
        responsive=RESPONSIVE,
    )


@app.route("/submit-score", methods=["POST"])
def submit_score():
    if "question_order" not in session:
        return redirect(url_for("index"))
    if session["question_number"] < len(session["question_order"]):
        return redirect(url_for("quiz"))

    name = request.form.get("name", "").strip()
    if not name or len(name) > 40:
        return render_template(
            "result.html",
            score=session["score"],
            max_questions=len(session["question_order"]),
            error="Enter a name between 1 and 40 characters.",
            show_leaderboard=True,
            show_review=True,
            responsive=RESPONSIVE,
        )

    scores = load_scores()
    scores.append({"name": name, "score": session["score"]})
    save_scores(scores)
    return redirect(url_for("leaderboard"))


@app.route("/leaderboard")
def leaderboard():
    return render_template(
        "leaderboard.html",
        scores=get_top_scores(),
        responsive=RESPONSIVE,
    )


@app.route("/api/questions")
def api_questions():
    # AI note: I asked AI how to provide data to other programs. It taught me to
    # return JSON with jsonify instead of rendering an HTML template.
    question_records = []
    for question, question_data in load_questions().items():
        answers = get_answers(question_data)
        record = {
            "question": question,
            "options": random.sample(answers, k=len(answers)),
        }
        if isinstance(question_data, dict) and question_data.get("media"):
            record["media"] = question_data["media"]
        question_records.append(record)
    return jsonify(question_records)


@app.route("/api/scores")
def api_scores():
    return jsonify(get_top_scores())


@app.route("/question-media/<path:filename>")
def question_media(filename):
    return send_from_directory(MEDIA_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
