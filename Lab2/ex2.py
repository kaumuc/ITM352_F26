# Ask the user to enter their birth year. Calculate their age based in the current year and print it out.
# Name: Cowmoo
# Date: Sept. 2, 2026
birth_year = input("Please enter your birth year: ")
current_year = 2026
age = current_year - int(birth_year)

print(f"You entered: {birth_year}")
print(f"Your age is: {age}")