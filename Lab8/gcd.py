# Tips:
# - The % operator gives the remainder after division.
# - Repeat the steps using the previous divisor and remainder.
# - When the remainder becomes 0, the current divisor is the GCD.
# - Try 18 and 12 as a test: the GCD should be 6.

def gcd(a, b):
    a = abs(a)
    b = abs(b)

    while b != 0:
        remainder = a % b
        a = b
        b = remainder

    return a


number1 = int(input("Enter the first whole number: "))
number2 = int(input("Enter the second whole number: "))

print("The GCD is", gcd(number1, number2))