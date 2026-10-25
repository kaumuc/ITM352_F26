# Read a file of quiz questions and save as a dictionary.
import json
from pathlib import Path

filename = Path(__file__).resolve().parent / "quiz_questions.json"
with open(filename, 'r') as file:
    questions = json.load(file)

print(questions)