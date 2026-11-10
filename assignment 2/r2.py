import time

import pandas as pd


# AI use: Copilot helped organize the menu from the assignment's R2 instructions.
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


def show_first_rows(data):
    print("The row preview will be added in R3.")


def total_sales_by_region_order_type(data):
    print("This analysis will be added in R3.")


def average_sales_by_region(data):
    print("This analysis will be added in R3.")


def sales_by_customer_type_order_type_state(data):
    print("This analysis will be added in R3.")


def total_sales_quantity_price_by_region_product(data):
    print("This analysis will be added in R3.")


def total_sales_quantity_price_by_customer_type(data):
    print("This analysis will be added in R3.")


def max_min_sales_price_by_category(data):
    print("This analysis will be added in R3.")


def unique_employees_by_region(data):
    print("This analysis will be added in R3.")


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