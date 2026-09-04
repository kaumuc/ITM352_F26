# This program converts weight in pounds to kilograms
# Name: Cowmoo
# Date: Sept. 4, 2026

print("The weight in kilograms is:", float(input("enter weight in pounds: "))*0.453592)

kg_to_pounds = .453592
weight_in_pounds = input("Enter weight in pounds: ")
weight_in_pounds_float = float(weight_in_pounds)
weight_in_kilograms = weight_in_pounds_float * kg_to_pounds

print("you entered:", weight_in_pounds_float)
print("The weight in kilograms is:", weight_in_kilograms)