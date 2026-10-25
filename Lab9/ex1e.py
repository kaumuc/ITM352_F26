# Read the entire file using readlines()
from pathlib import Path

filename = Path(__file__).resolve().parent / "names.txt"

with open(filename, "r") as file_object:
    names = file_object.readlines()
    print(f"Number of names: {len(names)}")
    for name in names:
        print(name.strip())
        