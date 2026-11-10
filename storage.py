import json
import math
import os
import shutil
from datetime import datetime

from expense_manager import get_category
from tempfile import NamedTemporaryFile


def load_expenses(file_path="expenses.json"):
    try:
        with open(file_path, "r") as file:
            loaded_expenses = json.load(file)

            required_fields = {"name", "amount", "category"}
            allowed_categories = {"Small", "Medium", "Large"}

            # Ensure the stored data is a list.
            if not isinstance(loaded_expenses, list):
                print("Warning: Expense data must be a list.")
                return []

            # Validate expense structure.
            if not all(
                isinstance(expense, dict) and required_fields.issubset(expense)
                for expense in loaded_expenses
            ):
                print("Warning: Expense data has missing or invalid fields.")
                return []

            # Validate expense values.
            if not all(
                isinstance(expense["name"], str)
                and bool(expense["name"].strip())
                and isinstance(expense["amount"], (int, float))
                and not isinstance(expense["amount"], bool)
                and math.isfinite(expense["amount"])
                and expense["amount"] > 0
                and isinstance(expense["category"], str)
                and expense["category"] in allowed_categories
                for expense in loaded_expenses
            ):
                print("Warning: Expense data contains invalid values.")
                return []

            # Validate category consistency.
            if not all(
                expense["category"] == get_category(expense["amount"])
                for expense in loaded_expenses
            ):
                print("Warning: Expense categories do not match their amounts.")
                return []

            # Validate provided dates.
            if not all(is_valid_expense_date(expense) for expense in loaded_expenses):
                print("Warning: Expense data contains invalid dates.")
                return []

            return loaded_expenses

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Warning: Expense file is corrupted.")
        return []


def save_expenses(expenses, file_path="expenses.json"):
    temp_file_path = None

    try:
        # Create a backup of the existing file.
        if os.path.exists(file_path):
            shutil.copy2(file_path, f"{file_path}.bak")

        # Create a temporary file in the same directory.
        directory = os.path.dirname(os.path.abspath(file_path))

        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=directory,
            prefix=".expenses_",
            suffix=".tmp",
            delete=False,
        ) as temp_file:
            temp_file_path = temp_file.name

            # Write the complete data.
            json.dump(expenses, temp_file, indent=4)

            # Ensure data is flushed to disk.
            temp_file.flush()
            os.fsync(temp_file.fileno())

        # Replace the original file only after writing succeeds.
        os.replace(temp_file_path, file_path)
        temp_file_path = None

    finally:
        # Remove the temporary file if saving failed.
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def is_valid_expense_date(expense):
    # Missing or empty dates are allowed for older records.
    expense_date = expense.get("date")

    if not expense_date:
        return True

    # Provided dates must be valid YYYY-MM-DD dates.
    try:
        datetime.strptime(expense_date, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False
