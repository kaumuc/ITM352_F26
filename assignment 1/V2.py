# Interactive Quiz system second version
# Make a list with the questions and correct answers

questions = [
    ("What is the capital of France?", "Paris"),
    ("What is the capital of Germany?", "Berlin"),
    ("What is the capital of Italy?", "Rome"),
    ("The Starry Night is a famous painting by which artist?", "Van Gogh")
]
for question, correct_answer in questions:
    answer = input(f"{question} ")
    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is '{correct_answer}', not {answer}.")