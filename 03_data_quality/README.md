# 🔍 Data Quality Framework

A reusable data validation framework demonstrating best practices in data quality management.

## 📊 Overview

This framework provides automated data quality checks, validation rules, and reporting capabilities for ensuring data integrity across pipelines.

## 🎯 Key Features

- **Completeness Checks**: Null value detection and thresholds
- **Uniqueness Validation**: Duplicate detection and primary key validation
- **Range Validation**: KPI boundary checks for numeric fields
- **Format Validation**: Date formats, email patterns, phone numbers
- **Referential Integrity**: Cross-table relationship validation
- **Quality Scoring**: Automated quality score calculation

## 📁 Structure

```
03_data_quality/
├── README.md
├── src/
│   ├── quality_checks.py       # Core validation functions
│   ├── report_generator.py     # Quality report generation
│   └── validators.py           # Field-level validators
├── config/
│   └── quality_rules.yaml      # Configurable quality rules
├── tests/
│   └── test_quality_checks.py  # Unit tests
└── outputs/
    └── quality_reports/
```

## 🚀 Quick Start

```bash
# Run quality checks on sample data
python src/quality_checks.py

# Generate quality report
python src/report_generator.py
```

## 📋 Sample Quality Rules

```yaml
completeness:
  threshold: 0.95
  critical_columns: [id, date, amount]
  
uniqueness:
  primary_keys: [transaction_id]
  
range_checks:
  amount: {min: 0, max: 1000000}
  percentage: {min: 0, max: 100}
```

*All data is synthetic/dummy data for demonstration purposes.*
