farenheight_input = input("Enter temperature in Fahrenheit: ")
farenheight_float = float(farenheight_input)

celsius_value = (farenheight_float - 32) * 5 / 9

celsius_value = round(celsius_value, 2)

print("You entered:", farenheight_float)
print("The temperature in Celsius is:", celsius_value)
