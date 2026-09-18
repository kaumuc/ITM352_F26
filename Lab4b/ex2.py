# Properly format an inputed name  in title case

raw_name = input("Enter your full name: ")

stripped_name = raw_name.strip(" rka") 
print("stripped name:", stripped_name)

title_case_name = stripped_name.title()
print('Formatted name in title case:', title_case_name)

