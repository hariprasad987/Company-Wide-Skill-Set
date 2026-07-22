#!/usr/bin/env python3
"""Train a multiple linear-regression model to estimate a house price."""

import argparse
import csv
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


DATA_FILE = Path(__file__).with_name("houses.csv")


def load_houses(path: Path) -> tuple[list[list[float]], list[float]]:
    """Return model features and prices loaded from the house dataset."""
    features: list[list[float]] = []
    prices: list[float] = []

    with path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            features.append(
                [
                    float(row["size_sqft"]),
                    float(row["bedrooms"]),
                    float(row["age_years"]),
                ]
            )
            prices.append(float(row["price"]))

    if len(features) < 8:
        raise ValueError("At least eight house records are required.")

    return features, prices


def positive_number(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return number


def non_negative_number(value: str) -> float:
    number = float(value)
    if number < 0:
        raise argparse.ArgumentTypeError("value cannot be negative")
    return number


def main() -> None:
    parser = argparse.ArgumentParser(description="Estimate a house sale price.")
    parser.add_argument("--size", type=positive_number, default=1750, help="square feet")
    parser.add_argument("--bedrooms", type=positive_number, default=3, help="bedrooms")
    parser.add_argument("--age", type=non_negative_number, default=6, help="age in years")
    args = parser.parse_args()

    features, prices = load_houses(DATA_FILE)
    train_x, test_x, train_y, test_y = train_test_split(
        features, prices, test_size=0.27, random_state=42
    )

    model = LinearRegression()
    model.fit(train_x, train_y)
    test_predictions = model.predict(test_x)
    estimated_price = model.predict([[args.size, args.bedrooms, args.age]])[0]

    print("Simulated House Price Estimator")
    print(f"Dataset records     : {len(features)}")
    print(f"Training records    : {len(train_x)}")
    print(f"Testing records     : {len(test_x)}")
    print(f"Test R-squared      : {r2_score(test_y, test_predictions):.4f}")
    print(f"Test mean abs. error: ${mean_absolute_error(test_y, test_predictions):,.2f}")
    print()
    print("House details")
    print(f"  Size              : {args.size:,.0f} sq ft")
    print(f"  Bedrooms          : {args.bedrooms:g}")
    print(f"  Property age      : {args.age:g} years")
    print(f"Estimated price     : ${estimated_price:,.2f}")


if __name__ == "__main__":
    main()
