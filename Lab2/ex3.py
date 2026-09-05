# Ask for a decimal number, calculate its square, and print the result.
# Name: Cowmoo
# Date: Sept. 2, 2026

input_value = input("Enter a floating point number: ")
# Convert the input text to a number before performing arithmetic.
float_value = float(input_value)
squared_value = float_value ** 2

print("You entered:", float_value)
print("The square of the number you entered is:", squared_value)
