# Linear Regression Prediction

This project trains a simple linear-regression model that predicts salary from years of experience.

## Setup

```bash
cd "4 - 7 yrs/Machine Learning/Linear Regression"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

Use the default input of 6.5 years:

```bash
python main.py
```

Or supply another value:

```bash
python main.py 8.5
```

The program displays the fitted model parameters, evaluation metrics, and predicted salary.

## Deactivate the environment

```bash
deactivate
```
