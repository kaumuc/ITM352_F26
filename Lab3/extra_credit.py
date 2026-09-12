"""Extra Credit: Functions as values and callback functions."""

from HandyMath import describe_function, exponent, max, min


def square(number):
	return number ** 2


def apply_function(numbers, function):
	"""Apply a callback function to every number in a list."""
	return [function(number) for number in numbers]


# 1. Functions can be stored in variables just like other values.
function_variable = square
print("Using a function stored in a variable:", function_variable(5))

# 2. Passing a function as an argument makes code more flexible.
# apply_function does not need to know what the callback does.
numbers = [1, 2, 3, 4]
print("Using square as a callback:", apply_function(numbers, square))

# The same helper can use different functions passed as arguments.
print(describe_function(8, 3, min))
print(describe_function(8, 3, max))
print(describe_function(8, 3, exponent))
