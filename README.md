# Personal Expense Tracker

A command-line expense management application built with Python. It allows users to record, manage, search, filter, and analyze expenses while maintaining persistent local storage using JSON.

## Features

- **Add Expenses** – Record expenses with a name, amount, category, and date.
- **View Expenses** – Display recorded expense entries.
- **Edit Expenses** – Update existing expense details.
- **Delete Expenses** – Remove unwanted expense records.
- **Automatic Categorization** – Categorize expenses as Small, Medium, or Large based on their amount.
- **Calculate Total** – Calculate overall spending.
- **Category-wise Summary** – View spending across different expense categories.
- **Search Expenses** – Find expenses by name.
- **Filter Expenses** – Filter records by category, date, or a combination of both.
- **Monthly Summary** – Analyze monthly spending with category-wise breakdowns.
- **Persistent Storage** – Automatically save expense records to a local JSON file.
- **Data Validation** – Validate user inputs and stored expense records.
- **Automatic Backups** – Preserve the previous data in a backup file before saving changes.
- **Atomic File Saving** – Use temporary files and atomic replacement to reduce the risk of data loss during saving.
- **Automated Tests** – Test application functionality and important edge cases using Python's built-in testing framework.

## Tech Stack

| Technology              | Purpose                                              |
| ----------------------- | ---------------------------------------------------- |
| Python                  | Application logic                                    |
| JSON                    | Local data persistence                               |
| `unittest`              | Automated testing                                    |
| Python standard library | Built-in functionality without external dependencies |

## Project Structure

```text
personal-expense-tracker/
│
├── expense_manager.py
├── main.py
├── storage.py
├── expenses.json
├── .gitignore
├── README.md
│
└── tests/
    ├── test_expense_manager.py
    ├── test_main.py
    └── test_storage.py
```

## Architecture

The application follows a modular structure that separates the command-line interface, business logic, and data persistence.

| Module               | Responsibility                                                             |
| -------------------- | -------------------------------------------------------------------------- |
| `main.py`            | Command-line interface, menu navigation, and user input handling           |
| `expense_manager.py` | Expense operations, calculations, filtering, and business rules            |
| `storage.py`         | JSON loading, saving, data validation, backups, and atomic file operations |
| `tests/`             | Automated unit and integration tests                                       |

## Requirements

- Python 3.10 or later.
- No external dependencies required.

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd personal-expense-tracker
```

Run the application:

```bash
python main.py
```

Follow the interactive command-line menu to manage your expenses.

## Running Tests

Run the complete test suite:

```bash
python -m unittest discover -s tests -v
```

## Data Storage and Reliability

The application uses a local JSON file for persistent storage.

- Expense records are stored in `expenses.json`.
- Changes are automatically saved after expense operations.
- Before overwriting existing data, the application creates a backup named `expenses.json.bak`.
- The backup is overwritten on subsequent saves.
- Data is validated when loading to help detect invalid or corrupted records.
- Changes are written to a temporary file before replacing the original file using `os.replace()`.

**Note:** Expense data and backup files are stored locally. Keep personal financial information out of public repositories.

## Future Improvements

Potential enhancements include:

- Export expense reports to CSV.
- Add budget limits and spending alerts.
- Generate visual spending reports.
- Introduce a graphical user interface.
- Add recurring expense support.

## License

This project is licensed under the [MIT License](LICENSE).

You are free to use, modify, and distribute this software in accordance with the terms of the MIT License.
