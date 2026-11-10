import os, unittest, json
from pathlib import Path
from tempfile import TemporaryDirectory, NamedTemporaryFile
from unittest.mock import patch

from storage import save_expenses, load_expenses, is_valid_expense_date


class TestStorage(unittest.TestCase):

    def test_save_and_load_expenses(self):
        expenses = [
            {"name": "Adesh", "amount": 100.0, "category": "Medium"},
            {"name": "Adesh", "amount": 50.0, "category": "Small"},
        ]

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test_expenses.json"

            save_expenses(expenses, file_path)
            loaded_expenses = load_expenses(file_path)
            self.assertEqual(loaded_expenses, expenses)

    def test_load_missing_file(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "missing.json"
            result = load_expenses(file_path)
            self.assertEqual(result, [])

    def test_load_corrupted_file(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "corrupted.json"
            file_path.write_text("{ this is not valid json")
            result = load_expenses(file_path)
            self.assertEqual(result, [])

    def test_load_expenses_with_zero_amount(self):
        expenses = [{"name": "Groceries", "amount": 0, "category": "Small"}]
        self.write_expenses(expenses)

        result = load_expenses(self.file_path)

        self.assertEqual(result, [])

    def test_load_expenses_with_negative_amount(self):
        expenses = [{"name": "Groceries", "amount": -100, "category": "Small"}]
        self.write_expenses(expenses)

        result = load_expenses(self.file_path)

        self.assertEqual(result, [])

    def test_load_expenses_with_non_numeric_amount(self):
        invalid_amounts = ["500", None, True, False]

        for amount in invalid_amounts:
            with self.subTest(amount=amount):
                expenses = [
                    {"name": "Groceries", "amount": amount, "category": "Medium"}
                ]
                self.write_expenses(expenses)

                result = load_expenses(self.file_path)

                self.assertEqual(result, [])

    def test_load_expenses_with_non_finite_amount(self):
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
                self.write_expenses(expenses)

                result = load_expenses(self.file_path)

                self.assertEqual(result, [])

    def test_load_expenses_with_mismatched_category(self):
        expenses = [{"name": "Laptop", "amount": 750, "category": "Medium"}]
        self.write_expenses(expenses)

        result = load_expenses(self.file_path)

        self.assertEqual(result, [])

    def test_load_expenses_with_valid_category_boundaries(self):
        expenses = [
            {"name": "Snacks", "amount": 99.99, "category": "Small"},
            {"name": "Groceries", "amount": 100, "category": "Medium"},
            {"name": "Shopping", "amount": 499.99, "category": "Medium"},
            {"name": "Laptop", "amount": 500, "category": "Large"},
        ]
        self.write_expenses(expenses)

        result = load_expenses(self.file_path)

        self.assertEqual(result, expenses)

    def test_save_expenses_preserves_original_file_on_write_failure(self):
        original_expenses = [{"name": "Groceries", "amount": 200, "category": "Medium"}]

        new_expenses = [{"name": "Laptop", "amount": 800, "category": "Large"}]

        self.write_expenses(original_expenses)

        # Simulate a failure while writing JSON.
        with patch("storage.json.dump", side_effect=OSError("Disk error")):
            with self.assertRaises(OSError):
                save_expenses(new_expenses, self.file_path)

        # Original file must still contain its previous data.
        loaded_expenses = load_expenses(self.file_path)

        self.assertEqual(loaded_expenses, original_expenses)

        # Temporary file should be cleaned up.
        directory = os.path.dirname(os.path.abspath(self.file_path))
        temp_files = [
            filename
            for filename in os.listdir(directory)
            if filename.startswith(".expenses_") and filename.endswith(".tmp")
        ]

        self.assertEqual(temp_files, [])

    def test_save_expenses_creates_backup_of_previous_data(self):
        original_expenses = [{"name": "Groceries", "amount": 200, "category": "Medium"}]

        new_expenses = [{"name": "Laptop", "amount": 800, "category": "Large"}]

        self.write_expenses(original_expenses)

        save_expenses(new_expenses, self.file_path)

        backup_file_path = f"{self.file_path}.bak"

        self.assertTrue(os.path.exists(backup_file_path))

        with open(backup_file_path, "r") as file:
            backup_expenses = json.load(file)

        self.assertEqual(backup_expenses, original_expenses)

        self.assertEqual(load_expenses(self.file_path), new_expenses)

    # validation

    def write_test_data(self, data):
        """Write test data to a temporary JSON file."""
        temp_file = NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump(data, temp_file)
        temp_file.close()
        return temp_file.name

    def test_load_expenses_invalid_top_level_data(self):
        file_path = self.write_test_data(
            {"name": "Groceries", "amount": 700, "category": "Large"}
        )

        result = load_expenses(file_path)

        self.assertEqual(result, [])

    def test_load_expenses_missing_required_field(self):
        expenses = [{"name": "Groceries", "amount": 700}]
        file_path = self.write_test_data(expenses)

        result = load_expenses(file_path)

        self.assertEqual(result, [])

    def test_load_expenses_empty_name(self):
        expenses = [{"name": "   ", "amount": 700, "category": "Large"}]
        file_path = self.write_test_data(expenses)

        result = load_expenses(file_path)

        self.assertEqual(result, [])

    def test_load_expenses_invalid_amount(self):
        expenses = [{"name": "Groceries", "amount": "seven", "category": "Large"}]
        file_path = self.write_test_data(expenses)

        result = load_expenses(file_path)

        self.assertEqual(result, [])

    def test_load_expenses_invalid_category(self):
        expenses = [{"name": "Groceries", "amount": 700, "category": "Unknown"}]
        file_path = self.write_test_data(expenses)

        result = load_expenses(file_path)

        self.assertEqual(result, [])

    def test_load_expenses_valid_data(self):
        expenses = [{"name": "Groceries", "amount": 700, "category": "Large"}]
        file_path = self.write_test_data(expenses)

        result = load_expenses(file_path)

        self.assertEqual(result, expenses)

    def test_save_expenses_creates_backup(self):
        original_expenses = [{"name": "Groceries", "amount": 700, "category": "Large"}]
        updated_expenses = [{"name": "Bus Fare", "amount": 30, "category": "Small"}]

        file_path = self.write_test_data(original_expenses)
        save_expenses(updated_expenses, file_path)
        self.assertTrue(os.path.exists(f"{file_path}.bak"))

        with open(f"{file_path}.bak", "r") as file:
            backup_data = json.load(file)
        self.assertEqual(backup_data, original_expenses)

        with open(file_path, "r") as file:
            saved_data = json.load(file)
        self.assertEqual(saved_data, updated_expenses)

    # date validation

    def test_valid_expense_date(self):
        expense = {"date": "2026-11-09"}
        result = is_valid_expense_date(expense)
        self.assertTrue(result)

    def test_expense_date_missing(self):
        expense = {"name": "Groceries"}
        result = is_valid_expense_date(expense)
        self.assertTrue(result)

    def test_expense_date_empty(self):
        expense = {"date": ""}
        result = is_valid_expense_date(expense)
        self.assertTrue(result)

    def test_expense_date_invalid_calendar_date(self):
        expense = {"date": "2026-02-30"}
        result = is_valid_expense_date(expense)
        self.assertFalse(result)

    def test_expense_date_invalid_format(self):
        expense = {"date": "09-11-2026"}
        result = is_valid_expense_date(expense)
        self.assertFalse(result)

    def test_expense_date_invalid_string(self):
        expense = {"date": "hello"}
        result = is_valid_expense_date(expense)
        self.assertFalse(result)

    def test_load_expenses_valid_date(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 700,
                "category": "Large",
                "date": "2026-11-09",
            }
        ]
        file_path = self.write_test_data(expenses)
        result = load_expenses(file_path)
        self.assertEqual(result, expenses)

    def test_load_expenses_missing_date(self):
        expenses = [{"name": "Groceries", "amount": 700, "category": "Large"}]
        file_path = self.write_test_data(expenses)
        result = load_expenses(file_path)
        self.assertEqual(result, expenses)

    def test_load_expenses_invalid_date(self):
        expenses = [
            {
                "name": "Groceries",
                "amount": 700,
                "category": "Large",
                "date": "2026-02-30",
            }
        ]
        file_path = self.write_test_data(expenses)
        result = load_expenses(file_path)
        self.assertEqual(result, [])

    # empty file

    def test_load_expenses_empty_file(self):
        with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
            file_path = temp_file.name

        result = load_expenses(file_path)
        self.assertEqual(result, [])

    def test_save_expenses_without_existing_file(self):
        expenses = [{"name": "Groceries", "amount": 700, "category": "Large"}]

        with TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "expenses.json")

            save_expenses(expenses, file_path)

            self.assertTrue(os.path.exists(file_path))
            self.assertFalse(os.path.exists(f"{file_path}.bak"))

            with open(file_path, "r") as file:
                saved_data = json.load(file)

            self.assertEqual(saved_data, expenses)
