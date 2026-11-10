from datetime import date, datetime
import math


# get
def get_category(amount):
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number.")

    if not math.isfinite(amount) or amount <= 0:
        raise ValueError("Amount must be a finite number greater than zero.")

    if amount < 100:
        return "Small"
    elif amount < 500:
        return "Medium"
    else:
        return "Large"


# add
def add_expense(name, money_spent):
    # Validate name
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Name cannot be empty.")

    # Validate amount
    if isinstance(money_spent, bool) or not isinstance(money_spent, (int, float)):
        raise ValueError("Amount must be a number.")

    if not math.isfinite(money_spent) or money_spent <= 0:
        raise ValueError("Amount must be a finite number greater than zero.")

    category = get_category(money_spent)

    expense = {
        "name": name.strip(),
        "amount": money_spent,
        "category": category,
        "date": date.today().strftime("%Y-%m-%d"),
    }

    return expense


# view
def view_expenses(expenses):
    if not expenses:
        print("No matching expenses found.")
    else:
        print("========== YOUR EXPENSES ==========")

        for index, expense in enumerate(expenses, start=1):
            print(
                f"{index}. {expense['name']} | "
                f"₹{expense['amount']:.2f} | "
                f"{expense['category']} Expense | "
                f"{expense.get('date', 'Unknown')}"
            )

        print("==================================")
    print("\n")


# total
def calculate_total(expenses):
    total = 0

    for expense in expenses:
        if not isinstance(expense, dict):
            raise ValueError("Invalid expense.")

        amount = expense.get("amount")

        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a number.")

        if not math.isfinite(amount) or amount <= 0:
            raise ValueError("Amount must be a finite number greater than zero.")

        total += amount

    return total


# filter


def filter_expenses(expenses, category):
    allowed_categories = {"Small", "Medium", "Large"}

    if not isinstance(category, str) or category not in allowed_categories:
        raise ValueError("Invalid category.")

    filtered_expenses = []

    for expense in expenses:
        if not isinstance(expense, dict):
            raise ValueError("Invalid expense.")

        expense_category = expense.get("category")

        if not isinstance(expense_category, str):
            raise ValueError("Invalid expense category.")

        if expense_category not in allowed_categories:
            raise ValueError("Invalid expense category.")

        if expense_category == category:
            filtered_expenses.append(expense)

    return filtered_expenses


# category total
def calculate_category_totals(expenses):
    category_totals = {"Small": 0, "Medium": 0, "Large": 0}

    for expense in expenses:
        if not isinstance(expense, dict):
            raise ValueError("Invalid expense.")

        if "category" not in expense or "amount" not in expense:
            raise ValueError("Expense is missing required fields.")

        amount = expense["amount"]
        category = expense["category"]

        # Validate the amount using the existing get_category() function.
        expected_category = get_category(amount)

        if not isinstance(category, str) or category not in category_totals:
            raise ValueError("Invalid category.")

        if category != expected_category:
            raise ValueError("Expense category does not match its amount.")

        category_totals[category] += amount

    return category_totals


# delete
def delete_expense(expenses, index):
    if isinstance(index, bool) or not isinstance(index, int):
        raise ValueError("Invalid expense index.")

    if not 0 <= index < len(expenses):
        raise ValueError("Invalid expense index.")

    return expenses.pop(index)


# edit
def edit_expense(expenses, index, new_name, new_amount):
    if isinstance(index, bool) or not isinstance(index, int):
        raise ValueError("Invalid expense index.")

    if not 0 <= index < len(expenses):
        raise ValueError("Invalid expense index.")

    if not isinstance(new_name, str) or not new_name.strip():
        raise ValueError("Name cannot be empty.")

    if isinstance(new_amount, bool) or not isinstance(new_amount, (int, float)):
        raise ValueError("Amount must be a number.")

    if not math.isfinite(new_amount) or new_amount <= 0:
        raise ValueError("Amount must be a finite number greater than zero.")

    expense = expenses[index]
    expense["name"] = new_name.strip()
    expense["amount"] = new_amount
    expense["category"] = get_category(expense["amount"])
    return expense


# search
def search_expenses(expenses, search_term):
    if not isinstance(search_term, str) or not search_term.strip():
        raise ValueError("Search term cannot be empty.")

    search_term = search_term.strip().lower()

    result = []

    for expense in expenses:
        if search_term in expense["name"].lower():
            result.append(expense)

    return result


# filter expenses by date
def filter_expenses_by_date(expenses, target_date):
    if not validate_date(target_date):
        raise ValueError("Invalid date.")

    filtered_expenses = []

    for expense in expenses:
        if expense.get("date") == target_date:
            filtered_expenses.append(expense)

    return filtered_expenses


# validate date
def validate_date(date_string):
    if not isinstance(date_string, str):
        return False

    try:
        datetime.strptime(date_string, "%Y-%m-%d").date()
        return True
    except ValueError:
        return False


# filter expenses by category and date
def filter_expenses_by_category_and_date(expenses, category, target_date):
    allowed_categories = {"Small", "Medium", "Large"}

    if not isinstance(category, str) or category not in allowed_categories:
        raise ValueError("Invalid category.")

    if not validate_date(target_date):
        raise ValueError("Invalid date.")

    filtered_expenses = []

    for expense in expenses:
        if not isinstance(expense, dict):
            raise ValueError("Invalid expense.")

        expense_category = expense.get("category")

        if not isinstance(expense_category, str):
            raise ValueError("Invalid expense category.")

        if expense_category not in allowed_categories:
            raise ValueError("Invalid expense category.")

        expense_date = expense.get("date")

        # Skip expenses without a date.
        if not expense_date:
            continue

        if not validate_date(expense_date):
            raise ValueError("Invalid expense date.")

        if expense_category == category and expense_date == target_date:
            filtered_expenses.append(expense)

    return filtered_expenses


# filter expenses by month
def filter_expenses_by_month(expenses, target_year, target_month):
    if isinstance(target_year, bool) or not isinstance(target_year, int):
        raise ValueError("Invalid year.")

    if not 1000 <= target_year <= 9999:
        raise ValueError("Year must be between 1000 and 9999.")

    if isinstance(target_month, bool) or not isinstance(target_month, int):
        raise ValueError("Invalid month.")

    if not 1 <= target_month <= 12:
        raise ValueError("Month must be between 1 and 12.")

    filtered_expenses = []

    for expense in expenses:
        expense_date = expense.get("date")

        if not expense_date:
            continue

        if not validate_date(expense_date):
            continue

        parsed_date = datetime.strptime(expense_date, "%Y-%m-%d").date()

        if parsed_date.year == target_year and parsed_date.month == target_month:
            filtered_expenses.append(expense)

    return filtered_expenses
