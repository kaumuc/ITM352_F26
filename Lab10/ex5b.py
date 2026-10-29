from pathlib import Path

import pandas as pd

csv_path = Path(__file__).with_name("homes_data.csv")
homes_df = pd.read_csv(csv_path)

large_properties = homes_df.loc[homes_df["units"] >= 500].drop(
    columns=["id", "block", "lot", "easement"]
)

print(large_properties.head(10))