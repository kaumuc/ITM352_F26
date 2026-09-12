"""Temperature conversion using functions passed as arguments."""


def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def celsius_to_kelvin(celsius):
    return celsius + 273.15


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def fahrenheit_to_kelvin(fahrenheit):
    return celsius_to_kelvin(fahrenheit_to_celsius(fahrenheit))


def kelvin_to_fahrenheit(kelvin):
    return celsius_to_fahrenheit(kelvin_to_celsius(kelvin))


def convert_temperature(temperature, conversion_function):
    """Use the conversion function passed as an argument."""
    return conversion_function(temperature)


# The conversion function is passed directly instead of selected by input.
print("25 C to Fahrenheit:", convert_temperature(25, celsius_to_fahrenheit))
print("77 F to Celsius:", convert_temperature(77, fahrenheit_to_celsius))
print("25 C to Kelvin:", convert_temperature(25, celsius_to_kelvin))
print("298.15 K to Celsius:", convert_temperature(298.15, kelvin_to_celsius))
print("32 F to Kelvin:", convert_temperature(32, fahrenheit_to_kelvin))
print("273.15 K to Fahrenheit:", convert_temperature(273.15, kelvin_to_fahrenheit))

# Assessment:
# Pros: This design is flexible, reusable, and easy to extend with a new
# conversion function. convert_temperature does not need to know the details
# of every conversion.
#
# Cons: The caller must know which conversion function to pass, and it is
# possible to pass the wrong function for the temperature's unit. The code
# can also be less familiar than calling a fixed conversion function directly.
#
# I would use this design when another part of a program chooses the conversion
# dynamically, such as a menu, button, or event. For a small program with only
# a few known conversions, individual fixed conversion functions are simpler.
#
# Copilot's assessment agrees that passing a function makes the code flexible
# and reusable, while fixed functions are easier to read for simple cases.
# My additional concern is that the caller can accidentally pass a mismatched
# conversion function, such as passing fahrenheit_to_celsius for Celsius input.
