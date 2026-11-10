from pathlib import Path
import time

import pandas as pd


def load_csv(filepath):
    """Load sales data and report timing, shape, columns, and missing fields."""
    print(f"Loading CSV file from: {filepath}")
    start_time = time.time()
    try:
        data = pd.read_csv(filepath, engine="pyarrow", on_bad_lines="skip")
    except Exception as error:
        print(f"Error reading the CSV file: {error}")
        return None

    load_time = time.time() - start_time
    print(f"CSV file loaded successfully in {load_time:.2f} seconds.")
    print(f"Number of rows: {len(data)}")
    print("Columns:", ", ".join(data.columns))

    if "order_date" in data.columns:
        data["order_date"] = pd.to_datetime(
            data["order_date"], format="mixed", errors="coerce"
        )

    required_columns = [
        "sales_region",
        "employee_id",
        "customer_state",
        "order_type",
        "quantity",
        "unit_price",
    ]
    missing_columns = [
        column for column in required_columns if column not in data.columns
    ]
    if missing_columns:
        print(
            "Warning: missing required fields "
            f"{', '.join(missing_columns)}. Some analytics will not function."
        )
    return data


def display_initial_rows(data):
    """Display a requested number of rows, all rows, or skip the preview."""
    while True:
        response = input(
            f"\nHow many initial rows would you like to see? "
            f"(1-{len(data)}, 'all', or Enter to skip): "
        ).strip().lower()

        if not response:
            return
        if response == "all":
            print(data)
            return

        try:
            num_rows = int(response)
        except ValueError:
            print("Invalid input. Enter a whole number, 'all', or press Enter to skip.")
            continue

        if num_rows < 1:
            print("Please enter a number greater than 0.")
            continue
        if num_rows > len(data):
            print(f"Only {len(data)} rows are available; showing all of them.")
            num_rows = len(data)

        print(data.head(num_rows))
        return


def show_employees_by_region(data):
    """Display the number of unique employees in each sales region."""
    required = ["sales_region", "employee_id"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        print("Missing required columns:", ", ".join(missing))
        return

    employee_counts = pd.pivot_table(
        data,
        index="sales_region",
        values="employee_id",
        aggfunc="nunique",
    )
    employee_counts.columns = ["unique_employee_count"]
    print("\nNumber of employees by region:")
    print(employee_counts.to_string())


def show_average_sales_by_region(data):
    """Display average sales by region, customer state, and order type."""
    required = [
        "sales_region",
        "customer_state",
        "order_type",
        "quantity",
        "unit_price",
    ]
    missing = [column for column in required if column not in data.columns]
    if missing:
        print("Missing required columns:", ", ".join(missing))
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
    with pd.option_context("display.width", 200, "display.max_columns", None):
        print(pivot_table.round(2))


def get_user_selection(options, prompt, required=False, single=False):
    """Prompt for option numbers and return the corresponding selections."""
    while True:
        print(prompt)
        for number, option in enumerate(options, start=1):
            print(f"{number}. {option}")

        choice = input("Enter the number(s) of your choice(s), separated by commas: ").strip()
        if not choice:
            if required:
                print("A selection is required.")
                continue
            return []

        try:
            indexes = [int(value.strip()) for value in choice.split(",")]
        except ValueError:
            print("Invalid input. Enter numbers separated by commas.")
            continue

        if any(index < 1 or index > len(options) for index in indexes):
            print(f"Each number must be between 1 and {len(options)}.")
            continue

        selected = list(dict.fromkeys(options[index - 1] for index in indexes))
        if single and len(selected) != 1:
            print("Please select exactly one option.")
            continue
        return selected


def generate_custom_pivot_table(data):
    """Interactively create a pivot table from the sales data."""
    row_options = list(data.columns)
    if not row_options:
        print("No columns are available to use as rows.")
        return

    rows = get_user_selection(row_options, "\nSelect rows (required):", required=True)

    col_options = [column for column in row_options if column not in rows]
    cols = get_user_selection(
        col_options, "\nSelect columns (optional, press Enter to skip):"
    )

    value_options = list(data.select_dtypes(include=["number"]).columns)
    if not value_options:
        print("No numeric columns are available to aggregate.")
        return
    values = get_user_selection(
        value_options, "\nSelect value(s) to aggregate:", required=True
    )

    agg_options = ["sum", "mean", "count"]
    agg_func = get_user_selection(
        agg_options,
        "\nSelect aggregation function:",
        required=True,
        single=True,
    )[0]

    try:
        pivot_table = pd.pivot_table(
            data,
            index=rows,
            columns=cols if cols else None,
            values=values,
            aggfunc=agg_func,
        )
    except (KeyError, ValueError, TypeError) as error:
        print(f"Could not create the pivot table: {error}")
        return

    print("\nCustom pivot table:")
    print(pivot_table)


def exit_program(data):
    """Exit the dashboard."""
    print("Exiting the program. Goodbye!")
    raise SystemExit(0)


menu_options = (
    ("Show the first n rows of sales data", display_initial_rows),
    ("Show the number of employees by region", show_employees_by_region),
    ("Average sales by region, by state and order type", show_average_sales_by_region),
    ("Create a custom pivot table", generate_custom_pivot_table),
    ("Exit the program", exit_program),
)


def display_menu():
    """Display the menu and return the selected action index."""
    while True:
        print("\nSales Data Menu")
        for number, (description, _) in enumerate(menu_options, start=1):
            print(f"  {number}. {description}")

        choice = input(f"Select an option (1-{len(menu_options)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(menu_options):
            return int(choice) - 1
        print(f"Invalid selection '{choice}'. Choose a number from 1 to {len(menu_options)}.")


def main():
    """Load the local sales CSV and run the interactive dashboard."""
    csv_file = Path(__file__).with_name("sales_data_assn2.csv")
    sales_data = load_csv(csv_file)
    if sales_data is None:
        return

    while True:
        _, action = menu_options[display_menu()]
        action(sales_data)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")