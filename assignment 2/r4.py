import pandas as pd
import r3


# AI use: Copilot helped organize the custom pivot code from the R4 instructions.
def get_user_selection(options, prompt, required=False, single=False):
    """Ask the user to select options by entering their numbers."""
    while True:
        print(prompt)
        for number, option in enumerate(options, start=1):
            print(f"{number}. {option}")

        choice = input("Enter the number(s) of your choice(s), separated by commas: ")
        choice = choice.strip()

        if not choice:
            if required:
                print("A selection is required.")
                continue
            return []

        try:
            numbers = [int(value.strip()) for value in choice.split(",")]
        except ValueError:
            print("Invalid input. Enter numbers separated by commas.")
            continue

        if any(number < 1 or number > len(options) for number in numbers):
            print(f"Enter numbers from 1 to {len(options)}.")
            continue

        selected = []
        for number in numbers:
            option = options[number - 1]
            if option not in selected:
                selected.append(option)

        if single and len(selected) != 1:
            print("Please select one option.")
            continue

        return selected


def create_custom_pivot_table(data):
    """Let the user choose fields and display a custom pivot table."""
    pivot_data = data.copy()

    # The CSV has quantity and unit_price, so calculate a sales amount for analysis.
    if "quantity" in pivot_data.columns and "unit_price" in pivot_data.columns:
        pivot_data["sales"] = pivot_data["quantity"] * pivot_data["unit_price"]

    row_options = list(pivot_data.columns)
    if not row_options:
        print("There are no fields available to use as rows.")
        return

    rows = get_user_selection(
        row_options, "\nSelect rows (required):", required=True
    )

    column_options = [column for column in row_options if column not in rows]
    columns = get_user_selection(
        column_options,
        "\nSelect columns (optional, press Enter for no grouping):",
    )

    value_options = list(pivot_data.select_dtypes(include=["number"]).columns)
    if not value_options:
        print("There are no numeric fields to summarize.")
        return

    values = get_user_selection(
        value_options, "\nSelect values (required):", required=True
    )

    aggregation_options = ["sum", "mean", "count"]
    aggregation = get_user_selection(
        aggregation_options,
        "\nSelect aggregation function:",
        required=True,
        single=True,
    )[0]

    try:
        pivot_table = pd.pivot_table(
            pivot_data,
            index=rows,
            columns=columns if columns else None,
            values=values,
            aggfunc=aggregation,
        )
    except (KeyError, ValueError, TypeError) as error:
        print(f"Could not create the pivot table: {error}")
        return

    print("\nCustom pivot table:")
    print(pivot_table)
    return pivot_table


menu_options = (
    ("Show the first n rows of sales data", r3.show_first_rows),
    ("Total sales by region and order_type", r3.total_sales_by_region_order_type),
    ("Average sales by region with average sales by state and sale type", r3.average_sales_by_region),
    ("Sales by customer type and order type by state", r3.sales_by_customer_type_order_type_state),
    ("Total sales quantity and price by region and product", r3.total_sales_quantity_price_by_region_product),
    ("Total sales quantity and price customer type", r3.total_sales_quantity_price_by_customer_type),
    ("Max and min sales price of sales by category", r3.max_min_sales_price_by_category),
    ("Number of unique employees by region", r3.unique_employees_by_region),
    ("Create a custom pivot table", create_custom_pivot_table),
    ("Exit", r3.exit_program),
)


def display_menu():
    """Print the dashboard menu and return the selected option's position."""
    while True:
        print("\n--- Sales Data Dashboard ---")
        for number, (description, action) in enumerate(menu_options, start=1):
            print(f"{number}. {description}")

        choice = input(f"Enter a number from 1 to {len(menu_options)}: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(menu_options):
            return int(choice) - 1

        print("Invalid choice. Please enter one of the menu numbers.")


def main():
    """Load the sales data and run the dashboard with the custom pivot option."""
    data = r3.load_csv(r3.sales_data_url)
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