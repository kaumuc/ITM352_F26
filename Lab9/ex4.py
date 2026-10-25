# Read taxi_1000.csv and calculate fare statistics for fares greater than $10.
import csv
from pathlib import Path

filename = Path(__file__).resolve().parents[1] / "taxi_1000.csv"

total_fare = 0.0
max_distance = 0.0
qualifying_rows = 0

with open(filename, 'r', newline='') as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        fare = float(row['Fare'])
        if fare > 10:
            distance = float(row['Trip Miles'])

            total_fare += fare
            if distance > max_distance:
                max_distance = distance

            qualifying_rows += 1

average_fare = total_fare / qualifying_rows if qualifying_rows > 0 else 0.0

print(f"Total Fare: ${total_fare:.2f}")
print(f"Average Fare: ${average_fare:.2f}")
print(f"Max Trip Distance: {max_distance:.2f} miles")