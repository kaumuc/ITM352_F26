from pathlib import Path

import pandas as pd

csv_path = Path(__file__).with_name("homes_data.csv")
homes_df = pd.read_csv(csv_path)

large_properties = homes_df.loc[homes_df["units"] >= 500].drop(
    columns=["id", "block", "lot", "easement"]
)

print("First 10 properties with at least 500 units:")
print(large_properties.head(10))

print("\nData types before cleaning:")
print(large_properties.dtypes)

cleaned_properties = large_properties.copy()
cleaned_properties["borough"] = cleaned_properties["borough"].astype("category")

numeric_columns = [
    "units",
    "land_sqft",
    "gross_sqft",
    "year_built",
    "sale_price",
]
for column in numeric_columns:
    cleaned_properties[column] = pd.to_numeric(
        cleaned_properties[column], errors="coerce"
    )

print("\nData types after cleaning:")
print(cleaned_properties.dtypes)

print("\nCleaned properties:")
print(cleaned_properties)