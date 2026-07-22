#!/usr/bin/env python3
"""Train a linear-regression model and predict salary from experience."""

import argparse
import csv
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


DATA_FILE = Path(__file__).with_name("data.csv")


def load_dataset(path: Path) -> tuple[list[list[float]], list[float]]:
    """Load experience and salary values from a CSV file."""
    features: list[list[float]] = []
    targets: list[float] = []

    with path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            features.append([float(row["years_experience"])])
            targets.append(float(row["salary"]))

    if len(features) < 2:
        raise ValueError("The dataset must contain at least two rows.")

    return features, targets


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Predict salary using years of experience."
    )
    parser.add_argument(
        "years",
        nargs="?",
        type=float,
        default=6.5,
        help="years of experience to predict for (default: 6.5)",
    )
    args = parser.parse_args()

    if args.years < 0:
        parser.error("years of experience cannot be negative")

    features, targets = load_dataset(DATA_FILE)
    model = LinearRegression()
    model.fit(features, targets)

    fitted_values = model.predict(features)
    prediction = model.predict([[args.years]])[0]

    print("Linear Regression Model")
    print(f"Dataset rows       : {len(features)}")
    print(f"Slope              : {model.coef_[0]:,.2f}")
    print(f"Intercept          : {model.intercept_:,.2f}")
    print(f"R-squared score    : {r2_score(targets, fitted_values):.4f}")
    print(f"Mean absolute error: ${mean_absolute_error(targets, fitted_values):,.2f}")
    print()
    print(f"Experience entered : {args.years:g} years")
    print(f"Predicted salary   : ${prediction:,.2f}")


if __name__ == "__main__":
    main()
