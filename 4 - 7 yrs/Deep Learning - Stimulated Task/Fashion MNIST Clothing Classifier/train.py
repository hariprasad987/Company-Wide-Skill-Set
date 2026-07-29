"""Train a CNN to classify clothing images from a Fashion-MNIST subset."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import keras
import numpy as np


CLASSES = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]
PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "output"


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-size", type=int, default=12_000)
    parser.add_argument("--test-size", type=int, default=2_000)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=128)
    return parser.parse_args()


def create_model() -> keras.Model:
    model = keras.Sequential(
        [
            keras.layers.Input(shape=(28, 28, 1)),
            keras.layers.Conv2D(16, 3, activation="relu"),
            keras.layers.MaxPooling2D(),
            keras.layers.Conv2D(32, 3, activation="relu"),
            keras.layers.MaxPooling2D(),
            keras.layers.Flatten(),
            keras.layers.Dense(64, activation="relu"),
            keras.layers.Dropout(0.25),
            keras.layers.Dense(10, activation="softmax"),
        ],
        name="fashion_mnist_cnn",
    )
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main() -> None:
    args = arguments()
    keras.utils.set_random_seed(42)
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Loading Fashion-MNIST clothing images...")
    (x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()
    train_size = min(args.train_size, len(x_train))
    test_size = min(args.test_size, len(x_test))
    x_train = np.expand_dims(x_train[:train_size].astype("float32") / 255.0, -1)
    y_train = y_train[:train_size]
    x_test = np.expand_dims(x_test[:test_size].astype("float32") / 255.0, -1)
    y_test = y_test[:test_size]

    print(f"Training images: {train_size:,}")
    print(f"Testing images:  {test_size:,}")
    print(f"Categories:      {len(CLASSES)}")

    model = create_model()
    model.summary()
    print("\nTraining convolutional neural network...")
    history = model.fit(
        x_train,
        y_train,
        epochs=args.epochs,
        batch_size=args.batch_size,
        validation_split=0.1,
        verbose=2,
    )

    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    probabilities = model.predict(x_test[:12], verbose=0)
    predictions = np.argmax(probabilities, axis=1)
    confidence = np.max(probabilities, axis=1)

    model_path = OUTPUT_DIR / "fashion_classifier.keras"
    results_path = OUTPUT_DIR / "results.json"
    predictions_path = OUTPUT_DIR / "sample_predictions.txt"
    model.save(model_path)

    results = {
        "train_images": train_size,
        "test_images": test_size,
        "epochs": args.epochs,
        "categories": CLASSES,
        "test_loss": round(float(test_loss), 4),
        "test_accuracy_percent": round(float(test_accuracy) * 100, 2),
        "training_accuracy_percent": round(float(history.history["accuracy"][-1]) * 100, 2),
        "validation_accuracy_percent": round(
            float(history.history["val_accuracy"][-1]) * 100, 2
        ),
    }
    results_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    lines = ["Fashion-MNIST sample predictions", "=" * 32]
    print("\nSample clothing predictions:")
    for index, (actual, predicted, score) in enumerate(
        zip(y_test[:12], predictions, confidence, strict=True), 1
    ):
        actual_name = CLASSES[int(actual)]
        predicted_name = CLASSES[int(predicted)]
        status = "correct" if int(actual) == int(predicted) else "incorrect"
        line = (
            f"Image {index:02d}: actual={actual_name:<12} "
            f"predicted={predicted_name:<12} confidence={score * 100:5.1f}% [{status}]"
        )
        lines.append(line)
        print(line)
    predictions_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\nEvaluation complete")
    print(f"Test loss:     {test_loss:.4f}")
    print(f"Test accuracy: {test_accuracy * 100:.2f}%")
    print(f"Model saved:   {model_path.relative_to(PROJECT_DIR)}")
    print(f"Results saved: {results_path.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
