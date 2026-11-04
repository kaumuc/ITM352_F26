import time
from pathlib import Path

import pandas as pd


def load_csv(filepath):
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    print(f"Loading CSV file from: {path}")
    start_time = time.time()

    try:
        df = pd.read_csv(path, engine="pyarrow", on_bad_lines="skip")
        load_time = time.time() - start_time
        print(f"CSV file loaded successfully in {load_time:.2f} seconds.")
        print(f"Number of rows: {len(df)}")
        return df
    except Exception as exc:
        print(f"Error reading the CSV file: {exc}")
        return None


if __name__ == "__main__":
    csv_file = Path(__file__).with_name("sales_data_assn2.csv")
    sales_data = load_csv(csv_file)

    if sales_data is not None:
        print(sales_data.head(10))
#describe the dataframe field data types
    print("\nData types of the dataframe fields:")
    print(sales_data.dtypes)
