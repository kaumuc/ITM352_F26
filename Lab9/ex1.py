# Open a file of names and print its type
from pathlib import Path

filename = Path(__file__).resolve().parent / "names.txt"

file_object = open(filename, "r")
print(type(file_object))
file_object.close