#!/usr/bin/env python3
"""Calculate a student's letter grade from marks entered in the terminal."""


def calculate_grade(marks: float) -> str:
    """Return the letter grade for marks in the inclusive range 0–100."""
    if not 0 <= marks <= 100:
        raise ValueError("Marks must be between 0 and 100.")

    if marks >= 90:
        return "A"
    if marks >= 80:
        return "B"
    if marks >= 70:
        return "C"
    if marks >= 60:
        return "D"
    return "F"


def main() -> None:
    print("Student Grade Calculator")

    try:
        marks = float(input("Enter marks (0-100): "))
        grade = calculate_grade(marks)
    except ValueError as error:
        print(f"Error: {error}")
        raise SystemExit(1) from error

    print(f"Marks: {marks:.2f} / 100")
    print(f"Grade: {grade}")


if __name__ == "__main__":
    main()
