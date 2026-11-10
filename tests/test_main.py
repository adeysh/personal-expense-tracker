import unittest
from unittest.mock import patch

from main import (
    get_valid_category,
    get_valid_date,
    get_expense_index,
    get_valid_name,
    get_valid_amount,
    get_valid_year,
    get_valid_month,
    get_valid_search_term,
)


class TestMain(unittest.TestCase):

    # Category validation

    def test_get_valid_category(self):
        with patch("builtins.input", return_value="small"):
            category = get_valid_category()

        self.assertEqual(category, "Small")

    def test_get_valid_category_with_invalid_input(self):
        with patch("builtins.input", side_effect=["Invalid", "medium"]) as mock_input:
            category = get_valid_category()

        self.assertEqual(category, "Medium")
        self.assertEqual(mock_input.call_count, 2)

    # Date validation

    def test_get_valid_date(self):
        with patch("builtins.input", return_value="2026-11-10"):
            target_date = get_valid_date()

        self.assertEqual(target_date, "2026-11-10")

    def test_get_valid_date_with_invalid_input(self):
        with patch(
            "builtins.input", side_effect=["2026-02-30", "2026-11-10"]
        ) as mock_input:
            target_date = get_valid_date()

        self.assertEqual(target_date, "2026-11-10")
        self.assertEqual(mock_input.call_count, 2)

    # Expense index validation

    def test_get_expense_index(self):
        expenses = [
            {"name": "Groceries", "amount": 100},
            {"name": "Transport", "amount": 50},
        ]

        with patch("builtins.input", return_value="2"):
            index = get_expense_index(expenses)

        self.assertEqual(index, 1)

    def test_get_expense_index_with_invalid_inputs(self):
        expenses = [
            {"name": "Groceries", "amount": 100},
            {"name": "Transport", "amount": 50},
        ]

        with patch("builtins.input", side_effect=["abc", "0", "3", "2"]) as mock_input:
            index = get_expense_index(expenses)

        self.assertEqual(index, 1)
        self.assertEqual(mock_input.call_count, 4)

    # Name validation

    def test_get_valid_name(self):
        with patch("builtins.input", return_value="Groceries"):
            name = get_valid_name()

        self.assertEqual(name, "Groceries")

    def test_get_valid_name_with_empty_input(self):
        with patch(
            "builtins.input", side_effect=["", "   ", "Groceries"]
        ) as mock_input:
            name = get_valid_name()

        self.assertEqual(name, "Groceries")
        self.assertEqual(mock_input.call_count, 3)

    # Amount validation

    def test_get_valid_amount(self):
        with patch("builtins.input", return_value="150.50"):
            amount = get_valid_amount()

        self.assertEqual(amount, 150.50)

    def test_get_valid_amount_with_invalid_inputs(self):
        with patch(
            "builtins.input", side_effect=["abc", "0", "-10", "nan", "inf", "75"]
        ) as mock_input:
            amount = get_valid_amount()

        self.assertEqual(amount, 75.0)
        self.assertEqual(mock_input.call_count, 6)

    # Year validation

    def test_get_valid_year(self):
        with patch("builtins.input", return_value="2026"):
            year = get_valid_year()

        self.assertEqual(year, 2026)

    def test_get_valid_year_with_invalid_inputs(self):
        with patch("builtins.input", side_effect=["abc", "999", "2026"]) as mock_input:
            year = get_valid_year()

        self.assertEqual(year, 2026)
        self.assertEqual(mock_input.call_count, 3)

    # Month validation

    def test_get_valid_month(self):
        with patch("builtins.input", return_value="11"):
            month = get_valid_month()

        self.assertEqual(month, 11)

    def test_get_valid_month_with_invalid_inputs(self):
        with patch(
            "builtins.input", side_effect=["abc", "0", "13", "11"]
        ) as mock_input:
            month = get_valid_month()

        self.assertEqual(month, 11)
        self.assertEqual(mock_input.call_count, 4)

        # Search validation

        def test_get_valid_search_term(self):
            with patch("builtins.input", return_value="Groceries"):
                search_term = get_valid_search_term()

            self.assertEqual(search_term, "Groceries")

        def test_get_valid_search_term_with_empty_input(self):
            with patch(
                "builtins.input", side_effect=["", "   ", "Groceries"]
            ) as mock_input:
                search_term = get_valid_search_term()

            self.assertEqual(search_term, "Groceries")
            self.assertEqual(mock_input.call_count, 3)


if __name__ == "__main__":
    unittest.main()
