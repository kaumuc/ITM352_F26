def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


# Map operations to functions
operations = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide
}

while True:
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        operation = input("Choose an operation (+, -, *, /): ")

        if operation not in operations:
            print("Invalid operation. Please choose +, -, *, or /.")
            continue

        result = operations[operation](num1, num2)
        print(f"Result: {result}")

        again = input("Would you like to perform another calculation? (y/n): ").lower()
        if again != 'y':
            print("Goodbye!")
            break

    except ValueError:
        print("Invalid input. Please enter numeric values.")
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
    except EOFError:
        print("\nInput ended. Exiting calculator.")
        break
