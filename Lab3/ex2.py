# this code calculates the midpoint of two numbers

def midpoint(first_number, second_number):
    return (first_number + second_number) / 2

another_problem = "y"

while another_problem.lower() == "y":
    first = float(input("Enter the first number: "))
    second = float(input("Enter the second number: "))

    print("The midpoint is:", midpoint(first, second))

    another_problem = input("Do you have another problem? (y/n): ")

print("Goodbye:)")

