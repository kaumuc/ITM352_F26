

import numpy as np
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

for column in ("quantity", "unit_price"):
    numeric_values = pd.to_numeric(sales_df[column], errors="coerce")
    invalid_values = sales_df[column].notna() & numeric_values.isna()
    if invalid_values.any():
        print(
            f"Warning: {invalid_values.sum()} non-numeric value(s) in "
            f"{column} were converted to missing values."
        )
    sales_df[column] = numeric_values

sales_df["sales"] = sales_df["quantity"] * sales_df["unit_price"]

sales_pivot = pd.pivot_table(
    sales_df,
    values="sales",
    index="sales_region",
    columns="order_type",
    aggfunc=lambda values: np.sum(values.dropna().to_numpy()),
    margins=True,
)

pd.set_option("display.max_columns", None)
print("Sales by region and order type:")
print(sales_pivot)
