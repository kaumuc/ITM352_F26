import time

import pandas as pd


# I used AI to help explain the pivot table arguments, then checked the results
# with a small sample dataset.
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


def check_columns(data, columns):
    """Check that an analysis has the columns it needs."""
    missing_columns = [column for column in columns if column not in data.columns]
    if missing_columns:
        print("This analysis needs these columns:", ", ".join(missing_columns))
        return False
    return True


def show_first_rows(data):
    """Show the requested starting rows, all rows, or skip the preview."""
    while True:
        print(f"\nThere are {len(data)} rows available.")
        print("Enter a number to show rows, 'all' to show everything,")
        print("or press Enter to skip the preview.")
        choice = input("Your choice: ").strip().lower()

        if not choice:
            return
        if choice == "all":
            print(data)
            return

        try:
            row_count = int(choice)
        except ValueError:
            print("Invalid input. Enter a whole number, 'all', or press Enter.")
            continue

        if row_count < 1 or row_count > len(data):
            print(f"Enter a number from 1 to {len(data)}.")
            continue

        print(data.head(row_count))
        return


def total_sales_by_region_order_type(data):
    """Show total dollar sales by region and order type."""
    if not check_columns(data, ["sales_region", "order_type", "quantity", "unit_price"]):
        return

    sales_data = data.copy()
    sales_data["sales"] = sales_data["quantity"] * sales_data["unit_price"]
    pivot_table = pd.pivot_table(
        sales_data,
        index="sales_region",
        columns="order_type",
        values="sales",
        aggfunc="sum",
        fill_value=0,
    )
    print("\nTotal sales by region and order type:")
    print(pivot_table)


def average_sales_by_region(data):
    """Show average dollar sales by region, state, and order type."""
    if not check_columns(
        data, ["sales_region", "customer_state", "order_type", "quantity", "unit_price"]
    ):
        return

    sales_data = data.copy()
    sales_data["sales"] = sales_data["quantity"] * sales_data["unit_price"]
    pivot_table = pd.pivot_table(
        sales_data,
        index="sales_region",
        columns=["customer_state", "order_type"],
        values="sales",
        aggfunc="mean",
    )
    print("\nAverage sales by region, state, and order type:")
    print(pivot_table.round(2))


def sales_by_customer_type_order_type_state(data):
    """Show sales by customer type and order type, broken down by state."""
    if not check_columns(
        data, ["customer_type", "order_type", "customer_state", "quantity", "unit_price"]
    ):
        return

    sales_data = data.copy()
    sales_data["sales"] = sales_data["quantity"] * sales_data["unit_price"]
    pivot_table = pd.pivot_table(
        sales_data,
        index=["customer_type", "order_type"],
        columns="customer_state",
        values="sales",
        aggfunc="sum",
        fill_value=0,
    )
    print("\nSales by customer type and order type, by state:")
    print(pivot_table)


def total_sales_quantity_price_by_region_product(data):
    """Show summed quantity and dollar sales by region and product."""
    if not check_columns(
        data, ["sales_region", "produce_name", "quantity", "unit_price"]
    ):
        return

    sales_data = data.copy()
    sales_data["sales"] = sales_data["quantity"] * sales_data["unit_price"]
    pivot_table = pd.pivot_table(
        sales_data,
        index=["sales_region", "produce_name"],
        values=["quantity", "sales"],
        aggfunc="sum",
        fill_value=0,
    )
    print("\nTotal quantity and sales by region and product:")
    print(pivot_table)


def total_sales_quantity_price_by_customer_type(data):
    """Show summed quantity and dollar sales by order and customer type."""
    if not check_columns(
        data, ["order_type", "customer_type", "quantity", "unit_price"]
    ):
        return

    sales_data = data.copy()
    sales_data["sales"] = sales_data["quantity"] * sales_data["unit_price"]
    pivot_table = pd.pivot_table(
        sales_data,
        index=["order_type", "customer_type"],
        values=["quantity", "sales"],
        aggfunc="sum",
        fill_value=0,
    )
    print("\nTotal quantity and sales by order and customer type:")
    print(pivot_table)


def max_min_sales_price_by_category(data):
    """Show the maximum and minimum unit price for each product category."""
    if not check_columns(data, ["product_category", "unit_price"]):
        return

    pivot_table = pd.pivot_table(
        data,
        index="product_category",
        values="unit_price",
        aggfunc=["max", "min"],
    )
    print("\nMaximum and minimum unit price by product category:")
    print(pivot_table)


def unique_employees_by_region(data):
    """Count unique employees in each sales region."""
    if not check_columns(data, ["sales_region", "employee_id"]):
        return

    pivot_table = pd.pivot_table(
        data,
        index="sales_region",
        values="employee_id",
        aggfunc="nunique",
    )
    pivot_table.columns = ["unique_employee_count"]
    print("\nNumber of unique employees by region:")
    print(pivot_table)


def create_custom_pivot_table(data):
    print("The custom pivot table will be added in R4.")


def exit_program(data):
    print("Exiting the Sales Data Dashboard.")
    raise SystemExit


menu_options = (
    ("Show the first n rows of sales data", show_first_rows),
    ("Total sales by region and order_type", total_sales_by_region_order_type),
    ("Average sales by region with average sales by state and sale type", average_sales_by_region),
    ("Sales by customer type and order type by state", sales_by_customer_type_order_type_state),
    ("Total sales quantity and price by region and product", total_sales_quantity_price_by_region_product),
    ("Total sales quantity and price customer type", total_sales_quantity_price_by_customer_type),
    ("Max and min sales price of sales by category", max_min_sales_price_by_category),
    ("Number of unique employees by region", unique_employees_by_region),
    ("Create a custom pivot table", create_custom_pivot_table),
    ("Exit", exit_program),
)


def display_menu():
    """Print the menu and return the selected option's position."""
    while True:
        print("\n--- Sales Data Dashboard ---")
        for number, (description, action) in enumerate(menu_options, start=1):
            print(f"{number}. {description}")

        choice = input(f"Enter a number from 1 to {len(menu_options)}: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(menu_options):
            return int(choice) - 1

        print("Invalid choice. Please enter one of the menu numbers.")


def main():
    data = load_csv(sales_data_url)
    if data is None:
        return

    while True:
        selection = display_menu()
        description, action = menu_options[selection]
        action(data)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting the Sales Data Dashboard.")