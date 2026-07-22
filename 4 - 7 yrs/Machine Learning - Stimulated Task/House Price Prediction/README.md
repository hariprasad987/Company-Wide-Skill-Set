# House Price Prediction — Stimulated Machine Learning Task

This simulated real-estate project uses multiple linear regression to estimate a house price from:

- Size in square feet
- Number of bedrooms
- Property age

The script reserves part of the dataset for testing and reports R-squared and mean absolute error before making a prediction.

## Setup

```bash
cd "4 - 7 yrs/Machine Learning - Stimulated Task/House Price Prediction"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

Default house: 1,750 sq ft, 3 bedrooms, 6 years old.

```bash
python predict.py
```

Supply custom house details:

```bash
python predict.py --size 2100 --bedrooms 4 --age 5
```

When finished:

```bash
deactivate
```
