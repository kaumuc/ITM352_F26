# Open a file and read its contents
from pathlib import Path

filename = Path(__file__).resolve().parent / "names.txt"

with open(filename, "r") as file_object:
    contents = file_object.read()
    print(contents)
    contents_list = contents.splitlines()
    print(f"Number of names: {len(contents_list)}")
    for name in contents_list:
        print(name)