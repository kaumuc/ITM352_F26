import contextlib
import io
import unittest
from unittest.mock import patch

import pandas as pd

import finalversion

# This test suite checks the functions in finalversion.py using a small sample
# dataset. It tests loading, summaries, row selection, pivot tables, menus, and
# saved results. Mocking lets the tests provide input and capture printed output.

class FinalVersionTests(unittest.TestCase):
    def setUp(self):
        # Use the same small dataset in each test so expected results are clear.
        self.data = pd.DataFrame(
            {
                "order_number": [1, 2, 3],
                "employee_id": [10, 10, 20],
                "order_date": ["01/02/2025", "02/02/2025", "03/02/2025"],
                "sales_region": ["East", "East", "West"],
                "order_type": ["Retail", "Wholesale", "Retail"],
                "customer_type": ["Individual", "Business", "Individual"],
                "customer_name": ["A", "B", "A"],
                "customer_state": ["HI", "CA", "HI"],
                "product_category": ["Oil", "Oil", "Fruit"],
                "produce_name": ["Olive Oil", "Olive Oil", "Apple"],
                "quantity": [2, 3, 4],
                "unit_price": [5.0, 10.0, 2.5],
            }
        )

    # These tests check that loading handles missing values and file errors,
    # and that the summary displays information or handles missing columns.
    def test_load_csv_fills_missing_values_and_warns(self):
        sample = pd.DataFrame({"sales_region": ["East", None]})
        output = io.StringIO()
        with patch.object(finalversion.pd, "read_csv", return_value=sample):
            with contextlib.redirect_stdout(output):
                result = finalversion.load_csv("sample.csv")

        self.assertEqual(result.loc[1, "sales_region"], 0)
        self.assertIn("Number of rows: 2", output.getvalue())
        self.assertIn("Warning: missing required fields:", output.getvalue())

    def test_load_csv_reports_failure(self):
        output = io.StringIO()
        with patch.object(
            finalversion.pd, "read_csv", side_effect=OSError("unavailable")
        ):
            with contextlib.redirect_stdout(output):
                result = finalversion.load_csv("missing.csv")

        self.assertIsNone(result)
        self.assertIn("Could not load the sales data", output.getvalue())

    def test_data_summary_shows_requested_information(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            finalversion.display_data_summary(self.data)

        text = output.getvalue()
        self.assertIn("Total orders: 3", text)
        self.assertIn("Employees: 2", text)
        self.assertIn("Unique customers: 2", text)
        self.assertIn("Total sales amount: $50.00", text)
        self.assertIn("Total product quantity sold: 9", text)

    def test_data_summary_handles_missing_columns(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            finalversion.display_data_summary(pd.DataFrame({"quantity": [1]}))
        self.assertIn("Not available", output.getvalue())

    # These tests check that the row preview can be skipped, validated, or show
    # all of the data when the user enters "all".
    def test_show_first_rows_can_skip(self):
        with patch("builtins.input", return_value=""):
            self.assertIsNone(finalversion.show_first_rows(self.data))

    def test_show_first_rows_retries_invalid_choice(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["wrong", "2"]):
            with contextlib.redirect_stdout(output):
                finalversion.show_first_rows(self.data)
        self.assertIn("Invalid input", output.getvalue())
        self.assertIn("01/02/2025", output.getvalue())

    def test_show_first_rows_can_show_all(self):
        output = io.StringIO()
        with patch("builtins.input", return_value="all"):
            with contextlib.redirect_stdout(output):
                finalversion.show_first_rows(self.data)
        self.assertIn("Olive Oil", output.getvalue())
        self.assertIn("Apple", output.getvalue())

    # These tests check the results of each preset analysis against values
    # calculated from the small sample dataset above. I asked AI to explain
    # how pivot tables group data; that helped me check the correct row and
    # column labels when testing each result.
    def test_total_sales_by_region_and_order_type(self):
        result = finalversion.total_sales_by_region_order_type(self.data)
        self.assertEqual(result.to_numpy().sum(), 80)
        self.assertEqual(result.loc["East", "Wholesale"], 30)

    def test_average_sales_by_region(self):
        result = finalversion.average_sales_by_region(self.data)
        self.assertEqual(result.loc["East", ("HI", "Retail")], 10)

    def test_sales_by_customer_type_order_type_and_state(self):
        result = finalversion.sales_by_customer_type_order_type_state(self.data)
        self.assertEqual(result.loc[("Business", "Wholesale"), "CA"], 30)

    def test_quantity_and_sales_by_region_and_product(self):
        result = finalversion.total_sales_quantity_price_by_region_product(self.data)
        self.assertEqual(result.loc[("East", "Olive Oil"), "quantity"], 5)
        self.assertEqual(result.loc[("East", "Olive Oil"), "sales"], 40)

    def test_quantity_and_sales_by_customer_type(self):
        result = finalversion.total_sales_quantity_price_by_customer_type(self.data)
        self.assertEqual(result.loc[("Wholesale", "Business"), "sales"], 30)

    def test_max_and_min_sales_by_category(self):
        result = finalversion.max_min_sales_price_by_category(self.data)
        self.assertEqual(result.loc["Oil", ("max", "unit_price")], 10)
        self.assertEqual(result.loc["Oil", ("min", "unit_price")], 5)

    def test_unique_employees_by_region(self):
        result = finalversion.unique_employees_by_region(self.data)
        self.assertEqual(result.loc["East", "unique_employee_count"], 1)

    # These tests cover the mean used to fill pivot-table gaps and check that
    # product percentages are calculated against the totals for their region.
    def test_pivot_gaps_are_filled_with_column_mean(self):
        pivot = pd.DataFrame({"sales": [10.0, None, 30.0]})
        result = finalversion.fill_pivot_gaps(pivot)
        self.assertEqual(result.loc[1, "sales"], 20)

    def test_sales_percentages_by_region_and_product(self):
        sample = self.data.copy()
        sample.loc[1, "produce_name"] = "New Product"
        result = finalversion.sales_percentages_by_region_product(sample)

        self.assertAlmostEqual(
            result.loc[("East", "Olive Oil"), "quantity_percentage"], 40
        )
        self.assertAlmostEqual(
            result.loc[("East", "New Product"), "quantity_percentage"], 60
        )
        self.assertAlmostEqual(
            result.loc[("East", "Olive Oil"), "sales_percentage"], 25
        )
        self.assertAlmostEqual(
            result.loc[("East", "New Product"), "sales_percentage"], 75
        )

    # These tests check that custom pivot selections work and that invalid
    # choices are rejected. I asked AI how to test input() without typing
    # during each test; it explained that patch can supply the answers in order.
    def test_custom_pivot_table(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["4", "4", "5", "1"]):
            with contextlib.redirect_stdout(output):
                result = finalversion.create_custom_pivot_table(self.data)

        self.assertEqual(result.loc["East", ("sales", "Retail")], 10)
        self.assertIn("Custom pivot table:", output.getvalue())

    def test_add_sales_column(self):
        result = finalversion.add_sales_column(self.data)
        self.assertEqual(result.loc[0, "sales"], 10)
        self.assertNotIn("sales", self.data.columns)

    # These tests check that the menu validates input and saved analyses keep
    # unique names and copies of their pivot tables. AI also helped explain
    # that a copied DataFrame can be changed in the test without changing the
    # saved result, which is what the copy test checks.
    def test_get_user_selection_retries_invalid_input(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["x", "4", "2"]):
            with contextlib.redirect_stdout(output):
                result = finalversion.get_user_selection(
                    ["sum", "mean", "count"], "Choose:", required=True, single=True
                )
        self.assertEqual(result, ["mean"])
        self.assertIn("Invalid input", output.getvalue())
        self.assertIn("Enter numbers from 1 to 3", output.getvalue())

    def test_display_menu_retries_invalid_choice(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["wrong", "12"]):
            with contextlib.redirect_stdout(output):
                selection, options = finalversion.display_menu(self.data, {})
        self.assertEqual(options[selection][0], "Exit")
        self.assertIn("Invalid choice", output.getvalue())

    def test_save_result_keeps_repeated_results(self):
        results = {}
        pivot = pd.DataFrame({"sales": [10]})
        finalversion.save_result(results, "Sales", pivot)
        finalversion.save_result(results, "Sales", pivot)
        self.assertEqual(list(results), ["Sales", "Sales (2)"])

    def test_save_result_keeps_a_copy(self):
        results = {}
        pivot = pd.DataFrame({"sales": [10]})
        finalversion.save_result(results, "Sales", pivot)
        pivot.loc[0, "sales"] = 20
        self.assertEqual(results["Sales"].loc[0, "sales"], 10)

    # These tests check displaying saved results, hiding analyses that need
    # missing fields, exiting, and starting the dashboard.
    def test_display_saved_results(self):
        output = io.StringIO()
        results = {"Sales": pd.DataFrame({"sales": [10]})}
        with contextlib.redirect_stdout(output):
            finalversion.display_saved_results(results)
        self.assertIn("Sales", output.getvalue())
        self.assertIn("10", output.getvalue())

    def test_display_saved_results_when_empty(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            finalversion.display_saved_results({})
        self.assertIn("No analysis results", output.getvalue())

    def test_available_menu_hides_analytics_with_missing_columns(self):
        options = finalversion.get_available_menu(pd.DataFrame({"sales_region": []}))
        names = [name for name, action in options]
        self.assertIn("Show the first n rows of sales data", names)
        self.assertNotIn("Total sales by region and order_type", names)
        self.assertIn("Exit", names)

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            finalversion.exit_program(self.data)

    def test_main_loads_data_and_exits_from_menu(self):
        options = finalversion.get_available_menu(self.data)
        exit_choice = len(options) - 1
        with patch.object(finalversion, "load_csv", return_value=self.data):
            with patch.object(finalversion, "display_data_summary"):
                with patch.object(
                    finalversion,
                    "display_menu",
                    return_value=(exit_choice, options),
                ):
                    with self.assertRaises(SystemExit):
                        finalversion.main()


if __name__ == "__main__":
    unittest.main()
