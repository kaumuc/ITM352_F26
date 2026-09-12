# Import the requested functions directly from HandyMath.py.
from HandyMath import max, min
from HandyMath import exponent, midpoint, squareroot

# Ask the user for two numbers.
first_number = float(input("Enter the first number: "))
second_number = float(input("Enter the second number: "))

# Display the requested calculations using f-strings.
print(f"The midpoint is {midpoint(first_number, second_number)}.")
print(
    f"The square root of the square of the first number is "
    f"{squareroot(first_number ** 2)}."
)
print(
    f"The first number raised to the second number is "
    f"{exponent(first_number, second_number)}."
)
print(f"The maximum is {max(first_number, second_number)}.")
print(f"The minimum is {min(first_number, second_number)}.")