# Open names.txt and read its contents
# Append your own name at the end of the file without losing existing names
from pathlib import Path

filename = Path(__file__).resolve().parent / "names.txt"
new_name = "Clemente, Kaumualii"

with open(filename, "r") as file_object:
    contents_list = file_object.readlines()
    print("Before append:")
    print(contents_list)

if not any(name.strip() == new_name for name in contents_list):
    with open(filename, "a") as file_object:
        print(f"Appending {new_name} to the end of the file...")
        file_object.write(new_name + "\n")

with open(filename, "r") as file_object:
    print("\nEntire file contents:")
    print(file_object.read())