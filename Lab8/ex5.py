# Algorithm:
# 1. Ask the user to enter a string.
# 2. Set one position to the start of the string and another to the end.
# 3. Compare the characters at those two positions.
# 4. If they do not match, the string is not a palindrome.
# 5. Move the positions toward the middle and repeat.
# 6. If all the compared characters match, the string is a palindrome.

text = input("Enter a string: ")
left = 0
right = len(text) - 1
is_palindrome = True

while left < right:
    if text[left] != text[right]:
        is_palindrome = False
        break
    left += 1
    right -= 1

if is_palindrome:
    print("The string is a palindrome.")
else:
    print("The string is not a palindrome.")
