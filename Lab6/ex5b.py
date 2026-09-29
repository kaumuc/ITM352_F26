def celsius_to_fahrenheit(celsius):
	assert celsius >= -273.15, "Temperature cannot be below absolute zero"
	return (celsius * 9 / 5) + 32


assert celsius_to_fahrenheit(0) == 32, "0 degrees Celsius should be 32 degrees Fahrenheit"
assert celsius_to_fahrenheit(100) == 212, "100 degrees Celsius should be 212 degrees Fahrenheit"
