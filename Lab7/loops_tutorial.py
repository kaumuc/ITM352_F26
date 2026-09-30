"""A beginner-friendly introduction to Python for loops.

Use a for loop to repeat an action for each item in a sequence, or to repeat
an action a known number of times. Use a while loop when repetition depends on
a condition and you do not know in advance how many times it will repeat.
"""

# Strings: the loop variable contains each character, one at a time.
print("\nString characters:")
for character in "Python":
	print(character)

# Grades: use if/elif/else to choose a letter grade for each score.
print("\nLetter grades:")
scores = [55, 68, 74, 86, 93]
for score in scores:
	if score >= 90:
		letter_grade = "A"
	elif score >= 80:
		letter_grade = "B"
	elif score >= 70:
		letter_grade = "C"
	elif score >= 60:
		letter_grade = "D"
	else:
		letter_grade = "F"
	print(f"{score}: {letter_grade}")

# Count from 1 through 10. The stop value in range() is not included.
print("\nCount from 1 to 10:")
for number in range(1, 11):
	print(number)

# Count backwards from 10 through 1 with a step of -1.
print("\nCount backwards:")
for number in range(10, 0, -1):
	print(number)

# Count by 2s from 2 through 10.
print("\nCount by 2s:")
for number in range(2, 11, 2):
	print(number)

# Loop through a list when you want to process each student.
print("\nStudents:")
students = ["Maya", "Noah", "Ava"]
for student in students:
	print(f"Hello, {student}!")

# Use enumerate() when you need each item's position as well as its value.
print("\nNumbered student list:")
for position, student in enumerate(students, start=1):
	print(f"{position}. {student}")

# Use split() to loop through the words in a sentence.
print("\nSentence words:")
sentence = "Loops process words one at a time"
for word in sentence.split():
	print(word)

# Use continue to skip grades below 80 and process the remaining students.
print("\nStudent grades 80 or higher:")
grades = {"Maya": 92, "Noah": 78, "Ava": 85}
for student, grade in grades.items():
	if grade < 80:
		continue
	print(f"{student}: {grade}")

# Use while when the condition determines how long to repeat.
print("\nWhile loop with a condition:")
number = 1
while number <= 3:
	print(number)
	number += 1

# This guessing game uses input and an indefinite loop that ends with break.
import random

print("\nGuessing game:")
secret_number = random.randint(1, 10)
while True:
	guess = int(input("Guess a number from 1 to 10: "))
	if guess < secret_number:
		print("Too low. Try again.")
	elif guess > secret_number:
		print("Too high. Try again.")
	else:
		print("You guessed it!")
		# break exits the loop as soon as the player guesses correctly.
		break
