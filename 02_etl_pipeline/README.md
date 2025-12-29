# 🔄 ETL Pipeline Demo

A production-style ETL pipeline demonstrating the **Bronze → Silver → Gold** medallion architecture with integrated data quality checks.

## 🏗️ Architecture

```
Raw Data → [Bronze Layer] → [Silver Layer] → [Gold Layer] → Analytics
                ↓               ↓               ↓
           Raw Ingestion    Cleansing       Aggregations
           + Metadata       + Validation    + KPIs
```

## ✨ Features

- **Bronze Layer**: Raw data ingestion with metadata
- **Silver Layer**: Data cleansing and standardization
- **Gold Layer**: Business-level aggregations
- **Data Quality Web App**: Interactive validation dashboard
- **Incremental Processing**: Watermark-based loading

## 📁 Structure

```
02_etl_pipeline/
├── README.md
├── config/
│   └── pipeline_config.yaml
├── src/
│   ├── bronze_layer.py
│   ├── silver_layer.py
│   └── gold_layer.py
├── data_quality_app/       # Web App for Data Checks
│   ├── app.py              # Flask web application
│   ├── templates/
│   │   └── dashboard.html
│   └── static/
│       └── style.css
└── tests/
    └── test_transformations.py
```

## 🚀 Quick Start

```bash
# Run the full pipeline
python src/bronze_layer.py
python src/silver_layer.py
python src/gold_layer.py

# Launch Data Quality Web App
cd data_quality_app
python app.py
# Open http://localhost:5000 in browser
```

## 🌐 Data Quality Web App

The integrated web app provides:
- Real-time data validation
- Quality score dashboards
- Issue detection and reporting
- Data profiling statistics

*All data is simulated data for analytical demonstration.*
