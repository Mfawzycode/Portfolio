# 📦 Inventory Analysis Project

A comprehensive inventory management analytics project demonstrating supply chain optimization, stock management, and inventory performance KPIs.

## 📊 Overview

This project analyzes synthetic inventory data to demonstrate how data analytics drives smarter inventory decisions, reduces costs, and improves operational efficiency. Inventory management is critical for businesses as it directly impacts **cash flow**, **customer satisfaction**, and **operational costs**.

## 🎯 Business Value

Poor inventory management can cost businesses **20-30% of their inventory value annually** through:
- Stockouts leading to lost sales
- Overstocking tying up capital
- Obsolete inventory write-offs
- Emergency ordering at premium prices

This analysis helps businesses **optimize stock levels**, **reduce carrying costs**, and **improve service levels**.

---

## 📈 Key Performance Indicators (KPIs)

### 🔄 Inventory Turnover Ratio

**Formula**: `Cost of Goods Sold (COGS) / Average Inventory Value`

**What it measures**: How many times inventory is sold and replaced over a period.

**Why it matters for business**:
- **High turnover (8-12)**: Indicates strong sales and efficient inventory management
- **Low turnover (<4)**: Suggests overstocking, obsolete items, or weak demand
- **Industry benchmark**: Varies by industry (grocery: 15-20, fashion: 4-6, manufacturing: 5-8)

**Actionable insights**:
- Identify slow-moving items for markdown or discontinuation
- Optimize reorder quantities for fast-moving products
- Reduce carrying costs by improving turnover

---

### 📊 Days Sales of Inventory (DSI)

**Formula**: `(Average Inventory / COGS) × 365 days`

**What it measures**: Average number of days to sell the entire inventory.

**Why it matters for business**:
- **Lower DSI**: Money is tied up for less time, improving cash flow
- **Higher DSI**: Capital locked in inventory, potential obsolescence risk
- **Target**: 30-60 days for most retail businesses

**Actionable insights**:
- Forecast seasonal demand variations
- Negotiate better payment terms with suppliers
- Plan clearance sales for aging inventory

---

### 📉 Stockout Rate

**Formula**: `(Number of Stockout Events / Total Product Requests) × 100`

**What it measures**: Percentage of times an item was unavailable when requested.

**Why it matters for business**:
- **Lost revenue**: Each stockout = missed sale opportunity
- **Customer churn**: 70% of customers will switch to competitors after stockouts
- **Target**: Keep below 2-3% for critical items

**Actionable insights**:
- Identify products needing safety stock increases
- Improve demand forecasting accuracy
- Establish automatic reorder triggers

---

### 💰 Carrying Cost Rate

**Formula**: `(Total Carrying Costs / Average Inventory Value) × 100`

**What it measures**: Annual cost of holding inventory as a percentage of its value.

**Why it matters for business**:
- **Components**: Storage, insurance, depreciation, obsolescence, capital cost
- **Industry average**: 20-30% of inventory value annually
- **Optimization**: Balance between carrying costs and stockout risks

**Actionable insights**:
- Reduce warehouse space through better inventory levels
- Identify high-cost storage items for alternative solutions
- Optimize order quantities to minimize total costs

---

### 🎯 Fill Rate (Order Fulfillment Rate)

**Formula**: `(Orders Fulfilled Completely / Total Orders) × 100`

**What it measures**: Percentage of orders shipped complete on the first attempt.

**Why it matters for business**:
- **Customer satisfaction**: Direct correlation with repeat purchases
- **Operational efficiency**: Reduces partial shipments and backorders
- **Target**: 95-98% for competitive businesses

**Actionable insights**:
- Improve inventory accuracy through cycle counting
- Enhance demand forecasting models
- Prioritize critical SKUs for higher service levels

---

### ⚡ Inventory Accuracy

**Formula**: `(Correct Inventory Records / Total Records) × 100`

**What it measures**: Match between system records and physical inventory counts.

**Why it matters for business**:
- **Foundation**: Enables all other inventory optimization
- **Impact**: Inaccurate data leads to wrong ordering decisions
- **Target**: 97%+ accuracy for world-class operations

**Actionable insights**:
- Implement cycle counting programs
- Investigate and fix root causes of discrepancies
- Train staff on proper inventory handling procedures

---

### 🔒 Safety Stock Level

**Formula**: `(Maximum Daily Usage - Average Daily Usage) × Lead Time`

**What it measures**: Buffer stock to protect against demand variability and supply delays.

**Why it matters for business**:
- **Protection**: Guards against stockouts during demand spikes
- **Balance**: Too much = excess carrying costs, too little = stockouts
- **Dynamic**: Should adjust based on demand patterns and supplier reliability

**Actionable insights**:
- Segment products by demand variability
- Adjust safety stock seasonally
- Monitor supplier lead time consistency

---

### 📦 ABC Classification Metrics

**Categories**:
- **A Items**: ~20% of SKUs, ~80% of revenue (high focus)
- **B Items**: ~30% of SKUs, ~15% of revenue (moderate focus)
- **C Items**: ~50% of SKUs, ~5% of revenue (low focus)

**Why it matters for business**:
- **Resource allocation**: Focus efforts on highest-value items
- **Differentiated policies**: Service levels and safety stock by category
- **Cost optimization**: Reduce effort on low-value items

**Actionable insights**:
- Apply tighter controls to A items
- Consider vendor-managed inventory for C items
- Review classification quarterly

---

### 📈 Gross Margin Return on Investment (GMROI)

**Formula**: `Gross Profit / Average Inventory Cost`

**What it measures**: Profit generated for every dollar invested in inventory.

**Why it matters for business**:
- **ROI focus**: Links inventory investment to profitability
- **Target**: >3.0 for healthy retail operations
- **Decision making**: Helps prioritize which products to stock

**Actionable insights**:
- Identify low-GMROI products for pricing review
- Optimize product mix for better returns
- Negotiate better costs with suppliers for high-volume items

---

### 📊 Weeks of Supply

**Formula**: `Current Inventory / Average Weekly Sales`

**What it measures**: How many weeks current inventory will last at average sales rate.

**Why it matters for business**:
- **Planning**: Essential for replenishment timing
- **Cash flow**: Identifies excess inventory tying up capital
- **Target**: Varies by product category and seasonality

**Actionable insights**:
- Flag items with excessive weeks of supply
- Plan promotions for slow-moving inventory
- Adjust ordering patterns based on trends

---

## 📁 Project Structure

```
06_inventory_analysis/
├── README.md
├── data/
│   ├── inventory_data.csv
│   ├── products.csv
│   ├── sales_transactions.csv
│   └── suppliers.csv
├── notebooks/
│   └── inventory_analysis_dashboard.ipynb    # 📊 Interactive visualizations
├── scripts/
│   ├── generate_inventory_data.py
│   └── inventory_analysis.py
└── outputs/
    ├── inventory_kpis.csv
    ├── abc_classification.csv
    └── critical_items.csv
```

## 🚀 Quick Start

```bash
# Generate synthetic inventory data
python scripts/generate_inventory_data.py

# Run inventory analysis and calculate KPIs
python scripts/inventory_analysis.py
```

## 📊 Sample Dashboard Metrics

After running the analysis, you'll have:

| Metric | Value | Status |
|--------|-------|--------|
| Inventory Turnover | 7.2x | 🟢 Good |
| Days Sales of Inventory | 51 days | 🟢 Good |
| Stockout Rate | 2.8% | 🟡 Monitor |
| Fill Rate | 96.5% | 🟢 Good |
| Carrying Cost Rate | 23% | 🟡 Monitor |
| Inventory Accuracy | 98.2% | 🟢 Good |

## 💼 Business Impact Summary

Implementing these KPI-driven insights can help businesses achieve:

| Improvement Area | Typical Impact |
|-----------------|----------------|
| Inventory Reduction | 15-25% decrease in stock levels |
| Stockout Reduction | 50-70% fewer stockouts |
| Carrying Cost Savings | 10-20% reduction |
| Cash Flow Improvement | 20-30% faster inventory-to-cash cycle |
| Customer Satisfaction | 5-10% improvement in service levels |

---

*All data is simulated data for analytical demonstration.*
