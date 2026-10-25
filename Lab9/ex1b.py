# Open a file using "with"
from pathlib import Path

filename = Path(__file__).resolve().parent / "names.txt"

with open(filename, "r") as file_object:
    print(type(file_object))

print("File is closed:", file_object.closed)