#This function takes two numbers as input and returns their midpoint.
def midpoint(first_number, second_number):
    return (first_number + second_number) / 2

#this function takes a number as input and returns its square root.
def squareroot(number):
    return number ** 0.5

#this function takes two numbers as input and returns the larger of the two.
def max(first_number, second_number):
    return first_number if first_number > second_number else second_number

#this function takes two numbers as input and returns the smaller of the two.
def min(first_number, second_number):
    return first_number if first_number < second_number else second_number

#this function takes a base and an exponent as input and returns the result of raising the base to the power of the exponent.
def exponent(base, power):
    return base ** power


#This function applies a two-number function and describes the result.
def describe_function(x, y, function):
    return f"The function {function.__name__} {x},{y} = {function(x, y)}"