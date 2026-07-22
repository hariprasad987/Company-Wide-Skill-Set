# Personal Expense Tracker — Stimulated Python Task

This command-line project records expenses in a local JSON file and provides transaction and category-summary reports.

## Add expenses

```bash
cd "4 - 7 yrs/Python - Stimulated Task/Personal Expense Tracker"

python3 expense_tracker.py add \
  --amount 42.50 \
  --category Food \
  --description "Weekly groceries" \
  --date 2026-07-20
```

## List expenses

```bash
python3 expense_tracker.py list
```

## Show category totals

```bash
python3 expense_tracker.py summary
```

Expense data is stored in `expenses.json`, which is intentionally excluded from Git. No additional dependencies are required.
