from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

ASSIGNMENT_DIR = Path(__file__).resolve().parent
EVIDENCE_PATH = ASSIGNMENT_DIR / "assignment_1_testing_evidence.txt"


def load_module(module_name: str, file_name: str):
    """Import an assignment script by path without starting its quiz."""
    file_path = ASSIGNMENT_DIR / file_name
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {file_name}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AssignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v8 = load_module("assignment_v8", "v8.py")
        cls.v9 = load_module("assignment_v9", "v9.py")
        cls.v11 = load_module("assignment_v11", "v11.py")
        cls.legacy_questions = json.loads(
            (ASSIGNMENT_DIR / "questions.json").read_text(encoding="utf-8")
        )
        cls.final_questions = cls.v11.load_questions()

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.module_file = Path(self.temp_dir.name) / "quiz.py"

    def use_temporary_score_history(self, *modules):
        for module in modules:
            self.patch_module_file(module)

    def patch_module_file(self, module):
        patcher = patch.object(module, "__file__", str(self.module_file))
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_legacy_question_data_remains_text_only(self):
        self.assertGreaterEqual(len(self.legacy_questions), 5)
        self.assertTrue(
            all(isinstance(answers, list) for answers in self.legacy_questions.values())
        )
        self.assertTrue(all(len(answers) >= 2 for answers in self.legacy_questions.values()))

    def test_v11_question_data_contains_text_and_three_media_questions(self):
        media_questions = [
            (question, data)
            for question, data in self.final_questions.items()
            if isinstance(data, dict)
        ]
        text_questions = [
            data
            for data in self.final_questions.values()
            if isinstance(data, list)
        ]

        self.assertEqual(len(media_questions), 3)
        self.assertGreaterEqual(len(text_questions), 5)
        self.assertTrue(all(len(data) >= 2 for data in text_questions))

        for question, data in media_questions:
            with self.subTest(question=question):
                self.assertEqual(data["media"]["type"], "image")
                self.assertTrue(data["answers"])
                media_path = ASSIGNMENT_DIR / data["media"]["source"]
                self.assertTrue(media_path.is_file(), f"Missing media file: {media_path}")

    def test_v11_selection_includes_all_available_media_and_fills_quiz(self):
        media_names = {
            question
            for question, data in self.final_questions.items()
            if isinstance(data, dict)
        }

        for _ in range(10):
            selected = self.v11.select_questions(self.final_questions)
            selected_names = [question for question, _ in selected]
            self.assertEqual(len(selected), self.v11.NUM_QUESTIONS_PER_QUIZ)
            self.assertEqual(len(selected_names), len(set(selected_names)))
            self.assertTrue(media_names.issubset(selected_names))

    def test_question_timer_returns_correctness_and_elapsed_time(self):
        with patch.object(
            self.v11.random, "sample", side_effect=lambda items, k: list(items[:k])
        ), patch("builtins.input", return_value="a"), patch.object(
            self.v11.time, "perf_counter", side_effect=[10.0, 13.25]
        ), contextlib.redirect_stdout(io.StringIO()):
            result = self.v11.ask_question(1, "Example?", ["yes", "no"])

        self.assertEqual(result, (True, 3.25))

    def test_question_retries_invalid_choice_and_marks_incorrect_answer(self):
        with patch.object(
            self.v11.random, "sample", side_effect=lambda items, k: list(items[:k])
        ), patch("builtins.input", side_effect=["z", "b"]), patch.object(
            self.v11.time, "perf_counter", side_effect=[1.0, 8.0]
        ), contextlib.redirect_stdout(io.StringIO()) as output:
            result = self.v11.ask_question(1, "Example?", ["yes", "no"])

        self.assertEqual(result, (False, 7.0))
        self.assertIn("Invalid choice", output.getvalue())

    def test_question_stops_cleanly_when_input_ends(self):
        with patch.object(
            self.v11.random, "sample", side_effect=lambda items, k: list(items[:k])
        ), patch("builtins.input", side_effect=EOFError), contextlib.redirect_stdout(
            io.StringIO()
        ):
            result = self.v11.ask_question(1, "Example?", ["yes", "no"])

        self.assertIsNone(result)

    def test_fast_correct_answer_earns_bonus_and_saves_full_score(self):
        self.use_temporary_score_history(self.v11)
        quiz_data = {
            "Fast text question?": ["yes", "no"],
            "Fast media question?": {
                "answers": ["Guitar", "Violin"],
                "media": {"type": "image", "source": "media/guitar.svg"},
            },
        }
        selected = list(quiz_data.items())
        asked = []

        def fake_ask(number, question, answers, media=None):
            asked.append((number, question, answers, media))
            return True, 2.0

        with patch.object(
            self.v11, "load_questions", return_value=quiz_data
        ), patch.object(
            self.v11, "select_questions", return_value=selected
        ), patch.object(
            self.v11, "ask_question", side_effect=fake_ask
        ), contextlib.redirect_stdout(io.StringIO()) as output:
            self.v11.run_quiz()

        score_history = (Path(self.temp_dir.name) / "score_history.txt").read_text(
            encoding="utf-8"
        )
        self.assertEqual(asked[0][0], 1)
        self.assertEqual(asked[0][2], ["yes", "no"])
        self.assertIsNone(asked[0][3])
        self.assertEqual(asked[1][0], 2)
        self.assertEqual(asked[1][2], ["Guitar", "Violin"])
        self.assertEqual(asked[1][3], quiz_data["Fast media question?"]["media"])
        self.assertIn("4 points", output.getvalue())
        self.assertIn("New high score!", output.getvalue())
        self.assertIn("4 points (2/2 correct, 2 bonus)", score_history)

    def test_slow_correct_answer_does_not_earn_bonus(self):
        self.use_temporary_score_history(self.v11)
        quiz_data = {"Question?": ["yes", "no"]}

        with patch.object(
            self.v11, "load_questions", return_value=quiz_data
        ), patch.object(
            self.v11, "select_questions", return_value=list(quiz_data.items())
        ), patch.object(
            self.v11,
            "ask_question",
            return_value=(True, self.v11.FAST_ANSWER_SECONDS + 0.1),
        ), patch.object(
            self.v11, "get_high_score", return_value=100
        ), contextlib.redirect_stdout(io.StringIO()) as output:
            self.v11.run_quiz()

        score_history = (Path(self.temp_dir.name) / "score_history.txt").read_text(
            encoding="utf-8"
        )
        self.assertIn("earned 0 bonus points", output.getvalue())
        self.assertNotIn("New high score!", output.getvalue())
        self.assertIn("1 point (1/1 correct, 0 bonus)", score_history)

    def test_legacy_and_current_history_formats_are_read_for_high_score(self):
        self.use_temporary_score_history(self.v8, self.v9, self.v11)
        history_path = Path(self.temp_dir.name) / "score_history.txt"
        history_path.write_text(
            "2026-01-01 00:00:00 - 3/5\n"
            "2026-01-02 00:00:00 - 4 points (3/5 correct, 1 bonus)\n",
            encoding="utf-8",
        )

        self.assertEqual(self.v9.get_high_score(), 3)
        self.assertEqual(self.v11.get_high_score(), 4)

    def test_older_version_score_history_is_still_recorded(self):
        self.use_temporary_score_history(self.v8, self.v9)
        with contextlib.redirect_stdout(io.StringIO()):
            self.v8.write_score_history(3, 5)

        history_path = Path(self.temp_dir.name) / "score_history.txt"
        self.assertIn("3/5", history_path.read_text(encoding="utf-8"))
        self.assertEqual(self.v9.get_high_score(), 3)

    def test_local_image_and_video_url_open_in_browser(self):
        image_media = {
            "type": "image",
            "source": "media/guitar.svg",
        }
        video_url = "https://example.org/sample.mp4"

        with patch.object(self.v11.webbrowser, "open", return_value=True) as browser:
            with contextlib.redirect_stdout(io.StringIO()):
                self.v11.open_question_media(image_media)
            self.assertTrue(browser.call_args.args[0].startswith("file:"))

        with patch.object(self.v11.webbrowser, "open", return_value=True) as browser:
            with contextlib.redirect_stdout(io.StringIO()):
                self.v11.open_question_media({"type": "video", "source": video_url})
            self.assertEqual(browser.call_args.args[0], video_url)

    def test_invalid_or_missing_media_reports_an_error(self):
        with self.assertRaises(ValueError):
            self.v11.open_question_media({"type": "audio", "source": "song.mp3"})

        with self.assertRaises(FileNotFoundError):
            self.v11.open_question_media(
                {"type": "image", "source": "media/not_a_real_image.png"}
            )

        with patch.object(self.v11.webbrowser, "open", return_value=False):
            with self.assertRaises(RuntimeError):
                self.v11.open_question_media(
                    {"type": "video", "source": "https://example.org/sample.mp4"}
                )


def run_tests() -> tuple[list[str], bool]:
    report = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AssignmentTests)
    result = unittest.TextTestRunner(stream=report, verbosity=2).run(suite)

    lines = [
        "Assignment 1 Testing Evidence",
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Python: {sys.version.split()[0]}",
        f"Target directory: {ASSIGNMENT_DIR}",
        "",
        report.getvalue().rstrip(),
        "",
        f"Summary: {result.testsRun - len(result.failures) - len(result.errors)}/"
        f"{result.testsRun} tests passed",
    ]
    EVIDENCE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return lines, result.wasSuccessful()


if __name__ == "__main__":
    test_report, tests_passed = run_tests()
    print("\n".join(test_report))
    raise SystemExit(0 if tests_passed else 1)
