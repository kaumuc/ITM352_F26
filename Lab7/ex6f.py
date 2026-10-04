

data = ("hello", "10", "goodbye", 3, "goodnight", 5)

user_input = input("Enter a value to append to the tuple: ")

try:
    data.append(user_input)
except AttributeError:
    data = list(data)
    data.append(user_input)
    data = tuple(data)

print(data)