import unittest

from Lab7.ex4c import check_budget


class CheckBudgetTests(unittest.TestCase):
    def test_marks_purchase_within_budget(self):
        self.assertEqual(
            check_budget([20.0], 50.0),
            ["This purchase 20.0 is within budget."],
        )

    def test_marks_purchase_over_budget(self):
        self.assertEqual(
            check_budget([60.0], 50.0),
            ["This purchase 60.0 is over budget!"],
        )

    def test_stops_after_first_over_budget_purchase(self):
        self.assertEqual(
            check_budget([30.0, 25.0, 5.0], 50.0),
            [
                "This purchase 30.0 is within budget.",
                "This purchase 25.0 is over budget!",
            ],
        )

    def test_empty_purchase_list(self):
        self.assertEqual(check_budget([], 50.0), [])


if __name__ == "__main__":
    unittest.main()
