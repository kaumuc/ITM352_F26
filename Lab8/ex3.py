# Algorithm:
# 1. Ask the user for the ending number, n.
# 2. Count from 1 through n.
# 3. For each number, print FizzBuzz if it is divisible by both 3 and 5,
#    Fizz if divisible by 3, Buzz if divisible by 5, or the number otherwise.

try:
    n = int(input("Enter a positive whole number: "))
except ValueError:
    print("Please enter a whole number.")
    raise SystemExit(1)

if n < 1:
    print("Please enter a number greater than 0.")
    raise SystemExit(1)

for number in range(1, n + 1):
    if number % 3 == 0 and number % 5 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz")
    elif number % 5 == 0:
        print("Buzz")
    else:
        print(number)
