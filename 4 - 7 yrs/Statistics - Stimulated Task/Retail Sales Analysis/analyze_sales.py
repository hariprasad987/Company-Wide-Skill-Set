#!/usr/bin/env python3
"""Analyze order and revenue statistics from a retail sales CSV file."""

import csv
from pathlib import Path
from statistics import mean, median, multimode, pstdev


DATA_FILE = Path(__file__).with_name("daily_sales.csv")


def load_sales(path: Path) -> list[dict[str, str | int | float]]:
    records: list[dict[str, str | int | float]] = []
    with path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            records.append(
                {
                    "date": row["date"],
                    "orders": int(row["orders"]),
                    "revenue": float(row["revenue"]),
                }
            )
    if not records:
        raise ValueError("The sales dataset is empty.")
    return records


def mode_text(values: list[int]) -> str:
    modes = multimode(values)
    if len(modes) == len(values):
        return "No mode"
    return ", ".join(str(value) for value in modes)


def main() -> None:
    sales = load_sales(DATA_FILE)
    orders = [int(record["orders"]) for record in sales]
    revenues = [float(record["revenue"]) for record in sales]
    best_day = max(sales, key=lambda record: float(record["revenue"]))
    weakest_day = min(sales, key=lambda record: float(record["revenue"]))

    print("Retail Sales Statistical Report")
    print("================================")
    print(f"Days analyzed          : {len(sales)}")
    print(f"Total orders           : {sum(orders)}")
    print(f"Total revenue          : ${sum(revenues):,.2f}")
    print()
    print("Order Statistics")
    print("----------------")
    print(f"Mean orders/day        : {mean(orders):.2f}")
    print(f"Median orders/day      : {median(orders):.2f}")
    print(f"Mode orders/day        : {mode_text(orders)}")
    print(f"Order range            : {max(orders) - min(orders)}")
    print(f"Population std. dev.   : {pstdev(orders):.2f}")
    print()
    print("Revenue Statistics")
    print("------------------")
    print(f"Mean revenue/day       : ${mean(revenues):,.2f}")
    print(f"Median revenue/day     : ${median(revenues):,.2f}")
    print(f"Population std. dev.   : ${pstdev(revenues):,.2f}")
    print(f"Best sales day         : {best_day['date']} (${float(best_day['revenue']):,.2f})")
    print(f"Weakest sales day      : {weakest_day['date']} (${float(weakest_day['revenue']):,.2f})")


if __name__ == "__main__":
    main()
