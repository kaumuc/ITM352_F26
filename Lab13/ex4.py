# Retrieve and analyze public vehicle license data from Chicago
import pandas as pd
from sodapy import Socrata

client = Socrata("data.cityofchicago.org", None)

# 1. Fetch the first 500 records from the passenger vehicle licenses dataset
json_file = "rr23-ymwb"
results = client.get(json_file, limit=500)

# 2. Convert the records to a DataFrame and inspect the first few rows
results_df = pd.DataFrame.from_records(results)
print("First few records:")
print(results_df.head())

# 3. Print the public vehicle numbers and their fuel sources
vehicles = results_df[["public_vehicle_number", "vehicle_fuel_source"]]
print("Public vehicles and fuel sources:")
print(vehicles)

# 4. Count vehicles grouped by fuel source
vehicles_by_fuel = (
    vehicles.groupby("vehicle_fuel_source")
    .size()
    .reset_index(name="number_of_vehicles")
)
print(vehicles_by_fuel)