import time

import pandas as pd


# I asked AI to explain pandas pivot tables, filling missing pivot values,
# calculating percentages, and saving results. It helped me understand how
# rows and columns group the data. I tested these parts with small examples.
sales_data_url = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"

# These columns are used by the dashboard summary and its analyses.
required_columns = [
    "order_number",
    "employee_id",
    "order_date",
    "sales_region",
    "order_type",
    "customer_type",
    "customer_name",
    "customer_state",
    "product_category",
    "produce_name",
    "quantity",
    "unit_price",
]


# Load the CSV and show the required startup summary.
def load_csv(filepath):
    """Load the sales data and show its size, columns, and missing fields."""
    print(f"Loading sales data from: {filepath}")
    start_time = time.time()

    # Report a clear message if the file cannot be opened or read as a CSV.
    try:
        data = pd.read_csv(filepath)
    except (OSError, ValueError, pd.errors.ParserError) as error:
        print(f"Could not load the sales data: {error}")
        return None

    # Replace blank cells so they do not cause problems in later calculations.
    data = data.fillna(0)
    print(f"Sales data loaded in {time.time() - start_time:.2f} seconds.")
    print(f"Number of rows: {len(data)}")
    print("Available columns:", ", ".join(data.columns))

    # Keep running if a field is missing, but tell the user which analyses may fail.
    missing_columns = [
        column for column in required_columns if column not in data.columns
    ]
    if missing_columns:
        print("Warning: missing required fields:", ", ".join(missing_columns))
        print("Some analytics may not be available.")

    return data


def display_data_summary(data):
    """Show the summary statistics requested for the loaded sales data."""
    print("\n--- Sales Data Summary ---")

    # Count distinct IDs/names rather than counting every row as a new item.
    if "order_number" in data.columns:
        print("Total orders:", data["order_number"].nunique())
    else:
        print("Total orders: Not available (missing order_number)")

    if "employee_id" in data.columns:
        print("Employees:", data["employee_id"].nunique())
    else:
        print("Employees: Not available (missing employee_id)")

    if "sales_region" in data.columns:
        print("Sales regions:", data["sales_region"].nunique())
    else:
        print("Sales regions: Not available (missing sales_region)")

    if "order_date" in data.columns:
        # Convert date text to dates; invalid or blank dates are ignored.
        dates = pd.to_datetime(
            data["order_date"].replace(0, pd.NA),
            format="mixed",
            errors="coerce",
        ).dropna()
        if len(dates) > 0:
            print("Order date range:", dates.min().date(), "to", dates.max().date())
        else:
            print("Order date range: Not available")
    else:
        print("Order date range: Not available (missing order_date)")

    if "customer_name" in data.columns:
        print("Unique customers:", data["customer_name"].nunique())
    else:
        print("Unique customers: Not available (missing customer_name)")

    if "product_category" in data.columns:
        print("Product categories:", data["product_category"].nunique())
    else:
        print("Product categories: Not available (missing product_category)")

    if "customer_state" in data.columns:
        print("Unique states:", data["customer_state"].nunique())
    else:
        print("Unique states: Not available (missing customer_state)")

    if "quantity" in data.columns and "unit_price" in data.columns:
        # The CSV has no total-sales column, so calculate quantity times price.
        total_sales = (data["quantity"] * data["unit_price"]).sum()
        print(f"Total sales amount: ${total_sales:,.2f}")
    else:
        print("Total sales amount: Not available (missing quantity or unit_price)")

    if "quantity" in data.columns:
        print("Total product quantity sold:", data["quantity"].sum())
    else:
        print("Total product quantity sold: Not available (missing quantity)")


# Check fields and create common values used by the analyses.
def check_columns(data, columns):
    """Return whether all requested columns are in the data."""
    # Do not start an analysis that needs fields the loaded file does not have.
    missing_columns = [column for column in columns if column not in data.columns]
    if missing_columns:
        print("This analysis needs these columns:", ", ".join(missing_columns))
        return False
    return True


def add_sales_column(data):
    """Return a copy of the data with sales calculated from quantity and price."""
    # Use a copy so adding a calculated column does not change the loaded data.
    sales_data = data.copy()
    sales_data["sales"] = sales_data["quantity"] * sales_data["unit_price"]
    return sales_data


def fill_pivot_gaps(pivot_table):
    """Requirement 9: use each numeric column's mean for empty pivot cells."""
    # AI helped me understand select_dtypes: it selects numeric columns so each
    # blank value can be filled with the average for its own column.
    column_averages = pivot_table.select_dtypes(include=["number"]).mean()
    return pivot_table.fillna(column_averages)


def show_first_rows(data):
    """Show the requested starting rows, all rows, or skip the preview."""
    while True:
        print(f"\nThere are {len(data)} rows available.")
        print("Enter a number, 'all', or press Enter to skip.")
        choice = input("Your choice: ").strip().lower()

        if not choice:
            return None
        if choice == "all":
            print(data)
            return None

        # Ask again if the entry is not a valid row count.
        try:
            row_count = int(choice)
        except ValueError:
            print("Invalid input. Enter a whole number, 'all', or press Enter.")
            continue

        if row_count < 1 or row_count > len(data):
            print(f"Enter a number from 1 to {len(data)}.")
            continue

        print(data.head(row_count))
        return None


# Predefined pivot tables from the dashboard menu.
def total_sales_by_region_order_type(data):
    """Show total dollar sales by region and order type."""
    if not check_columns(data, ["sales_region", "order_type", "quantity", "unit_price"]):
        return None

    sales_data = add_sales_column(data)
    # I asked AI to explain pivot_table. I learned that index groups rows,
    # columns makes subgroups, and aggfunc combines the sales in each group.
    pivot_table = pd.pivot_table(
        sales_data,
        index="sales_region",
        columns="order_type",
        values="sales",
        aggfunc="sum",
    )
    pivot_table = fill_pivot_gaps(pivot_table)
    print("\nTotal sales by region and order type:")
    print(pivot_table)
    return pivot_table


def average_sales_by_region(data):
    """Show average sales by region, state, and order type."""
    if not check_columns(
        data, ["sales_region", "customer_state", "order_type", "quantity", "unit_price"]
    ):
        return None

    sales_data = add_sales_column(data)
    # Multiple column fields create nested headings: state, then order type.
    pivot_table = pd.pivot_table(
        sales_data,
        index="sales_region",
        columns=["customer_state", "order_type"],
        values="sales",
        aggfunc="mean",
    )
    pivot_table = fill_pivot_gaps(pivot_table)
    print("\nAverage sales by region, state, and order type:")
    print(pivot_table.round(2))
    return pivot_table


def sales_by_customer_type_order_type_state(data):
    """Show sales by customer type and order type, broken down by state."""
    if not check_columns(
        data, ["customer_type", "order_type", "customer_state", "quantity", "unit_price"]
    ):
        return None

    sales_data = add_sales_column(data)
    # Group customer and order types down the rows, with each state in a column.
    pivot_table = pd.pivot_table(
        sales_data,
        index=["customer_type", "order_type"],
        columns="customer_state",
        values="sales",
        aggfunc="sum",
    )
    pivot_table = fill_pivot_gaps(pivot_table)
    print("\nSales by customer type and order type, by state:")
    print(pivot_table)
    return pivot_table


def total_sales_quantity_price_by_region_product(data):
    """Show summed quantity and sales by region and product."""
    if not check_columns(
        data, ["sales_region", "produce_name", "quantity", "unit_price"]
    ):
        return None

    sales_data = add_sales_column(data)
    # Sum both the number of items and their calculated dollar sales per group.
    pivot_table = pd.pivot_table(
        sales_data,
        index=["sales_region", "produce_name"],
        values=["quantity", "sales"],
        aggfunc="sum",
    )
    pivot_table = fill_pivot_gaps(pivot_table)
    print("\nTotal quantity and sales by region and product:")
    print(pivot_table)
    return pivot_table


def total_sales_quantity_price_by_customer_type(data):
    """Show summed quantity and sales by order and customer type."""
    if not check_columns(
        data, ["order_type", "customer_type", "quantity", "unit_price"]
    ):
        return None

    sales_data = add_sales_column(data)
    # Group by both order type and customer type.
    pivot_table = pd.pivot_table(
        sales_data,
        index=["order_type", "customer_type"],
        values=["quantity", "sales"],
        aggfunc="sum",
    )
    pivot_table = fill_pivot_gaps(pivot_table)
    print("\nTotal quantity and sales by order and customer type:")
    print(pivot_table)
    return pivot_table


def max_min_sales_price_by_category(data):
    """Show maximum and minimum unit price by product category."""
    if not check_columns(data, ["product_category", "unit_price"]):
        return None

    # Use two aggregation functions to show both ends of each category's prices.
    pivot_table = pd.pivot_table(
        data,
        index="product_category",
        values="unit_price",
        aggfunc=["max", "min"],
    )
    pivot_table = fill_pivot_gaps(pivot_table)
    print("\nMaximum and minimum unit price by product category:")
    print(pivot_table)
    return pivot_table


def unique_employees_by_region(data):
    """Count unique employees in each sales region."""
    if not check_columns(data, ["sales_region", "employee_id"]):
        return None

    # nunique counts each employee once within a region.
    pivot_table = pd.pivot_table(
        data,
        index="sales_region",
        values="employee_id",
        aggfunc="nunique",
    )
    pivot_table.columns = ["unique_employee_count"]
    print("\nNumber of unique employees by region:")
    print(pivot_table)
    return pivot_table


def sales_percentages_by_region_product(data):
    """Show each product's quantity and sales share within its region."""
    if not check_columns(
        data, ["sales_region", "produce_name", "quantity", "unit_price"]
    ):
        return None

    sales_data = add_sales_column(data)
    # reset_index puts the group names back into columns so the loop can use them.
    pivot_table = pd.pivot_table(
        sales_data,
        index=["sales_region", "produce_name"],
        values=["quantity", "sales"],
        aggfunc="sum",
    ).reset_index()
    pivot_table["quantity_percentage"] = 0.0
    pivot_table["sales_percentage"] = 0.0

    # I asked AI to explain the percentage calculation: divide each product's
    # amount by its region total, then multiply by 100.
    for row_number in range(len(pivot_table)):
        region = pivot_table.loc[row_number, "sales_region"]
        region_data = pivot_table[pivot_table["sales_region"] == region]
        quantity_total = region_data["quantity"].sum()
        sales_total = region_data["sales"].sum()

        if quantity_total != 0:
            pivot_table.loc[row_number, "quantity_percentage"] = (
                pivot_table.loc[row_number, "quantity"] / quantity_total * 100
            )
        if sales_total != 0:
            pivot_table.loc[row_number, "sales_percentage"] = (
                pivot_table.loc[row_number, "sales"] / sales_total * 100
            )

    pivot_table = fill_pivot_gaps(pivot_table)
    # Put the region and product names back on the left as row labels.
    pivot_table = pivot_table.set_index(["sales_region", "produce_name"])
    print("\nQuantity and sales percentages by region and product:")
    print(pivot_table.round(2))
    return pivot_table


# Ask for and validate the user's custom pivot table choices.
def get_user_selection(options, prompt, required=False, single=False):
    """Ask the user to select options by entering their numbers."""
    while True:
        print(prompt)
        for number, option in enumerate(options, start=1):
            print(f"{number}. {option}")

        choice = input("Enter numbers separated by commas: ").strip()
        if not choice:
            if required:
                print("A selection is required.")
                continue
            return []

        # Convert the typed numbers to integers so they can select list items.
        try:
            numbers = [int(value.strip()) for value in choice.split(",")]
        except ValueError:
            print("Invalid input. Enter numbers separated by commas.")
            continue

        # Reject numbers outside the displayed list before using them as indexes.
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
    # Add calculated sales as another option when the needed source fields exist.
    pivot_data = data.copy()
    if "quantity" in pivot_data.columns and "unit_price" in pivot_data.columns:
        pivot_data["sales"] = pivot_data["quantity"] * pivot_data["unit_price"]

    # Rows are required; selected row fields are removed from column choices.
    row_options = list(pivot_data.columns)
    if not row_options:
        print("There are no fields available to use as rows.")
        return None

    # I asked AI how to connect the user's selections to pivot_table options.
    rows = get_user_selection(row_options, "\nSelect rows (required):", required=True)
    column_options = [column for column in row_options if column not in rows]
    columns = get_user_selection(
        column_options,
        "\nSelect columns (optional, press Enter for no grouping):",
    )

    # AI explained that select_dtypes keeps the value choices numeric, which
    # makes sense for the requested sum, mean, and count operations.
    value_options = list(pivot_data.select_dtypes(include=["number"]).columns)
    if not value_options:
        print("There are no numeric fields to summarize.")
        return None

    values = get_user_selection(
        value_options, "\nSelect values (required):", required=True
    )
    aggregation = get_user_selection(
        ["sum", "mean", "count"],
        "\nSelect aggregation function:",
        required=True,
        single=True,
    )[0]

    # Use the user's selections to build the pivot, and show a useful error
    # instead of stopping the whole dashboard if those selections cannot work.
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
        return None

    pivot_table = fill_pivot_gaps(pivot_table)
    print("\nCustom pivot table:")
    print(pivot_table)
    return pivot_table


def save_result(results, name, pivot_table):
    """Requirement 10: keep each analysis result in the results dictionary."""
    result_name = name
    number = 2
    # Give repeated analyses different names so earlier results stay available.
    while result_name in results:
        result_name = f"{name} ({number})"
        number += 1

    # Save a copy so later changes to the pivot do not change the saved result.
    results[result_name] = pivot_table.copy()
    print(f"Saved result: {result_name}")


def display_saved_results(results):
    """Print all pivot tables saved during this dashboard session."""
    if not results:
        print("\nNo analysis results have been saved yet.")
        return

    print("\n--- Saved Analysis Results ---")
    for name, pivot_table in results.items():
        print(f"\n{name}:")
        print(pivot_table)


def exit_program(data):
    print("Exiting the Sales Data Dashboard.")
    raise SystemExit


# Keep the menu items and their functions together so they are easy to reorder.
menu_options = (
    ("Show the first n rows of sales data", show_first_rows),
    ("Total sales by region and order_type", total_sales_by_region_order_type),
    ("Average sales by region with average sales by state and sale type", average_sales_by_region),
    ("Sales by customer type and order type by state", sales_by_customer_type_order_type_state),
    ("Total sales quantity and price by region and product", total_sales_quantity_price_by_region_product),
    ("Total sales quantity and price customer type", total_sales_quantity_price_by_customer_type),
    ("Max and min sales price of sales by category", max_min_sales_price_by_category),
    ("Number of unique employees by region", unique_employees_by_region),
    ("Sales percentages by region and product", sales_percentages_by_region_product),
    ("Create a custom pivot table", create_custom_pivot_table),
    ("Display saved results", display_saved_results),
    ("Exit", exit_program),
)

# List the data fields each preset analysis needs; custom and general options
# are handled separately because they do not have one fixed set of fields.
analysis_columns = {
    "Total sales by region and order_type": [
        "sales_region", "order_type", "quantity", "unit_price"
    ],
    "Average sales by region with average sales by state and sale type": [
        "sales_region", "customer_state", "order_type", "quantity", "unit_price"
    ],
    "Sales by customer type and order type by state": [
        "customer_type", "order_type", "customer_state", "quantity", "unit_price"
    ],
    "Total sales quantity and price by region and product": [
        "sales_region", "produce_name", "quantity", "unit_price"
    ],
    "Total sales quantity and price customer type": [
        "order_type", "customer_type", "quantity", "unit_price"
    ],
    "Max and min sales price of sales by category": [
        "product_category", "unit_price"
    ],
    "Number of unique employees by region": ["sales_region", "employee_id"],
    "Sales percentages by region and product": [
        "sales_region", "produce_name", "quantity", "unit_price"
    ],
}


def get_available_menu(data):
    """Hide predefined analyses when the data is missing columns they need."""
    available_options = []
    for description, action in menu_options:
        needed_columns = analysis_columns.get(description, [])
        if all(column in data.columns for column in needed_columns):
            available_options.append((description, action))
    return available_options


def display_menu(data, results):
    """Show saved result names and return a valid choice from the available menu."""
    available_options = get_available_menu(data)

    while True:
        print("\n--- Sales Data Dashboard ---")
        # Show completed analysis names above the menu as required.
        if results:
            print("Completed analyses:")
            for name in results:
                print("-", name)
        else:
            print("Completed analyses: none")

        for number, (description, action) in enumerate(available_options, start=1):
            print(f"{number}. {description}")

        choice = input(
            f"Choose an option from 1 to {len(available_options)}: "
        ).strip()
        if choice.isdigit() and 1 <= int(choice) <= len(available_options):
            return int(choice) - 1, available_options

        print("Invalid choice. Please enter one of the menu numbers.")


def main():
    """Load data, show its summary, and run the dashboard menu."""
    data = load_csv(sales_data_url)
    if data is None:
        return

    display_data_summary(data)
    # Keep completed pivot tables for the duration of this dashboard session.
    results = {}

    while True:
        selection, available_options = display_menu(data, results)
        description, action = available_options[selection]

        # The saved-results choice displays old results; other choices may
        # return a pivot table that should be added to the results dictionary.
        if action == display_saved_results:
            action(results)
        else:
            pivot_table = action(data)
            if isinstance(pivot_table, pd.DataFrame):
                save_result(results, description, pivot_table)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting the Sales Data Dashboard.")