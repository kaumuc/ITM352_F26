from pathlib import Path

import pandas as pd


def get_user_selection(options, prompt, required=False, single=False):
    """Prompt for comma-separated option numbers and return the chosen options."""
    while True:
        print(prompt)
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        choice = input("Enter the number(s) of your choice(s), separated by commas: ").strip()
        if not choice:
            if required:
                print("A selection is required.")
                continue
            return []

        try:
            indexes = [int(value.strip()) for value in choice.split(",")]
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
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
    """Interactively build and display a pivot table from the sales data."""
    row_options = list(data.columns)
    if not row_options:
        print("No columns are available to use as rows.")
        return

    rows = get_user_selection(row_options, "\nSelect rows (required):", required=True)

    col_options = row_options
    col_options = [col for col in col_options if col not in rows]
    cols = get_user_selection(
        col_options, "\nSelect columns (optional, press Enter to skip):"
    )

    value_options = list(data.select_dtypes(include=["number"]).columns)
    if not value_options:
        print("No numeric columns available to aggregate.")
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

    pivot_table = pd.pivot_table(
        data,
        index=rows,
        columns=cols if cols else None,
        values=values,
        aggfunc=agg_func,
    )

    print("\nCustom pivot table:")
    print(pivot_table)


def exit_program(data):
    print("Exiting the program. Goodbye!")
    raise SystemExit(0)


menu_options = (
    ("Create a custom pivot table", generate_custom_pivot_table),
    ("Exit the program", exit_program),
)


def display_menu():
    """Show the menu and return a valid selection as an index."""
    while True:
        print("\nSales Data Menu")
        for number, (description, _) in enumerate(menu_options, start=1):
            print(f"  {number}. {description}")

        choice = input(f"Select an option (1-{len(menu_options)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(menu_options):
            return int(choice) - 1
        print(f"Invalid selection '{choice}'. Please choose a listed number.")


def main():
    csv_file = Path(__file__).with_name("sales_data_assn2.csv")
    sales_data = pd.read_csv(csv_file)

    while True:
        _, action = menu_options[display_menu()]
        action(sales_data)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
