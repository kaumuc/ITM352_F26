# Algorithm:
# 1. Store the given numbers in an array.
# 2. Ask the user for the number to search for.
# 3. Check each array element against the target number.
# 4. If a match is found, report that the number exists and stop searching.
# 5. If the end of the array is reached without a match, report that it does
#    not exist.

searchMe = [2, 5, 7, 11, 15, 22, 27, 30, 34, 41, 55, 57, 58, 60, 77]

try:
    target = int(input("Enter a number to search for: "))
except ValueError:
    print("Please enter a whole number.")
    raise SystemExit(1)

found = False
for number in searchMe:
    if number == target:
        found = True
        break

if found:
    print(f"{target} exists in the array.")
else:
    print(f"{target} does not exist in the array.")
