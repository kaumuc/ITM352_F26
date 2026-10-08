# First example: guessing from 0 to 100
import random

secret_number = random.randint(0, 100)

print("I'm thinking of a number from 0 to 100.")

while True:
    try:
        guess = int(input("Enter your guess: "))
    except ValueError:
        print("Please enter a whole number.")
        continue

    if guess < 0 or guess > 100:
        print("Your guess must be between 0 and 100.")
    elif guess < secret_number:
        print("Too low!")
    elif guess > secret_number:
        print("Too high!")
    else:
        print("You guessed it!")
        break

# Second example: guessing using min and max variables

min = 1
max = 100

secret_number = random.randint(min, max)

print(f"I'm thinking of a number from {min} to {max}.")

while True:
    try:
        guess = int(input("Enter your guess: "))
    except ValueError:
        print("Please enter a whole number.")
        continue

    if guess < min or guess > max:
        print(f"Your guess must be between {min} and {max}.")
    elif guess < secret_number:
        print("Too low!")
    elif guess > secret_number:
        print("Too high!")
    else:
        print("You guessed it!")
        break