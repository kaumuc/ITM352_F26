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


def display_initial_rows(data):
    while True:
        try:
            row_count = input(
                "How many initial rows would you like to see? "
                "(enter a positive whole number): "
            )
        except EOFError:
            print("\nInput closed; exiting.")
            return False

        try:
            number_of_rows = int(row_count)
        except ValueError:
            print("Invalid input. Enter a positive whole number.")
            continue

        if number_of_rows <= 0:
            print("Invalid input. Enter a number greater than zero.")
            continue

        print(data.head(number_of_rows))
        return True


def main():
    csv_file = Path(__file__).with_name("sales_data_assn2.csv")
    sales_data = load_csv(csv_file)
    if sales_data is None:
        return

    try:
        while True:
            if not display_initial_rows(sales_data):
                break
    except KeyboardInterrupt:
        print("\nExiting.")


if __name__ == "__main__":
    main()
