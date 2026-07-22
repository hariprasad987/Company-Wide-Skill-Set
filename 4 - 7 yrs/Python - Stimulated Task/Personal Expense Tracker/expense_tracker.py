#!/usr/bin/env python3
"""A small JSON-backed command-line personal expense tracker."""

import argparse
import json
from collections import defaultdict
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


DEFAULT_DATA_FILE = Path(__file__).with_name("expenses.json")


def valid_amount(value: str) -> Decimal:
    try:
        amount = Decimal(value).quantize(Decimal("0.01"))
    except InvalidOperation as error:
        raise argparse.ArgumentTypeError("amount must be a number") from error
    if amount <= 0:
        raise argparse.ArgumentTypeError("amount must be greater than zero")
    return amount


def valid_date(value: str) -> str:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError as error:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD format") from error


def load_expenses(path: Path) -> list[dict[str, str | int]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError("expense data must be a JSON list")
    return data


def save_expenses(path: Path, expenses: list[dict[str, str | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=2)
        file.write("\n")


def add_expense(args: argparse.Namespace, expenses: list[dict[str, str | int]]) -> None:
    next_id = max((int(item["id"]) for item in expenses), default=0) + 1
    expense = {
        "id": next_id,
        "date": args.date,
        "category": args.category.strip().title(),
        "description": args.description.strip(),
        "amount": str(args.amount),
    }
    expenses.append(expense)
    save_expenses(args.data_file, expenses)
    print(f"Added expense #{next_id}: ${args.amount:,.2f} for {expense['category']}")


def list_expenses(expenses: list[dict[str, str | int]]) -> None:
    if not expenses:
        print("No expenses recorded.")
        return

    print("ID  Date        Category       Amount      Description")
    print("--  ----------  -------------  ----------  ------------------------------")
    for item in sorted(expenses, key=lambda expense: (str(expense["date"]), int(expense["id"]))):
        print(
            f"{int(item['id']):<3} "
            f"{str(item['date']):<11} "
            f"{str(item['category']):<14} "
            f"${Decimal(str(item['amount'])):>8,.2f}  "
            f"{item['description']}"
        )


def show_summary(expenses: list[dict[str, str | int]]) -> None:
    if not expenses:
        print("No expenses recorded.")
        return

    totals: defaultdict[str, Decimal] = defaultdict(Decimal)
    for item in expenses:
        totals[str(item["category"])] += Decimal(str(item["amount"]))

    print("Expense Summary")
    print("---------------")
    for category, amount in sorted(totals.items(), key=lambda item: (-item[1], item[0])):
        print(f"{category:<15} ${amount:>9,.2f}")
    print("---------------")
    print(f"{'Total':<15} ${sum(totals.values()):>9,.2f}")
    print(f"Transactions    {len(expenses):>10}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track personal expenses from the terminal.")
    parser.add_argument(
        "--data-file",
        type=Path,
        default=DEFAULT_DATA_FILE,
        help="JSON storage path (default: expenses.json beside the script)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="record a new expense")
    add_parser.add_argument("--amount", required=True, type=valid_amount)
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--date", type=valid_date, default=date.today().isoformat())

    subparsers.add_parser("list", help="display every expense")
    subparsers.add_parser("summary", help="display totals by category")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        expenses = load_expenses(args.data_file)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(f"cannot read expense data: {error}")

    if args.command == "add":
        add_expense(args, expenses)
    elif args.command == "list":
        list_expenses(expenses)
    elif args.command == "summary":
        show_summary(expenses)


if __name__ == "__main__":
    main()
