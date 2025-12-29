# Shared Utilities

This folder contains shared code and utilities used across all projects.

## Files

- `generate_all_data.py` - Master script to generate all dummy datasets
- `data/` - Generated dummy data files

## Usage

```bash
# Generate all dummy data
python generate_all_data.py
```

## Data Generated

| Dataset | Records | Description |
|---------|---------|-------------|
| `sales_transactions.csv` | 10,000 | Sales transaction data |
| `customers.csv` | 2,000 | Customer demographics |
| `telecom_kpis.csv` | 5,000 | Network performance KPIs |
| `sales_with_issues.csv` | ~10,500 | Data with quality issues for testing |

*All data is 100% synthetic/dummy data.*
