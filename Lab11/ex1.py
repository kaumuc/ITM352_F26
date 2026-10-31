

import pandas as pd


SALES_DATA_URL = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

try:
    sales_df = pd.read_csv(
        SALES_DATA_URL,
        engine="pyarrow",
        dtype_backend="pyarrow",
        on_bad_lines="skip",
    )
except (ImportError, OSError, ValueError) as error:
    print(f"Unable to load sales_data.csv from Google Drive: {error}")
    raise

print("First 5 rows:")
print(sales_df.head())

print("\nColumn data types:")
print(sales_df.dtypes)
