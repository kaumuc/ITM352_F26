#This program prompts the user to enter a string, calculates the length of that string, and then prints both the entered string and its length.
# Name: Cowmoo
# Date: Sept. 4, 2026

user_string = input("Please enter a string: ")
string_length = len(user_string)

print("You entered:", user_string)
print("The length of the string you entered is:", string_length)

if string_length > 0:
	print("The last character is:", user_string[len(user_string) - 1])
else:
	print("You entered an empty string, so there is no last character.")