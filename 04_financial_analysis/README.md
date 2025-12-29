# 💰 Retail Financial Analysis

Professional financial modeling and statement analysis for retail and inventory-heavy businesses.

## 📈 Overview

This project simulates the financial engine of a retail business. It integrates sales transactions and inventory levels to generate professional **Financial Statements** and calculate **Retail Ratios** that drive investment and operational decisions.

## 🎯 Business Value

Financial visibility is the difference between a "hobby" and a "business". This project demonstrates:
- **Profitability Analysis**: Tracking Gross and Net margins to ensure sustainable pricing.
- **Working Capital Management**: Managing the trade-off between cash-on-hand and stock-on-shelf.
- **Investment Evaluation**: Using GMROI to identify which categories are actually making money.
- **Executive Reporting**: Generating "Board-Ready" Excel statements automatically.

---

## 🚀 Professional Financial Framework

### 📝 1. Income Statement (P&L)
A summary of revenue and expenses over a period.
- **Revenue**: Total sales from `01_sales_analytics`.
- **COGS (Cost of Goods Sold)**: Direct cost of products sold.
- **Gross Profit**: Revenue minus COGS.
- **Operating Expenses (OpEx)**: Simulated marketing, payroll, and rent.
- **Net Income**: The "Bottom Line" profit.

### 🏛️ 2. Balance Sheet (Current Assets focus)
A snapshot of what the business owns (Assets).
- **Cash**: Simulated based on cumulative profits.
- **Inventory Value**: Real-time valuation from `06_inventory_analysis`.
- **Accounts Receivable**: Estimated based on average payment terms.

---

## 🔢 Key Retail Financial Ratios

### 💎 GMROI (Gross Margin Return on Investment)
**Formula**: `Gross Profit / Average Inventory Cost`
**Why it matters**: Tells you how many dollars you get back for every dollar invested in stock. A GMROI of 2.5 means for every $1 of stock, you get $2.50 in gross profit.

### 🔄 Inventory Turnover
**Formula**: `COGS / Average Inventory`
**Why it matters**: Measures how many times a company has sold and replaced inventory during a specific period. High turnover indicates strong sales.

### 💵 Current Ratio
**Formula**: `Current Assets / Current Liabilities`
**Why it matters**: A liquidity ratio that measures a company's ability to pay short-term obligations. A ratio of 2.0 is generally healthy.

---

## 📁 Project Structure

```
04_financial_analysis/
├── README.md
├── scripts/
│   ├── retail_financial_engine.py  # 🔢 The core logic & Excel generator
│   └── financials.py              # Legacy budget scripts
├── notebooks/
│   └── retail_finance_dashboard.ipynb # 📊 Financial Visualization
└── outputs/
    ├── retail_financial_report.xlsx # 📗 Formatted Excel Report
    └── financial_metrics.csv
```

## 🚀 Quick Start

```bash
# Ensure sales and inventory data exist
python shared/generate_all_data.py
python 06_inventory_analysis/scripts/generate_inventory_data.py

# Run the financial engine
python 04_financial_analysis/scripts/retail_financial_engine.py
```

## 📗 Formatted Executive Export
The `retail_financial_engine.py` script generates a professional Excel report with:
- **Bold Headers**
- **Currency Formatting ($)**
- **Conditional Formatting** (Red for negative margins)
- **Ratio Summary Sheet**

---

*All data is synthetic/dummy data for demonstration purposes.*
