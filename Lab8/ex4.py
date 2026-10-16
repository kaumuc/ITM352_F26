# Algorithm:
# 1. Use the absolute values of the two whole numbers.
# 2. Divide the first number by the second and find the remainder.
# 3. Replace the first number with the second and the second with the
#    remainder.
# 4. Repeat until the remainder is 0. The first number is the GCD.

def gcd(a, b):
    a = abs(a)
    b = abs(b)

    while b != 0:
        a, b = b, a % b

    return a


try:
    number1 = int(input("Enter the first whole number: "))
    number2 = int(input("Enter the second whole number: "))
except ValueError:
    print("Please enter whole numbers.")
    raise SystemExit(1)

if number1 == 0 and number2 == 0:
    print("The GCD of 0 and 0 is undefined.")
    raise SystemExit(1)

print("The GCD is", gcd(number1, number2))
