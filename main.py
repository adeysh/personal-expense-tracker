from datetime import datetime
import math

from expense_manager import (
    add_expense,
    calculate_total,
    validate_date,
    view_expenses,
    filter_expenses,
    calculate_category_totals,
    delete_expense,
    edit_expense,
    search_expenses,
    filter_expenses_by_date,
    filter_expenses_by_category_and_date,
    filter_expenses_by_month,
)
from storage import load_expenses, save_expenses


def get_valid_category():
    allowed_categories = {"Small", "Medium", "Large"}

    while True:
        category = (
            input(
                "Which category do you want the expenses for: Small, Medium, or Large?\n"
            )
            .strip()
            .title()
        )

        if category in allowed_categories:
            return category

        print("Invalid category. Please choose Small, Medium, or Large.")


def get_valid_date():
    while True:
        target_date = input("Enter the date in YYYY-MM-DD format: ")
        is_valid = validate_date(target_date)
        if is_valid:
            return target_date

        print("Invalid date. Please enter a valid date.")


def get_expense_index(expenses):
    while True:
        try:
            expense_number = int(input("Enter the expense number:\n"))
        except ValueError:
            print(f"Please enter a number between 1 and {len(expenses)}.")
            continue

        if 1 <= expense_number <= len(expenses):
            return expense_number - 1

        print(f"Please enter a number between 1 and {len(expenses)}.")


def get_valid_name():
    while True:
        name = input("Enter new name: ").strip()

        if name:
            return name

        print("Name cannot be empty.")


def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter new amount: "))

            if amount > 0 and math.isfinite(amount):
                return amount

            print("Amount should be greater than zero.")

        except ValueError:
            print("Please enter a valid amount.")


def get_valid_year():
    while True:
        try:
            target_year = int(input("Enter year: "))

            if 1000 <= target_year <= 9999:
                return target_year
            else:
                print("Enter a valid 4-digit year.\n")

        except ValueError:
            print("Enter a valid numeric year.\n")


def get_valid_month():
    while True:
        try:
            target_month = int(input("Enter month (1-12): "))

            if 1 <= target_month <= 12:
                return target_month
            else:
                print("Enter a valid month (1-12).\n")

        except ValueError:
            print("Enter a valid numeric month.\n")


def get_valid_search_term():
    while True:
        search_term = input("Enter Search Term: ").strip()

        if search_term:
            return search_term

        print("Search term cannot be empty. Please try again.")


def main():
    print("Welcome to Expense Tracker!")

    expenses = load_expenses()

    while True:
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Total")
        print("4. Exit")
        print("5. Filter Expenses by Category")
        print("6. View Category Totals")
        print("7. Delete Expense")
        print("8. Edit Expense")
        print("9. Search Expenses")
        print("10. Filter Expenses by Date")
        print("11. Filter Expenses by Category and Date")
        print("12. View Monthly Expense Summary")

        choice = input("Choose an option: ")

        if choice == "1":
            name = get_valid_name()
            money_spent = get_valid_amount()
            new_expense = add_expense(name, money_spent)
            expenses.append(new_expense)
            save_expenses(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            if not expenses:
                print("No expenses recorded yet.")
            else:
                total = calculate_total(expenses)
                print(f"Total expenses: ₹{total:.2f}")
            print("\n")
        elif choice == "4":
            print("Goodbye!")
            break
        elif choice == "5":
            category = get_valid_category()

            filtered_expenses = filter_expenses(expenses, category)
            view_expenses(filtered_expenses)
        elif choice == "6":
            category_totals = calculate_category_totals(expenses)

            print("========== YOUR CATEGORY TOTALS ==========")

            for category, total in category_totals.items():
                print(f"{category} | Total: ₹{total:.2f}")

            print("==================================")
        elif choice == "7":
            if not expenses:
                print("No expenses to delete.")
            else:
                view_expenses(expenses)

                index = get_expense_index(expenses)
                deleted_expense = delete_expense(expenses, index)
                save_expenses(expenses)
                print(
                    f"Deleted: {deleted_expense['name']} - "
                    f"₹{deleted_expense['amount']:.2f}"
                )
        elif choice == "8":
            if not expenses:
                print("No recorded expenses yet.")
            else:
                view_expenses(expenses)

                index = get_expense_index(expenses)

                new_name = get_valid_name()
                new_amount = get_valid_amount()

                updated_expense = edit_expense(expenses, index, new_name, new_amount)
                save_expenses(expenses)
                print(
                    f"Updated: {updated_expense['name']} - "
                    f"₹{updated_expense['amount']:.2f}"
                )
        elif choice == "9":
            if not expenses:
                print("No recorded expenses yet.")
            else:
                search_term = get_valid_search_term()

                search_results = search_expenses(expenses, search_term)
                view_expenses(search_results)
        elif choice == "10":
            if not expenses:
                print("No recorded expenses yet.")
            else:
                target_date = get_valid_date()

                date_results = filter_expenses_by_date(expenses, target_date)
                view_expenses(date_results)
        elif choice == "11":
            if not expenses:
                print("No recorded expenses yet.")
            else:
                category = get_valid_category()
                target_date = get_valid_date()

                filtered_results = filter_expenses_by_category_and_date(
                    expenses, category, target_date
                )
                view_expenses(filtered_results)
        elif choice == "12":
            if not expenses:
                print("No recorded expenses yet.")
            else:
                target_year = get_valid_year()
                target_month = get_valid_month()

                filtered_results = filter_expenses_by_month(
                    expenses, target_year, target_month
                )

                month_name = datetime(target_year, target_month, 1).strftime("%B %Y")

                if not filtered_results:
                    print(f"No expenses recorded for {month_name}.\n")
                else:
                    monthly_total = calculate_total(filtered_results)
                    category_totals = calculate_category_totals(filtered_results)
                    print("========== YOUR MONTHLY EXPENSES ==========")
                    print(f"Total expenses for {month_name}: ₹{monthly_total:.2f}")

                    for category, category_total in category_totals.items():
                        print(f"{category}: ₹{category_total:.2f}")
                    view_expenses(filtered_results)

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
