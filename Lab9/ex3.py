# Read the 1,000 lines of taxi data from taxi_1000.csv and calculate:
# - the total of all fares
# - the average of those fares
# - the maximum trip distance based on the Trip Miles field

import csv
import os

csv_filename = os.path.join(os.path.dirname(__file__), "..", "taxi_1000.csv")
total_fare = 0.0
max_distance = 0.0
trip_count = 0

with open(csv_filename, "r") as csv_file:
    reader = csv.reader(csv_file)
    headers = next(reader)
    fare_index = headers.index("Fare")
    miles_index = headers.index("Trip Miles")

    for row in reader:
        fare = float(row[fare_index])
        distance = float(row[miles_index])
        total_fare += fare
        trip_count += 1

        if distance > max_distance:
            max_distance = distance

average_fare = total_fare / trip_count

print(f"Taxi trips read: {trip_count}")
print(f"Total fares: ${total_fare:.2f}")
print(f"Average fare: ${average_fare:.2f}")
print(f"Maximum trip distance: {max_distance:g} miles")