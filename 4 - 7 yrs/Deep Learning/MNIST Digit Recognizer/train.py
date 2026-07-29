"""Train a small neural network on a subset of the MNIST digit dataset."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import keras
import numpy as np


PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "output"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-size", type=int, default=10_000)
    parser.add_argument("--test-size", type=int, default=2_000)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=128)
    return parser.parse_args()


def build_model() -> keras.Model:
    """Create a basic fully connected neural network."""
    model = keras.Sequential(
        [
            keras.layers.Input(shape=(28, 28)),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(10, activation="softmax"),
        ],
        name="mnist_digit_recognizer",
    )
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main() -> None:
    args = parse_args()
    keras.utils.set_random_seed(42)
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Loading MNIST dataset...")
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    train_size = min(args.train_size, len(x_train))
    test_size = min(args.test_size, len(x_test))
    x_train = x_train[:train_size].astype("float32") / 255.0
    y_train = y_train[:train_size]
    x_test = x_test[:test_size].astype("float32") / 255.0
    y_test = y_test[:test_size]

    print(f"Training samples: {train_size:,}")
    print(f"Testing samples:  {test_size:,}")
    print("Image shape:      28 x 28 pixels")

    model = build_model()
    model.summary()
    print("\nTraining neural network...")
    history = model.fit(
        x_train,
        y_train,
        epochs=args.epochs,
        batch_size=args.batch_size,
        validation_split=0.1,
        verbose=2,
    )

    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    probabilities = model.predict(x_test[:10], verbose=0)
    predictions = np.argmax(probabilities, axis=1)

    model_path = OUTPUT_DIR / "mnist_model.keras"
    results_path = OUTPUT_DIR / "results.json"
    predictions_path = OUTPUT_DIR / "sample_predictions.txt"
    model.save(model_path)

    results = {
        "train_samples": train_size,
        "test_samples": test_size,
        "epochs": args.epochs,
        "test_loss": round(float(test_loss), 4),
        "test_accuracy": round(float(test_accuracy), 4),
        "test_accuracy_percent": round(float(test_accuracy) * 100, 2),
        "final_training_accuracy": round(float(history.history["accuracy"][-1]), 4),
        "final_validation_accuracy": round(float(history.history["val_accuracy"][-1]), 4),
    }
    results_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    prediction_lines = ["Sample MNIST predictions", "=" * 24]
    for index, (actual, predicted) in enumerate(zip(y_test[:10], predictions, strict=True), 1):
        status = "correct" if int(actual) == int(predicted) else "incorrect"
        prediction_lines.append(
            f"Image {index:02d}: actual={int(actual)} predicted={int(predicted)} [{status}]"
        )
    predictions_path.write_text("\n".join(prediction_lines) + "\n", encoding="utf-8")

    print("\nEvaluation complete")
    print(f"Test loss:     {test_loss:.4f}")
    print(f"Test accuracy: {test_accuracy * 100:.2f}%")
    print("\nFirst 10 predictions:")
    for actual, predicted in zip(y_test[:10], predictions, strict=True):
        print(f"Actual: {int(actual)}  Predicted: {int(predicted)}")
    print(f"\nModel saved to:   {model_path.relative_to(PROJECT_DIR)}")
    print(f"Results saved to: {results_path.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
