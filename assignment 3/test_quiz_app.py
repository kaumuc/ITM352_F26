"""Route tests using Flask's test client without opening a browser."""

# AI note: I asked AI how to test Flask routes. It taught me to use the test client
# to make requests without launching a browser.

import tempfile
import unittest
from pathlib import Path

import finalversion


class QuizAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        finalversion.LEADERBOARD_FILE = Path(self.temp_dir.name) / "scores.json"
        finalversion.save_scores([])
        finalversion.app.config["TESTING"] = True
        self.client = finalversion.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def answer_question(self, question_number, answer_correctly=True):
        with self.client.session_transaction() as state:
            question = state["question_order"][question_number]
            question_data = finalversion.load_questions()[question]
            answers = (
                question_data["answers"]
                if isinstance(question_data, dict)
                else question_data
            )
            options = state["answer_options"][question]
            answer = answers[0]
            if not answer_correctly:
                answer = next(option for option in options if option != answers[0])

        response = self.client.post("/quiz", data={"answer": answer})
        self.assertEqual(response.status_code, 302)
        self.client.get(response.location)
        return self.client.post("/next")

    def complete_quiz(self):
        self.client.post("/start")
        for question_number in range(5):
            self.answer_question(
                question_number,
                answer_correctly=question_number != 0,
            )

    def test_api_returns_questions_without_answer_key(self):
        response = self.client.get("/api/questions")

        self.assertEqual(response.status_code, 200)
        records = response.get_json()
        self.assertEqual(len(records), len(finalversion.load_questions()))
        self.assertTrue(all(record["options"] for record in records))
        self.assertTrue(all("correct_answer" not in record for record in records))

    def test_invalid_answer_does_not_advance_the_quiz(self):
        self.client.post("/start")

        response = self.client.post("/quiz", data={"answer": "not-an-option"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please choose one of the answer options.", response.data)
        with self.client.session_transaction() as state:
            self.assertEqual(state["question_number"], 0)

    def test_quiz_review_and_score_submission(self):
        self.complete_quiz()

        result = self.client.get("/result")
        self.assertIn(b"4 out of 5", result.data)
        review = self.client.get("/review")
        self.assertIn(b"Your answer:", review.data)
        self.assertEqual(
            self.client.post("/submit-score", data={"name": "Test Player"}).status_code,
            302,
        )
        self.assertEqual(
            self.client.get("/api/scores").get_json(),
            [{"name": "Test Player", "score": 4}],
        )

    def test_score_name_is_validated(self):
        self.complete_quiz()

        response = self.client.post("/submit-score", data={"name": " "})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Enter a name between 1 and 40 characters.", response.data)
        self.assertEqual(self.client.get("/api/scores").get_json(), [])

    def test_scores_api_is_sorted_and_limited_to_ten(self):
        finalversion.save_scores(
            [
                {"name": f"Player {score}", "score": score}
                for score in range(12)
            ]
        )

        scores = self.client.get("/api/scores").get_json()

        self.assertEqual(len(scores), 10)
        self.assertEqual(scores[0]["score"], 11)
        self.assertEqual(scores[-1]["score"], 2)

    def test_responsive_styles_are_enabled(self):
        self.assertIn(b"style.css", self.client.get("/").data)


if __name__ == "__main__":
    unittest.main()
