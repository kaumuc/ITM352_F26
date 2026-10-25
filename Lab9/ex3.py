# Read taxi_1000.csv and calculate the total of all fares, average fare,
# and max trip distance.
import csv
from pathlib import Path

filename = Path(__file__).resolve().parents[1] / "taxi_1000.csv"

with open(filename, 'r', newline='') as file:
    csv_reader = csv.DictReader(file)

    total_fare = 0.0
    max_distance = 0.0
    data_rows = 0

    for row in csv_reader:
        fare = float(row['Fare'])
        distance = float(row['Trip Miles'])

        total_fare += fare
        if distance > max_distance:
            max_distance = distance

        data_rows += 1

average_fare = total_fare / data_rows if data_rows > 0 else 0.0

print(f"Total Fare: ${total_fare:.2f}")
print(f"Average Fare: ${average_fare:.2f}")
print(f"Max Trip Distance: {max_distance:.2f} miles")