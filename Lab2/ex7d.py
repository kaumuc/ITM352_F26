#this program converts temperature from Fahrenheit to Celsius
# Name: Cowmoo
# Date: Sept. 4, 2026


def F_to_C(fahrenheit):
    celsius = (fahrenheit - 32) * 5 / 9
    rounded_celsius = round(celsius, 2)
    return rounded_celsius


farenheight_input = input("Enter temperature in Fahrenheit: ")
farenheight_float = float(farenheight_input)

celsius_value = F_to_C(farenheight_float)

print("You entered:", farenheight_float)
print("The temperature in Celsius is:", celsius_value)