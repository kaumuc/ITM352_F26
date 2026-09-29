# Determine movie price. The rules are:
# Normal price is $14
# If someone is 65 or older, they pay $8
# If it is Tuesday the price is $10
# If it is a matine, the price is $5 for seniors and $8 otherwise

age = 67
weekday = "Tuesday"
matinee = True

if matinee and age >= 65:
	price = 5
elif matinee:
	price = 8
elif age >= 65:
	price = 8
elif weekday.lower() == "tuesday":
	price = 10
else:
	price = 14

print(f"Age: {age}")
print(f"Weekday: {weekday}")
print(f"Matinee: {matinee}")
print(f"Price: ${price}")
