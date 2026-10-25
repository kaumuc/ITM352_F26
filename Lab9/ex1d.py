# Read a file of names one line at a time and print each name
from pathlib import Path

filename = Path(__file__).resolve().parent / "names.txt"

with open(filename, "r") as file_object:
    while (line := file_object.readline()):
        print(line.strip())
        