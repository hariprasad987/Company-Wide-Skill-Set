#!/usr/bin/env python3
"""Calculate the mean, median, and mode of a set of numbers."""

import argparse
from statistics import mean, median, multimode


DEFAULT_NUMBERS = [4, 7, 7, 9, 10, 12, 7]


def format_number(value: float) -> str:
    """Display whole numbers without an unnecessary decimal suffix."""
    return f"{value:g}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate mean, median, and mode for a set of numbers."
    )
    parser.add_argument(
        "numbers",
        nargs="*",
        type=float,
        help="numbers to analyze; a sample dataset is used when omitted",
    )
    args = parser.parse_args()

    numbers = args.numbers or DEFAULT_NUMBERS
    modes = multimode(numbers)

    print("Statistics Calculator")
    print(f"Numbers : {', '.join(format_number(number) for number in numbers)}")
    print(f"Count   : {len(numbers)}")
    print(f"Mean    : {format_number(mean(numbers))}")
    print(f"Median  : {format_number(median(numbers))}")

    if len(modes) == 1:
        print(f"Mode    : {format_number(modes[0])}")
    elif len(modes) == len(numbers):
        print("Mode    : No mode (all values occur once)")
    else:
        print(f"Modes   : {', '.join(format_number(mode) for mode in modes)}")


if __name__ == "__main__":
    main()
