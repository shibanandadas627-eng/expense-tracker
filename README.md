# Expense Tracker (Python Mini Project)

A command-line app to record and analyse daily expenses. Built with plain Python (no external libraries).

## Features
- Add expenses with amount, category, description and date (input validated)
- View all expenses in a table with total
- Delete an expense by ID
- Summary by category with percentages
- Monthly total
- Search by keyword
- Export to CSV
- Data saved automatically in `expenses.json`

## Concepts used
Variables, loops, functions, lists, dictionaries, file handling (JSON and CSV), exception handling, `datetime`, and unit testing with `unittest`.

## Run
```bash
python expense_tracker.py
```

## Run tests
```bash
python -m unittest discover tests
```

## Project structure
```
expense-tracker/
├── expense_tracker.py
├── tests/test_expense_tracker.py
├── README.md
└── .gitignore
```

## Sample
```
===== EXPENSE TRACKER =====
1. Add expense
2. View all expenses
...
```
