import time

import pandas as pd


# AI use: Copilot helped draft this loader from the assignment's R1 instructions.
sales_data_url = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"

required_columns = [
    "sales_region",
    "order_type",
    "customer_state",
    "customer_type",
    "quantity",
    "unit_price",
    "product_category",
    "produce_name",
    "employee_id",
]


def load_csv(filepath):
    """Load sales data and report its size, columns, and missing fields."""
    print(f"Loading sales data from: {filepath}")
    start_time = time.time()

    try:
        data = pd.read_csv(filepath)
    except (OSError, ValueError, pd.errors.ParserError) as error:
        print(f"Could not load the sales data: {error}")
        return None

    data = data.fillna(0)

    print(f"Sales data loaded successfully in {time.time() - start_time:.2f} seconds.")
    print(f"Number of rows: {len(data)}")
    print("Available columns:", ", ".join(data.columns))

    missing_columns = [
        column for column in required_columns if column not in data.columns
    ]
    if missing_columns:
        print("Warning: missing required fields:", ", ".join(missing_columns))
        print("Some dashboard analytics may not work.")

    return data


def main():
    load_csv(sales_data_url)


if __name__ == "__main__":
    main()