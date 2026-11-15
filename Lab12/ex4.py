from datetime import datetime
import json
import os
from pathlib import Path
import random
import time

from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "local-quiz-development-key")

ASSIGNMENT_DIR = Path(__file__).resolve().parent.parent / "assignment 1"
QUESTIONS_PATH = ASSIGNMENT_DIR / "final_questions.json"
MEDIA_DIR = ASSIGNMENT_DIR / "media"
HISTORY_PATH = ASSIGNMENT_DIR / "score_history.txt"
NUM_QUESTIONS_PER_QUIZ = 5
FAST_ANSWER_SECONDS = 5.0


def load_questions():
    with QUESTIONS_PATH.open("r", encoding="utf-8") as question_file:
        return json.load(question_file)


def select_questions(questions):
    question_items = list(questions.items())
    num_questions = min(NUM_QUESTIONS_PER_QUIZ, len(question_items))
    media_items = [
        item
        for item in question_items
        if isinstance(item[1], dict) and item[1].get("media") is not None
    ]

    if media_items and num_questions:
        selected = random.sample(media_items, k=min(len(media_items), num_questions))
        selected_names = {item[0] for item in selected}
        remaining = [item for item in question_items if item[0] not in selected_names]
        selected.extend(
            random.sample(remaining, k=num_questions - len(selected))
        )
        return random.sample(selected, k=len(selected))

    return random.sample(question_items, k=num_questions)


def get_answers(question_data):
    if isinstance(question_data, dict):
        return question_data["answers"]
    return question_data


def get_high_score():
    if not HISTORY_PATH.exists():
        return 0

    high_score = 0
    with HISTORY_PATH.open("r", encoding="utf-8") as history_file:
        for line in history_file:
            score_part = line.strip().split(" - ", 1)[-1]
            score_text = score_part.split()[0].split("/", 1)[0]
            try:
                high_score = max(high_score, int(score_text))
            except (ValueError, IndexError):
                continue
    return high_score


def write_score_history(total_score, total_questions, num_correct, bonus_points):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    score_label = "point" if total_score == 1 else "points"
    result_line = (
        f"{timestamp} - {total_score} {score_label} "
        f"({num_correct}/{total_questions} correct, {bonus_points} bonus)\n"
    )
    with HISTORY_PATH.open("a", encoding="utf-8") as history_file:
        history_file.write(result_line)


def finish_quiz():
    num_correct = session["num_correct"]
    bonus_points = session["bonus_points"]
    total_score = num_correct + bonus_points
    total_questions = len(session["quiz_questions"])
    previous_high_score = get_high_score()

    write_score_history(
        total_score, total_questions, num_correct, bonus_points
    )
    session["quiz_result"] = {
        "num_correct": num_correct,
        "bonus_points": bonus_points,
        "total_score": total_score,
        "total_questions": total_questions,
        "new_high_score": total_score > previous_high_score,
    }


@app.route("/")
def index():
    return render_template(
        "quiz_index.html",
        num_questions=NUM_QUESTIONS_PER_QUIZ,
        fast_answer_seconds=FAST_ANSWER_SECONDS,
    )


@app.route("/start", methods=["POST"])
def start_quiz():
    questions = load_questions()
    selected_questions = select_questions(questions)
    if not selected_questions:
        abort(500, description="No quiz questions are available.")

    session.clear()
    session["quiz_questions"] = [question for question, _ in selected_questions]
    session["current_index"] = 0
    session["num_correct"] = 0
    session["bonus_points"] = 0
    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    question_list = session.get("quiz_questions")
    if not question_list:
        return redirect(url_for("index"))

    current_index = session["current_index"]
    if current_index >= len(question_list):
        return redirect(url_for("results"))

    questions = load_questions()
    question = question_list[current_index]
    question_data = questions[question]
    answers = get_answers(question_data)

    if request.method == "POST":
        answer = request.form.get("answer")
        if answer not in answers:
            return render_template(
                "quiz_question.html",
                question=question,
                answers=random.sample(answers, k=len(answers)),
                question_number=current_index + 1,
                total_questions=len(question_list),
                media=question_data.get("media")
                if isinstance(question_data, dict)
                else None,
                error="Choose one of the listed answers.",
            ), 400

        elapsed_time = time.time() - session.get("question_started_at", time.time())
        if answer == answers[0]:
            session["num_correct"] += 1
            if elapsed_time <= FAST_ANSWER_SECONDS:
                session["bonus_points"] += 1

        session["current_index"] += 1
        session.pop("question_started_at", None)
        if session["current_index"] >= len(question_list):
            finish_quiz()
            return redirect(url_for("results"))
        return redirect(url_for("quiz"))

    session.setdefault("question_started_at", time.time())
    return render_template(
        "quiz_question.html",
        question=question,
        answers=random.sample(answers, k=len(answers)),
        question_number=current_index + 1,
        total_questions=len(question_list),
        media=question_data.get("media")
        if isinstance(question_data, dict)
        else None,
        error=None,
    )


@app.route("/question-media/<path:filename>")
def question_media(filename):
    return send_from_directory(MEDIA_DIR, filename)


@app.route("/results")
def results():
    quiz_result = session.get("quiz_result")
    if quiz_result is None:
        return redirect(url_for("index"))
    return render_template("quiz_results.html", result=quiz_result)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")