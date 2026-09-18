first = input ("Enter your first name: ")
middle_intial = input ("Enter your middle initial: ")
last = input ("Enter your last name: ")

full_name = first + " " + middle_intial + ". " + last
print ("Your full name is: ", full_name)

print(f"your full name using F-strings is: {first} {middle_intial}. {last}")
print("your full name using percent formatting is: %s %s %s" % (first, middle_intial, last))
print("your full name using .format() is: {} {}. {}".format(first, middle_intial, last))
print("your full name using list joins is: " + " ".join([first, middle_intial + ".", last]))
name_parts = [first, middle_intial + ".", last]
print("your full name using .format() with list unpacking is: {} {} {}".format(*name_parts))