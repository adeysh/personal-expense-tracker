import unittest
from expense_manager import (
    get_category,
    calculate_total,
    add_expense,
    view_expenses,
    filter_expenses,
    calculate_category_totals,
    delete_expense,
    edit_expense,
    search_expenses,
    filter_expenses_by_date,
    validate_date,
    filter_expenses_by_category_and_date,
    filter_expenses_by_month,
)
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout
from datetime import date


class TestExpenseManager(unittest.TestCase):
    # Category

    def test_get_category(self):
        self.assertEqual(get_category(50), "Small")
        self.assertEqual(get_category(99.99), "Small")

    def test_medium_category(self):
        self.assertEqual(get_category(100), "Medium")
        self.assertEqual(get_category(499.99), "Medium")

    def test_large_category(self):
        self.assertEqual(get_category(500), "Large")

    # Calculate total

    def test_calculate_total(self):
        expenses = [
            {"name": "Adesh", "amount": 100.0, "category": "Medium"},
            {"name": "Adesh", "amount": 50.0, "category": "Small"},
            {"name": "Adesh", "amount": 25.5, "category": "Small"},
        ]

        self.assertEqual(calculate_total(expenses), 175.5)
        self.assertEqual(calculate_total([]), 0)

    # Calculate total

    def test_calculate_total(self):
        expenses = [
            {"name": "Groceries", "amount": 250, "category": "Medium"},
            {"name": "Snacks", "amount": 50, "category": "Small"},
            {"name": "Laptop", "amount": 750, "category": "Large"},
        ]

        result = calculate_total(expenses)

        self.assertEqual(result, 1050)

    def test_calculate_total_with_decimal_amounts(self):
        expenses = [
            {"name": "Groceries", "amount": 250.50, "category": "Medium"},
            {"name": "Snacks", "amount": 49.99, "category": "Small"},
        ]

        result = calculate_total(expenses)

        self.assertAlmostEqual(result, 300.49)

    def test_calculate_total_with_empty_list(self):
        expenses = []

        result = calculate_total(expenses)

        self.assertEqual(result, 0)

    def test_calculate_total_with_invalid_expense(self):
        invalid_expenses = [
            None,
            "Groceries",
            123,
            [],
        ]

        for expense in invalid_expenses:
            with self.subTest(expense=expense):
                with self.assertRaises(ValueError):
                    calculate_total([expense])

    def test_calculate_total_with_missing_amount(self):
        expenses = [{"name": "Groceries", "category": "Medium"}]

        with self.assertRaises(ValueError):
            calculate_total(expenses)

    def test_calculate_total_with_invalid_amount(self):
        invalid_amounts = [
            0,
            -100,
            "500",
            None,
            True,
            False,
        ]

        for amount in invalid_amounts:
            with self.subTest(amount=amount):
                expenses = [
                    {"name": "Groceries", "amount": amount, "category": "Medium"}
                ]

                with self.assertRaises(ValueError):
                    calculate_total(expenses)

    def test_calculate_total_with_non_finite_amount(self):
        invalid_amounts = [
            float("nan"),
            float("inf"),
            float("-inf"),
        ]

        for amount in invalid_amounts:
            with self.subTest(amount=amount):
                expenses = [
                    {"name": "Groceries", "amount": amount, "category": "Medium"}
                ]

                with self.assertRaises(ValueError):
                    calculate_total(expenses)

    # Get category
    def test_get_category(self):
        test_cases = [
            (50, "Small"),
            (99.99, "Small"),
            (100, "Medium"),
            (250, "Medium"),
            (499.99, "Medium"),
            (500, "Large"),
            (750, "Large"),
        ]

        for amount, expected_category in test_cases:
            with self.subTest(amount=amount):
                self.assertEqual(get_category(amount), expected_category)

    def test_get_category_with_invalid_amount(self):
        invalid_amounts = [
            0,
            -50,
            -100,
            "500",
            None,
            True,
            False,
            [],
            {},
        ]

        for amount in invalid_amounts:
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    get_category(amount)

    def test_get_category_with_non_finite_amount(self):
        invalid_amounts = [
            float("nan"),
            float("inf"),
            float("-inf"),
        ]

        for amount in invalid_amounts:
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    get_category(amount)

    def test_get_category_with_very_large_amount(self):
        result = get_category(10**100)

        self.assertEqual(result, "Large")

    # add expense

    def test_add_expense(self):
        result = add_expense("Adesh", 50)
        today = date.today().strftime("%Y-%m-%d")
        self.assertEqual(
            result,
            {
                "name": "Adesh",
                "amount": 50,
                "category": "Small",
                "date": today,
            },
        )

    def test_add_expense_with_large_amount(self):
        result = add_expense("Laptop", 750)
        today = date.today().strftime("%Y-%m-%d")
        self.assertEqual(
            result,
            {
                "name": "Laptop",
                "amount": 750,
                "category": "Large",
                "date": today,
            },
        )

    def test_add_expense_with_medium_amount(self):
        result = add_expense("Phone", 250)
        today = date.today().strftime("%Y-%m-%d")
        self.assertEqual(
            result,
            {
                "name": "Phone",
                "amount": 250,
                "category": "Medium",
                "date": today,
            },
        )

    def test_add_expense_with_empty_name(self):
        with self.assertRaises(ValueError):
            add_expense("", 250)

    def test_add_expense_with_whitespace_name(self):
        with self.assertRaises(ValueError):
            add_expense("   ", 250)

    def test_add_expense_with_non_string_name(self):
        with self.assertRaises(ValueError):
            add_expense(None, 250)

    def test_add_expense_with_zero_amount(self):
        with self.assertRaises(ValueError):
            add_expense("Groceries", 0)

    def test_add_expense_with_negative_amount(self):
        with self.assertRaises(ValueError):
            add_expense("Groceries", -100)

    def test_add_expense_with_non_numeric_amount(self):
        with self.assertRaises(ValueError):
            add_expense("Groceries", "500")

    def test_add_expense_with_nan_amount(self):
        with self.assertRaises(ValueError):
            add_expense("Groceries", float("nan"))

    def test_add_expense_with_infinite_amount(self):
        with self.assertRaises(ValueError):
            add_expense("Groceries", float("inf"))

    # valid amount

    @patch("builtins.input")
    def test_add_expense_invalid_amount(self, mock_input):
        mock_input.side_effect = ["Adesh", "abc", "-20", "75"]

        result = add_expense()
        today = date.today().strftime("%Y-%m-%d")

        self.assertEqual(
            result,
            {"name": "Adesh", "amount": 75.0, "category": "Small", "date": today},
        )
        self.assertEqual(mock_input.call_count, 4)

    # view expense

    def test_view_expense(self):
        expenses = [
            {"name": "Adesh", "amount": 50.0, "category": "Small", "date": "2026-11-07"}
        ]
        f = StringIO()

        with redirect_stdout(f):
            view_expenses(expenses)

        expected_output = "========== YOUR EXPENSES ==========\n1. Adesh | ₹50.00 | Small Expense | 2026-11-07\n=================================="
        self.assertIn(expected_output, f.getvalue())

    def test_view_expenses_empty(self):
        f = StringIO()

        with redirect_stdout(f):
            view_expenses([])

        expected_output = "No matching expenses found."
        self.assertIn(expected_output, f.getvalue())

    # filter
    def test_filtered_expenses(self):
        expenses = [
            {"name": "Adesh", "amount": 70, "category": "Small"},
            {"name": "Adesh", "amount": 250, "category": "Medium"},
            {"name": "Adesh", "amount": 700, "category": "Large"},
        ]

        result = filter_expenses(expenses, "Small")
        self.assertEqual(result, [{"name": "Adesh", "amount": 70, "category": "Small"}])

    def test_filter_expenses(self):
        expenses = [
            {"name": "Snacks", "amount": 50, "category": "Small"},
            {"name": "Groceries", "amount": 250, "category": "Medium"},
            {"name": "Laptop", "amount": 750, "category": "Large"},
            {"name": "Tea", "amount": 80, "category": "Small"},
        ]

        result = filter_expenses(expenses, "Small")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Snacks")
        self.assertEqual(result[1]["name"], "Tea")

    def test_filter_expenses_with_medium_category(self):
        expenses = [
            {"name": "Groceries", "amount": 250, "category": "Medium"},
            {"name": "Snacks", "amount": 50, "category": "Small"},
        ]

        result = filter_expenses(expenses, "Medium")

        self.assertEqual(result, [expenses[0]])

    def test_filter_expenses_with_no_matches(self):
        expenses = [
            {"name": "Snacks", "amount": 50, "category": "Small"},
        ]

        result = filter_expenses(expenses, "Large")

        self.assertEqual(result, [])

    def test_filter_expenses_with_empty_list(self):
        result = filter_expenses([], "Small")

        self.assertEqual(result, [])

    def test_filter_expenses_with_invalid_category(self):
        invalid_categories = ["", "Unknown", "small", None, 123, True]

        expenses = [{"name": "Snacks", "amount": 50, "category": "Small"}]

        for category in invalid_categories:
            with self.subTest(category=category):
                with self.assertRaises(ValueError):
                    filter_expenses(expenses, category)

    def test_filter_expenses_with_invalid_expense(self):
        invalid_expenses = [None, "Snacks", 123, []]

        for expense in invalid_expenses:
            with self.subTest(expense=expense):
                with self.assertRaises(ValueError):
                    filter_expenses([expense], "Small")

    def test_filter_expenses_with_missing_category(self):
        expenses = [{"name": "Snacks", "amount": 50}]

        with self.assertRaises(ValueError):
            filter_expenses(expenses, "Small")

    def test_filter_expenses_with_invalid_stored_category(self):
        invalid_categories = ["Unknown", "", "small", None, 123, True]

        for category in invalid_categories:
            with self.subTest(category=category):
                expenses = [{"name": "Snacks", "amount": 50, "category": category}]

                with self.assertRaises(ValueError):
                    filter_expenses(expenses, "Small")

    def test_filter_expenses_with_non_string_category(self):
        expenses = [{"name": "Groceries", "amount": 50, "category": ["Small"]}]

        with self.assertRaises(ValueError):
            filter_expenses(expenses, "Small")

    def test_filter_expenses_with_non_dictionary_record(self):
        expenses = ["invalid expense record"]

        with self.assertRaises(ValueError):
            filter_expenses(expenses, "Small")

    # category totals
    def test_category_totals(self):
        expenses = [
            {"name": "Adesh", "amount": 70, "category": "Small"},
            {"name": "Adesh", "amount": 250, "category": "Medium"},
            {"name": "Adesh", "amount": 30, "category": "Small"},
        ]

        result = calculate_category_totals(expenses)
        self.assertEqual(result, {"Small": 100, "Medium": 250, "Large": 0})
        self.assertEqual(
            calculate_category_totals([]), {"Small": 0, "Medium": 0, "Large": 0}
        )

    def test_calculate_category_totals(self):
        expenses = [
            {"name": "Snacks", "amount": 50, "category": "Small"},
            {"name": "Groceries", "amount": 250, "category": "Medium"},
            {"name": "Laptop", "amount": 750, "category": "Large"},
            {"name": "Tea", "amount": 80, "category": "Small"},
        ]

        result = calculate_category_totals(expenses)

        self.assertEqual(result, {"Small": 130, "Medium": 250, "Large": 750})

    def test_calculate_category_totals_with_decimal_amounts(self):
        expenses = [
            {"name": "Snacks", "amount": 50.50, "category": "Small"},
            {"name": "Groceries", "amount": 250.75, "category": "Medium"},
        ]

        result = calculate_category_totals(expenses)

        self.assertAlmostEqual(result["Small"], 50.50)
        self.assertAlmostEqual(result["Medium"], 250.75)
        self.assertEqual(result["Large"], 0)

    def test_calculate_category_totals_with_empty_list(self):
        result = calculate_category_totals([])

        self.assertEqual(result, {"Small": 0, "Medium": 0, "Large": 0})

    def test_calculate_category_totals_with_invalid_expense(self):
        invalid_expenses = [None, "Groceries", 123, []]

        for expense in invalid_expenses:
            with self.subTest(expense=expense):
                with self.assertRaises(ValueError):
                    calculate_category_totals([expense])

    def test_calculate_category_totals_with_missing_category(self):
        expenses = [{"name": "Groceries", "amount": 250}]

        with self.assertRaises(ValueError):
            calculate_category_totals(expenses)

    def test_calculate_category_totals_with_missing_amount(self):
        expenses = [{"name": "Groceries", "category": "Medium"}]

        with self.assertRaises(ValueError):
            calculate_category_totals(expenses)

    def test_calculate_category_totals_with_invalid_category(self):
        invalid_categories = ["", "Unknown", "small", None, 123, True]

        for category in invalid_categories:
            with self.subTest(category=category):
                expenses = [{"name": "Groceries", "amount": 250, "category": category}]

                with self.assertRaises(ValueError):
                    calculate_category_totals(expenses)

    def test_calculate_category_totals_with_mismatched_category(self):
        expenses = [{"name": "Laptop", "amount": 750, "category": "Medium"}]

        with self.assertRaises(ValueError):
            calculate_category_totals(expenses)

    def test_calculate_category_totals_with_invalid_amount(self):
        invalid_amounts = [0, -100, "500", None, True, False]

        for amount in invalid_amounts:
            with self.subTest(amount=amount):
                expenses = [
                    {"name": "Groceries", "amount": amount, "category": "Medium"}
                ]

                with self.assertRaises(ValueError):
                    calculate_category_totals(expenses)

    def test_calculate_category_totals_with_non_finite_amount(self):
        invalid_amounts = [
            float("nan"),
            float("inf"),
            float("-inf"),
        ]

        for amount in invalid_amounts:
            with self.subTest(amount=amount):
                expenses = [
                    {"name": "Groceries", "amount": amount, "category": "Medium"}
                ]

                with self.assertRaises(ValueError):
                    calculate_category_totals(expenses)

    def test_calculate_category_totals_with_list_category(self):
        expenses = [{"name": "Groceries", "amount": 50, "category": ["Small"]}]

        with self.assertRaises(ValueError):
            calculate_category_totals(expenses)

    def test_calculate_category_totals_with_dictionary_category(self):
        expenses = [{"name": "Groceries", "amount": 50, "category": {"type": "Small"}}]

        with self.assertRaises(ValueError):
            calculate_category_totals(expenses)

    # delete
    def test_delete_expense(self):
        expenses = [
            {"name": "Adesh", "amount": 70, "category": "Small"},
            {"name": "Adesh", "amount": 250, "category": "Medium"},
            {"name": "Adesh", "amount": 30, "category": "Small"},
        ]

        result = delete_expense(expenses, 0)
        self.assertEqual(result, {"name": "Adesh", "amount": 70, "category": "Small"})
        self.assertEqual(len(expenses), 2)
        self.assertNotIn({"name": "Adesh", "amount": 70, "category": "Small"}, expenses)

    # Delete expense
    def test_delete_expense(self):
        expenses = [
            {"name": "Groceries", "amount": 250, "category": "Medium"},
            {"name": "Snacks", "amount": 50, "category": "Small"},
        ]

        result = delete_expense(expenses, 0)

        self.assertEqual(
            result,
            {"name": "Groceries", "amount": 250, "category": "Medium"},
        )
        self.assertEqual(
            expenses,
            [{"name": "Snacks", "amount": 50, "category": "Small"}],
        )

    def test_delete_expense_with_invalid_index(self):
        expenses = [{"name": "Groceries", "amount": 250, "category": "Medium"}]

        invalid_indexes = [-1, 1, 5, "0", True, False, 1.5, None]

        for index in invalid_indexes:
            with self.subTest(index=index):
                with self.assertRaises(ValueError):
                    delete_expense(expenses, index)

    def test_delete_expense_does_not_modify_list_on_invalid_index(self):
        expenses = [
            {"name": "Groceries", "amount": 250, "category": "Medium"},
            {"name": "Snacks", "amount": 50, "category": "Small"},
        ]

        original_expenses = [
            {"name": "Groceries", "amount": 250, "category": "Medium"},
            {"name": "Snacks", "amount": 50, "category": "Small"},
        ]

        with self.assertRaises(ValueError):
            delete_expense(expenses, -1)

        self.assertEqual(expenses, original_expenses)

    def test_delete_expense_from_empty_list(self):
        expenses = []

        with self.assertRaises(ValueError):
            delete_expense(expenses, 0)

        self.assertEqual(expenses, [])

    # edit
    def test_edit_expense(self):
        expenses = [
            {"name": "Grocerikes", "amount": 700, "category": "Large"},
            {"name": "Bus", "amount": 50, "category": "Small"},
        ]
        updated_expense = edit_expense(expenses, 0, "Vegetables", 70)

        self.assertEqual(
            updated_expense, {"name": "Vegetables", "amount": 70, "category": "Small"}
        )
        self.assertEqual(
            expenses,
            [
                {"name": "Vegetables", "amount": 70, "category": "Small"},
                {"name": "Bus", "amount": 50, "category": "Small"},
            ],
        )
        self.assertEqual(
            expenses[1], {"name": "Bus", "amount": 50, "category": "Small"}
        )

    # Edit expense
    def test_edit_expense(self):
        expenses = [{"name": "Groceries", "amount": 250, "category": "Medium"}]

        result = edit_expense(expenses, 0, "Laptop", 750)

        self.assertEqual(result["name"], "Laptop")
        self.assertEqual(result["amount"], 750)
        self.assertEqual(result["category"], "Large")

    def test_edit_expense_recalculates_category(self):
        expenses = [{"name": "Groceries", "amount": 750, "category": "Large"}]

        result = edit_expense(expenses, 0, "Snacks", 50)

        self.assertEqual(result["category"], "Small")

    def test_edit_expense_strips_name(self):
        expenses = [{"name": "Groceries", "amount": 250, "category": "Medium"}]

        result = edit_expense(expenses, 0, "  Laptop  ", 750)

        self.assertEqual(result["name"], "Laptop")

    def test_edit_expense_with_invalid_index(self):
        expenses = [{"name": "Groceries", "amount": 250, "category": "Medium"}]

        invalid_indexes = [-1, 1, 5, "0", True, 1.5]

        for index in invalid_indexes:
            with self.subTest(index=index):
                with self.assertRaises(ValueError):
                    edit_expense(expenses, index, "Laptop", 750)

    def test_edit_expense_with_invalid_name(self):
        expenses = [{"name": "Groceries", "amount": 250, "category": "Medium"}]

        invalid_names = ["", "   ", None, 123]

        for name in invalid_names:
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    edit_expense(expenses, 0, name, 750)

    def test_edit_expense_with_invalid_amount(self):
        expenses = [{"name": "Groceries", "amount": 250, "category": "Medium"}]

        invalid_amounts = [
            0,
            -100,
            "500",
            None,
            True,
            float("nan"),
            float("inf"),
            float("-inf"),
        ]

        for amount in invalid_amounts:
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    edit_expense(expenses, 0, "Laptop", amount)

    def test_edit_expense_does_not_modify_original_on_invalid_amount(self):
        expenses = [{"name": "Groceries", "amount": 250, "category": "Medium"}]

        original_expenses = [{"name": "Groceries", "amount": 250, "category": "Medium"}]

        with self.assertRaises(ValueError):
            edit_expense(expenses, 0, "Laptop", -500)

        self.assertEqual(expenses, original_expenses)

    # search
    def test_search(self):
        expenses = [
            {"name": "Groceries", "amount": 700, "category": "Large"},
            {"name": "Bus", "amount": 50, "category": "Small"},
            {"name": "Groceries", "amount": 250, "category": "Medium"},
        ]
        result = search_expenses(expenses, "gro")

        self.assertEqual(
            result,
            [
                {"name": "Groceries", "amount": 700, "category": "Large"},
                {"name": "Groceries", "amount": 250, "category": "Medium"},
            ],
        )
        self.assertEqual(len(search_expenses(expenses, "GRO")), 2)
        self.assertEqual(len(search_expenses(expenses, "bus")), 1)
        self.assertEqual(search_expenses(expenses, "pizza"), [])

    # Search expenses
    def test_search_expenses(self):
        expenses = [
            {"name": "Laptop", "amount": 50000, "category": "Large"},
            {"name": "Groceries", "amount": 250, "category": "Medium"},
        ]

        result = search_expenses(expenses, "Laptop")

        self.assertEqual(result, [expenses[0]])

    def test_search_expenses_case_insensitive(self):
        expenses = [
            {"name": "Laptop", "amount": 50000, "category": "Large"},
            {"name": "Groceries", "amount": 250, "category": "Medium"},
        ]

        result = search_expenses(expenses, "lApToP")

        self.assertEqual(result, [expenses[0]])

    def test_search_expenses_partial_match(self):
        expenses = [
            {"name": "Laptop", "amount": 50000, "category": "Large"},
            {"name": "Laptop Stand", "amount": 1200, "category": "Large"},
            {"name": "Groceries", "amount": 250, "category": "Medium"},
        ]

        result = search_expenses(expenses, "laptop")

        self.assertEqual(result, expenses[:2])

    def test_search_expenses_with_whitespace(self):
        expenses = [
            {"name": "Laptop", "amount": 50000, "category": "Large"},
        ]

        result = search_expenses(expenses, "  Laptop  ")

        self.assertEqual(result, [expenses[0]])

    def test_search_expenses_with_invalid_search_term(self):
        expenses = [
            {"name": "Laptop", "amount": 50000, "category": "Large"},
        ]

        invalid_terms = ["", "   ", None, 123, 45.5, True]

        for search_term in invalid_terms:
            with self.subTest(search_term=search_term):
                with self.assertRaises(ValueError):
                    search_expenses(expenses, search_term)

    def test_search_expenses_with_no_match(self):
        expenses = [
            {"name": "Laptop", "amount": 50000, "category": "Large"},
            {"name": "Groceries", "amount": 250, "category": "Medium"},
        ]

        result = search_expenses(expenses, "Mobile")

        self.assertEqual(result, [])

    def test_search_expenses_with_empty_list(self):
        expenses = []

        result = search_expenses(expenses, "Laptop")

        self.assertEqual(result, [])

    # filter expenses by date
    def test_filter_expenses_by_date(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 70,
                "category": "Small",
                "date": "2026-11-07",
            },
            {
                "name": "Bus Fare",
                "amount": 30,
                "category": "Small",
                "date": "2026-11-07",
            },
            {"name": "Shoes", "amount": 700, "category": "Large", "date": "2026-11-06"},
        ]

        result = filter_expenses_by_date(expenses, "2026-11-07")

        self.assertEqual(
            result,
            [
                {
                    "name": "Groceries",
                    "amount": 70,
                    "category": "Small",
                    "date": "2026-11-07",
                },
                {
                    "name": "Bus Fare",
                    "amount": 30,
                    "category": "Small",
                    "date": "2026-11-07",
                },
            ],
        )

    def test_filter_expenses_by_date_no_match(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 70,
                "category": "Small",
                "date": "2026-11-07",
            },
            {"name": "Shoes", "amount": 700, "category": "Large", "date": "2026-11-06"},
        ]

        result = filter_expenses_by_date(expenses, "2026-11-05")

        self.assertEqual(result, [])

    def test_filter_expenses_by_date_missing_date(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 70,
                "category": "Small",
                "date": "2026-11-07",
            },
            {"name": "Bus Fare", "amount": 30, "category": "Small"},
        ]

        result = filter_expenses_by_date(expenses, "2026-11-07")

        self.assertEqual(
            result,
            [
                {
                    "name": "Groceries",
                    "amount": 70,
                    "category": "Small",
                    "date": "2026-11-07",
                },
            ],
        )

    # Filter expenses by date
    def test_filter_expenses_by_date(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 250,
                "category": "Medium",
                "date": "2026-11-10",
            },
            {"name": "Snacks", "amount": 50, "category": "Small", "date": "2026-11-09"},
            {
                "name": "Laptop",
                "amount": 750,
                "category": "Large",
                "date": "2026-11-10",
            },
        ]

        result = filter_expenses_by_date(expenses, "2026-11-10")

        self.assertEqual(result, [expenses[0], expenses[2]])

    def test_filter_expenses_by_date_with_no_match(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 250,
                "category": "Medium",
                "date": "2026-11-10",
            },
        ]

        result = filter_expenses_by_date(expenses, "2026-11-09")

        self.assertEqual(result, [])

    def test_filter_expenses_by_date_with_invalid_date(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 250,
                "category": "Medium",
                "date": "2026-11-10",
            },
        ]

        invalid_dates = [
            "",
            "   ",
            "2026-02-30",
            "10-11-2026",
            None,
            12345,
            True,
        ]

        for target_date in invalid_dates:
            with self.subTest(target_date=target_date):
                with self.assertRaises(ValueError):
                    filter_expenses_by_date(expenses, target_date)

    def test_filter_expenses_by_date_with_missing_date(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 250,
                "category": "Medium",
                "date": "2026-11-10",
            },
            {"name": "Snacks", "amount": 50, "category": "Small"},
            {"name": "Laptop", "amount": 750, "category": "Large", "date": ""},
        ]

        result = filter_expenses_by_date(expenses, "2026-11-10")

        self.assertEqual(result, [expenses[0]])

    def test_filter_expenses_by_date_with_empty_list(self):
        expenses = []

        result = filter_expenses_by_date(expenses, "2026-11-10")

        self.assertEqual(result, [])

    # valid date
    def test_valid_date(self):
        dates_true = ["2026-11-07", "2026-01-01", "2024-02-29"]
        dates_false = [
            "07-11-2026",
            "2026-15-40",
            "hello",
            "",
            "2026-02-30",
            "2025-02-29",
        ]
        for date in dates_true:
            self.assertTrue(validate_date(date))
        for date in dates_false:
            self.assertFalse(validate_date(date))

    # Validate date
    def test_validate_date(self):
        valid_dates = [
            "2026-11-10",
            "2024-02-29",
            "2000-01-01",
        ]

        for date_string in valid_dates:
            with self.subTest(date_string=date_string):
                self.assertTrue(validate_date(date_string))

    def test_validate_date_with_invalid_calendar_dates(self):
        invalid_dates = [
            "2026-02-30",
            "2026-04-31",
            "2025-02-29",
            "2026-13-10",
            "2026-00-10",
            "2026-11-00",
        ]

        for date_string in invalid_dates:
            with self.subTest(date_string=date_string):
                self.assertFalse(validate_date(date_string))

    def test_validate_date_with_invalid_formats(self):
        invalid_dates = [
            "10-11-2026",
            "10/11/2026",
            "2026/11/10",
            "November 10, 2026",
            "",
            "   ",
        ]

        for date_string in invalid_dates:
            with self.subTest(date_string=date_string):
                self.assertFalse(validate_date(date_string))

    def test_validate_date_with_non_string_values(self):
        invalid_values = [
            None,
            12345,
            10.5,
            True,
            False,
            [],
            {},
        ]

        for value in invalid_values:
            with self.subTest(value=value):
                self.assertFalse(validate_date(value))

    # filter by category and date
    def test_filter_expenses_by_category_and_date(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 70,
                "category": "Small",
                "date": "2026-11-07",
            },
            {
                "name": "Bus Fare",
                "amount": 30,
                "category": "Small",
                "date": "2026-11-07",
            },
            {"name": "Shoes", "amount": 700, "category": "Large", "date": "2026-11-07"},
            {
                "name": "Coffee",
                "amount": 150,
                "category": "Medium",
                "date": "2026-11-06",
            },
        ]

        result = filter_expenses_by_category_and_date(expenses, "Small", "2026-11-07")

        self.assertEqual(
            result,
            [
                {
                    "name": "Groceries",
                    "amount": 70,
                    "category": "Small",
                    "date": "2026-11-07",
                },
                {
                    "name": "Bus Fare",
                    "amount": 30,
                    "category": "Small",
                    "date": "2026-11-07",
                },
            ],
        )

    def test_filter_expenses_by_category_and_date_no_match(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 70,
                "category": "Small",
                "date": "2026-11-07",
            },
            {"name": "Shoes", "amount": 700, "category": "Large", "date": "2026-11-07"},
            {
                "name": "Coffee",
                "amount": 150,
                "category": "Medium",
                "date": "2026-11-06",
            },
        ]

        result = filter_expenses_by_category_and_date(expenses, "Medium", "2026-11-07")

        self.assertEqual(result, [])

    def test_filter_expenses_by_category_and_date_missing_date(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 70,
                "category": "Small",
                "date": "2026-11-07",
            },
            {"name": "Old Expense", "amount": 50, "category": "Small"},
        ]

        result = filter_expenses_by_category_and_date(expenses, "Small", "2026-11-07")

        self.assertEqual(
            result,
            [
                {
                    "name": "Groceries",
                    "amount": 70,
                    "category": "Small",
                    "date": "2026-11-07",
                },
            ],
        )

    # Filter expenses by category and date
    def test_filter_expenses_by_category_and_date(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 250,
                "category": "Medium",
                "date": "2026-11-10",
            },
            {"name": "Snacks", "amount": 50, "category": "Small", "date": "2026-11-10"},
            {
                "name": "Laptop",
                "amount": 750,
                "category": "Large",
                "date": "2026-11-10",
            },
            {"name": "Tea", "amount": 30, "category": "Small", "date": "2026-11-09"},
        ]

        result = filter_expenses_by_category_and_date(expenses, "Small", "2026-11-10")

        self.assertEqual(result, [expenses[1]])

    def test_filter_expenses_by_category_and_date_with_invalid_category(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 250,
                "category": "Medium",
                "date": "2026-11-10",
            },
        ]

        invalid_categories = [
            "",
            "   ",
            "small",
            "Invalid",
            None,
            123,
            True,
        ]

        for category in invalid_categories:
            with self.subTest(category=category):
                with self.assertRaises(ValueError):
                    filter_expenses_by_category_and_date(
                        expenses, category, "2026-11-10"
                    )

    def test_filter_expenses_by_category_and_date_with_invalid_date(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 250,
                "category": "Medium",
                "date": "2026-11-10",
            },
        ]

        invalid_dates = [
            "",
            "   ",
            "2026-02-30",
            "10-11-2026",
            None,
            12345,
            True,
        ]

        for target_date in invalid_dates:
            with self.subTest(target_date=target_date):
                with self.assertRaises(ValueError):
                    filter_expenses_by_category_and_date(
                        expenses, "Medium", target_date
                    )

    def test_filter_expenses_by_category_and_date_with_no_match(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 250,
                "category": "Medium",
                "date": "2026-11-10",
            },
        ]

        result = filter_expenses_by_category_and_date(expenses, "Small", "2026-11-10")

        self.assertEqual(result, [])

    def test_filter_expenses_by_category_and_date_with_empty_list(self):
        expenses = []

        result = filter_expenses_by_category_and_date(expenses, "Medium", "2026-11-10")

        self.assertEqual(result, [])

    def test_filter_expenses_by_category_and_date_with_missing_date(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 250,
                "category": "Medium",
                "date": "2026-11-10",
            },
            {"name": "Snacks", "amount": 50, "category": "Small"},
        ]

        result = filter_expenses_by_category_and_date(expenses, "Small", "2026-11-10")

        self.assertEqual(result, [])

    def test_filter_expenses_by_category_and_date(self):
        expenses = [
            {"name": "Snacks", "amount": 50, "category": "Small", "date": "2026-11-10"},
            {
                "name": "Groceries",
                "amount": 250,
                "category": "Medium",
                "date": "2026-11-10",
            },
            {"name": "Tea", "amount": 80, "category": "Small", "date": "2026-11-09"},
        ]

        result = filter_expenses_by_category_and_date(expenses, "Small", "2026-11-10")

        self.assertEqual(result, [expenses[0]])

    def test_filter_expenses_by_category_and_date_with_no_matches(self):
        expenses = [
            {"name": "Snacks", "amount": 50, "category": "Small", "date": "2026-11-10"},
        ]

        result = filter_expenses_by_category_and_date(expenses, "Large", "2026-11-10")

        self.assertEqual(result, [])

    def test_filter_expenses_by_category_and_date_with_empty_list(self):
        result = filter_expenses_by_category_and_date([], "Small", "2026-11-10")

        self.assertEqual(result, [])

    def test_filter_expenses_by_category_and_date_with_invalid_category(self):
        invalid_categories = ["", "Unknown", "small", None, 123, True]

        for category in invalid_categories:
            with self.subTest(category=category):
                with self.assertRaises(ValueError):
                    filter_expenses_by_category_and_date([], category, "2026-11-10")

    def test_filter_expenses_by_category_and_date_with_invalid_date(self):
        invalid_dates = [
            "",
            "2026-02-30",
            "10-11-2026",
            None,
            123,
        ]

        for target_date in invalid_dates:
            with self.subTest(target_date=target_date):
                with self.assertRaises(ValueError):
                    filter_expenses_by_category_and_date([], "Small", target_date)

    def test_filter_expenses_by_category_and_date_with_invalid_expense(self):
        invalid_expenses = [None, "Snacks", 123, []]

        for expense in invalid_expenses:
            with self.subTest(expense=expense):
                with self.assertRaises(ValueError):
                    filter_expenses_by_category_and_date(
                        [expense], "Small", "2026-11-10"
                    )

    def test_filter_expenses_by_category_and_date_with_missing_fields(self):
        invalid_expenses = [
            {"name": "Snacks", "amount": 50, "date": "2026-11-10"},
            {"name": "Snacks", "amount": 50, "category": "Small"},
        ]

        for expense in invalid_expenses:
            with self.subTest(expense=expense):
                with self.assertRaises(ValueError):
                    filter_expenses_by_category_and_date(
                        [expense], "Small", "2026-11-10"
                    )

    def test_filter_expenses_by_category_and_date_with_invalid_stored_category(self):
        invalid_categories = ["Unknown", "", "small", None, 123, True]

        for category in invalid_categories:
            with self.subTest(category=category):
                expenses = [
                    {
                        "name": "Snacks",
                        "amount": 50,
                        "category": category,
                        "date": "2026-11-10",
                    }
                ]

                with self.assertRaises(ValueError):
                    filter_expenses_by_category_and_date(
                        expenses, "Small", "2026-11-10"
                    )

    def test_filter_expenses_by_category_and_date_with_invalid_stored_date(self):
        invalid_dates = [
            "",
            "2026-02-30",
            "10-11-2026",
            None,
            123,
        ]

        for target_date in invalid_dates:
            with self.subTest(target_date=target_date):
                expenses = [
                    {
                        "name": "Snacks",
                        "amount": 50,
                        "category": "Small",
                        "date": target_date,
                    }
                ]

                with self.assertRaises(ValueError):
                    filter_expenses_by_category_and_date(
                        expenses, "Small", "2026-11-10"
                    )

    # filter by month
    def test_filter_expenses_by_month(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 700,
                "category": "Large",
                "date": "2026-11-07",
            },
            {
                "name": "Bus Fare",
                "amount": 30,
                "category": "Small",
                "date": "2026-11-15",
            },
            {"name": "Shoes", "amount": 700, "category": "Large", "date": "2026-10-20"},
            {
                "name": "Coffee",
                "amount": 150,
                "category": "Medium",
                "date": "2025-11-10",
            },
            {"name": "Old Expense", "amount": 50, "category": "Small"},
        ]

        result = filter_expenses_by_month(expenses, 2026, 11)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Groceries")
        self.assertEqual(result[1]["name"], "Bus Fare")

    def test_filter_expenses_by_month_no_matches(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 700,
                "category": "Large",
                "date": "2026-11-07",
            },
            {
                "name": "Bus Fare",
                "amount": 30,
                "category": "Small",
                "date": "2026-11-15",
            },
        ]

        result = filter_expenses_by_month(expenses, 2026, 12)

        self.assertEqual(result, [])

    def test_filter_expenses_by_month_missing_date(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 700,
                "category": "Large",
                "date": "2026-11-07",
            },
            {"name": "Old Expense", "amount": 50, "category": "Small"},
        ]

        result = filter_expenses_by_month(expenses, 2026, 11)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Groceries")

    # Filter expenses by month
    def test_filter_expenses_by_month(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 250,
                "category": "Medium",
                "date": "2026-11-10",
            },
            {"name": "Snacks", "amount": 50, "category": "Small", "date": "2026-11-15"},
            {
                "name": "Laptop",
                "amount": 750,
                "category": "Large",
                "date": "2026-10-10",
            },
            {"name": "Tea", "amount": 30, "category": "Small", "date": "2025-11-09"},
        ]

        result = filter_expenses_by_month(expenses, 2026, 11)

        self.assertEqual(result, expenses[:2])

    def test_filter_expenses_by_month_with_invalid_year(self):
        expenses = []

        invalid_years = [
            999,
            10000,
            0,
            -2026,
            "2026",
            2026.5,
            None,
            True,
        ]

        for year in invalid_years:
            with self.subTest(year=year):
                with self.assertRaises(ValueError):
                    filter_expenses_by_month(expenses, year, 11)

    def test_filter_expenses_by_month_with_invalid_month(self):
        expenses = []

        invalid_months = [
            0,
            13,
            -1,
            "11",
            11.5,
            None,
            True,
        ]

        for month in invalid_months:
            with self.subTest(month=month):
                with self.assertRaises(ValueError):
                    filter_expenses_by_month(expenses, 2026, month)

    def test_filter_expenses_by_month_with_missing_dates(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 250,
                "category": "Medium",
                "date": "2026-11-10",
            },
            {"name": "Snacks", "amount": 50, "category": "Small"},
            {"name": "Tea", "amount": 30, "category": "Small", "date": ""},
            {"name": "Coffee", "amount": 80, "category": "Small", "date": None},
        ]

        result = filter_expenses_by_month(expenses, 2026, 11)

        self.assertEqual(result, [expenses[0]])

    def test_filter_expenses_by_month_with_invalid_stored_dates(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 250,
                "category": "Medium",
                "date": "2026-11-10",
            },
            {"name": "Snacks", "amount": 50, "category": "Small", "date": "2026-02-30"},
            {"name": "Tea", "amount": 30, "category": "Small", "date": "10-11-2026"},
            {"name": "Coffee", "amount": 80, "category": "Small", "date": "invalid"},
        ]

        result = filter_expenses_by_month(expenses, 2026, 11)

        self.assertEqual(result, [expenses[0]])

    def test_filter_expenses_by_month_with_no_match(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 250,
                "category": "Medium",
                "date": "2026-10-10",
            },
        ]

        result = filter_expenses_by_month(expenses, 2026, 11)

        self.assertEqual(result, [])

    def test_filter_expenses_by_month_with_empty_list(self):
        expenses = []

        result = filter_expenses_by_month(expenses, 2026, 11)

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
