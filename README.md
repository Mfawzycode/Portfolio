# 🚀 Data Portfolio - Analytics & Engineering Projects

Hi! I'm a **Data Analyst & Data Engineer** passionate about building robust data pipelines and extracting actionable insights from data.

## 📊 Projects

| Project | Description | Technologies |
|---------|-------------|--------------|
| [Sales Analytics](./01_sales_analytics/) | Business intelligence dashboard with KPI analysis | Python, Pandas, Plotly |
| [ETL Pipeline](./02_etl_pipeline/) | Bronze → Silver → Gold architecture with Web App | PySpark, Flask, Parquet |
| [Data Quality Framework](./03_data_quality/) | Automated validation with quality scoring | Python, Great Expectations |
| [Financial Analysis](./04_financial_analysis/) | Budget vs actual, cash flow, financial KPIs | Python, Pandas, Power BI |
| [Healthcare Analytics](./05_healthcare_analysis/) | Patient visits, wait times, clinical KPIs | Python, Pandas, Power BI |
| [Inventory Analysis](./06_inventory_analysis/) | Stock optimization, turnover KPIs, ABC classification | Python, Pandas, Power BI |
| [Customer Analysis](./07_customer_analysis/) | RFM Segmentation, Cohort Analysis, Sentiment Analysis | Python, Pandas, Plotly |
| [Predictive Analytics](./08_predictive_analytics/) | Demand Forecasting (TS) & Customer Churn Modeling (ML) | Python, MLPC, Plotly |

## 🛠️ Skills Demonstrated

- **Data Engineering**: ETL pipelines, schema evolution, incremental loading
- **Data Analysis**: Statistical analysis, KPI tracking, trend analysis
- **Visualization**: Interactive dashboards, Power BI reports
- **Data Quality**: Validation frameworks, automated testing, monitoring
- **Web Development**: Flask dashboards for data monitoring
- **Technologies**: Python, PySpark, SQL, DuckDB, Pandas, Flask

## 📁 Repository Structure

```
├── 01_sales_analytics/     # Sales data analysis & visualization
├── 02_etl_pipeline/        # Production-style ETL with data quality web app
├── 03_data_quality/        # Data validation framework
├── 04_financial_analysis/  # Budget and financial KPI analysis
├── 05_healthcare_analysis/ # Patient visit analytics
├── 06_inventory_analysis/  # Inventory KPIs and stock optimization
├── 07_customer_analysis/   # Advanced behavioral & retention analytics
├── 08_predictive_analytics/# Time-series forecasting & churn modeling
├── powerbi_exports/        # Ready-to-use Power BI data files
└── shared/                 # Common utilities and data generators
```

## 🚦 Quick Start

```bash
# Clone the repository
git clone https://github.com/Mfawzycode/Portfolio.git
cd Portfolio

# Install dependencies
pip install -r requirements.txt

# Generate all dummy data
python shared/generate_all_data.py
python 04_financial_analysis/scripts/generate_financial_data.py
python 05_healthcare_analysis/scripts/generate_healthcare_data.py
python 06_inventory_analysis/scripts/generate_inventory_data.py
python 07_customer_analysis/scripts/generate_customer_analysis_data.py
python 08_predictive_analytics/scripts/generate_predictive_data.py

# Run ETL Pipeline
python 02_etl_pipeline/src/bronze_layer.py
python 02_etl_pipeline/src/silver_layer.py
python 02_etl_pipeline/src/gold_layer.py

# Launch Data Quality Web App
cd 02_etl_pipeline/data_quality_app
python app.py
# Open http://localhost:5000 in browser
```

## 📈 Power BI Reports

Pre-generated data exports are available in `/powerbi_exports/` folder:
- `sales_data.csv` - Sales transactions
- `financial_transactions.csv` - Financial data
- `healthcare_visits.csv` - Patient visit data
- `telecom_kpi_data.csv` - Network performance KPIs
- `inventory_data.csv` - Inventory stock and KPIs
- `customer_segments.csv` - RFM Customer segmentation
- `cohort_matrix.csv` - Monthly retention rates
- `retail_financial_report.xlsx` - Formatted financial statements and ratios

Import these directly into Power BI Desktop to create dashboards.

## 📧 Contact

- **GitHub**: [@Mfawzycode](https://github.com/Mfawzycode)

---
*All data in this repository is synthetic/dummy data generated for demonstration purposes only.*
