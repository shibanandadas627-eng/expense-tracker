"""Expense Tracker - a command-line Python mini project.

Features: add, list, delete, summary by category, monthly total,
search, export to CSV. Data is saved in expenses.json.
"""
import csv
import json
import os
from datetime import date, datetime

DATA_FILE = os.environ.get("EXPENSE_FILE", "expenses.json")
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Education", "Entertainment", "Other"]


# ---------- storage ----------
def load_expenses(path=None):
    path = path or DATA_FILE
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read data file, starting fresh.")
        return []


def save_expenses(expenses, path=None):
    path = path or DATA_FILE
    with open(path, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)


# ---------- core logic (easy to test) ----------
def add_expense(expenses, amount, category, description="", when=None):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    when = when or date.today().isoformat()
    datetime.strptime(when, "%Y-%m-%d")  # raises ValueError if bad format
    next_id = max((e["id"] for e in expenses), default=0) + 1
    expense = {"id": next_id, "date": when, "amount": round(float(amount), 2),
               "category": category, "description": description}
    expenses.append(expense)
    return expense


def delete_expense(expenses, expense_id):
    for e in expenses:
        if e["id"] == expense_id:
            expenses.remove(e)
            return True
    return False


def total_by_category(expenses):
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))


def monthly_total(expenses, year, month):
    prefix = f"{year:04d}-{month:02d}"
    return round(sum(e["amount"] for e in expenses if e["date"].startswith(prefix)), 2)


def search(expenses, keyword):
    k = keyword.lower()
    return [e for e in expenses if k in e["description"].lower() or k in e["category"].lower()]


def export_csv(expenses, path="expenses_export.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "date", "amount", "category", "description"])
        writer.writeheader()
        writer.writerows(expenses)
    return path


# ---------- display / input helpers ----------
def print_table(expenses):
    if not expenses:
        print("No expenses to show.")
        return
    print(f"{'ID':<4}{'Date':<12}{'Amount':>10}  {'Category':<14}Description")
    print("-" * 60)
    for e in sorted(expenses, key=lambda x: x["date"]):
        print(f"{e['id']:<4}{e['date']:<12}{e['amount']:>10.2f}  {e['category']:<14}{e['description']}")
    print("-" * 60)
    print(f"{'Total':<16}{sum(e['amount'] for e in expenses):>10.2f}")


def ask_amount():
    while True:
        try:
            value = float(input("Amount (Rs.): "))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a number greater than 0.")


def ask_category():
    for i, c in enumerate(CATEGORIES, 1):
        print(f"  {i}. {c}")
    while True:
        choice = input("Choose category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("Invalid choice.")


def ask_date():
    while True:
        raw = input("Date YYYY-MM-DD (Enter for today): ").strip()
        if not raw:
            return date.today().isoformat()
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("Use the format YYYY-MM-DD.")


MENU = """
===== EXPENSE TRACKER =====
1. Add expense
2. View all expenses
3. Delete expense
4. Summary by category
5. Monthly total
6. Search
7. Export to CSV
0. Exit
"""


def main():
    expenses = load_expenses()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "1":
            amount = ask_amount()
            category = ask_category()
            desc = input("Description: ").strip()
            when = ask_date()
            add_expense(expenses, amount, category, desc, when)
            save_expenses(expenses)
            print("Expense added.")
        elif choice == "2":
            print_table(expenses)
        elif choice == "3":
            print_table(expenses)
            raw = input("ID to delete: ").strip()
            if raw.isdigit() and delete_expense(expenses, int(raw)):
                save_expenses(expenses)
                print("Deleted.")
            else:
                print("ID not found.")
        elif choice == "4":
            totals = total_by_category(expenses)
            grand = sum(totals.values()) or 1
            for cat, amt in totals.items():
                print(f"{cat:<14}{amt:>10.2f}  ({amt / grand * 100:.1f}%)")
            if not totals:
                print("No data yet.")
        elif choice == "5":
            raw = input("Month as YYYY-MM (Enter for current): ").strip()
            try:
                y, m = (int(x) for x in raw.split("-")) if raw else (date.today().year, date.today().month)
                print(f"Total for {y:04d}-{m:02d}: Rs. {monthly_total(expenses, y, m):.2f}")
            except ValueError:
                print("Use the format YYYY-MM.")
        elif choice == "6":
            print_table(search(expenses, input("Keyword: ")))
        elif choice == "7":
            print("Exported to", export_csv(expenses))
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
