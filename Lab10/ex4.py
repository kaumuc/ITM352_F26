from pathlib import Path

import pandas as pd

json_path = Path(__file__).with_name("Taxi_Trips.json")
df = pd.read_json(json_path)

print("Summary statistics:")
print(df.describe())

print("\nMedian:")
print(df.median(numeric_only=True))