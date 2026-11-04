from pathlib import Path

import pandas as pd

csv_file = Path(__file__).with_name("sales_data_assn2.csv")
outfile = Path(__file__).with_name("sales_data_test.csv")

try:
    df = pd.read_csv(csv_file, engine="pyarrow", on_bad_lines="skip")
    df.head(10).to_csv(outfile, index=False)
    print(f"First 10 rows of {csv_file.name} saved to {outfile.name}")
    print(df.head())
except Exception as exc:
    print(f"Error reading the CSV file: {exc}")
