# Deep Learning Stimulated Task: Fashion-MNIST Clothing Classifier

This project simulates an apparel sorting system. A convolutional neural network (CNN) learns to classify 28 × 28 grayscale product images into ten clothing categories.

## Categories

T-shirt/top, Trouser, Pullover, Dress, Coat, Sandal, Shirt, Sneaker, Bag, and Ankle boot.

## Model

- Two convolution and max-pooling blocks
- Dense hidden layer with dropout
- Ten-class probability output
- 12,000 training and 2,000 testing images by default

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

```bash
source .venv/bin/activate
python train.py
```

Generated files are saved under `output/`:

- `fashion_classifier.keras` — trained CNN
- `results.json` — evaluation results
- `sample_predictions.txt` — readable clothing predictions
