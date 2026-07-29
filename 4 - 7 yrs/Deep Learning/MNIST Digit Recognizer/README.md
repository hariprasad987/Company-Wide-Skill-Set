# Deep Learning: MNIST Digit Recognizer

This project trains a basic neural network to recognize handwritten digits from a subset of the MNIST dataset.

## Neural network

- Input: 28 × 28 grayscale digit image
- Flatten layer: converts each image into 784 values
- Hidden layer: 128 neurons with ReLU activation
- Dropout: reduces overfitting
- Output layer: 10 probabilities for digits 0–9

By default, the program trains on 10,000 images, tests on 2,000 images, and runs for 3 epochs.

## Setup

Run these commands from this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Train and see the output

```bash
source .venv/bin/activate
python train.py
```

The first run downloads MNIST automatically. After training, check:

- `output/mnist_model.keras` — trained model
- `output/results.json` — accuracy and loss
- `output/sample_predictions.txt` — actual and predicted digits

For a faster demonstration:

```bash
python train.py --train-size 5000 --test-size 1000 --epochs 2
```
