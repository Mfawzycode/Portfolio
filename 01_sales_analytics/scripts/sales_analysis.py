"""
Sales Analysis Script
Calculates comprehensive sales KPIs for business insights
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_data():
    """Load sales and customer data"""
    # Assuming the script runs from within 01_sales_analytics/scripts/
    # or from the project root. Let's make it robust.
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(base_dir, 'shared', 'data')
    
    sales_path = os.path.join(data_dir, 'sales_transactions.csv')
    customers_path = os.path.join(data_dir, 'customers.csv')
    
    if not os.path.exists(sales_path):
        print(f"❌ Data not found at {sales_path}. Please run shared/generate_all_data.py first.")
        return None, None
        
    sales = pd.read_csv(sales_path)
    customers = pd.read_csv(customers_path)
    
    sales['date'] = pd.to_datetime(sales['date'])
    customers['registration_date'] = pd.to_datetime(customers['registration_date'])
    
    return sales, customers

def calculate_sales_kpis(sales_df, customers_df):
    """Calculate all sales KPIs defined in the documentation"""
    
    kpis = []
    
    # 1. Total Revenue & Growth Rate (Monthly)
    monthly_revenue = sales_df.set_index('date').resample('ME')['revenue'].sum().reset_index()
    if len(monthly_revenue) >= 2:
        prev_month_rev = monthly_revenue.iloc[-2]['revenue']
        curr_month_rev = monthly_revenue.iloc[-1]['revenue']
        growth_rate = ((curr_month_rev - prev_month_rev) / prev_month_rev) * 100
    else:
        growth_rate = 0
        
    kpis.append({
        'metric': 'Revenue Growth Rate (Last Month)',
        'value': round(growth_rate, 2),
        'unit': '%',
        'status': 'Good' if growth_rate > 5 else 'Review'
    })
    
    # 2. Average Order Value (AOV)
    aov = sales_df['revenue'].mean()
    kpis.append({
        'metric': 'Average Order Value (AOV)',
        'value': round(aov, 2),
        'unit': 'USD',
        'status': 'Good' if aov > 100 else 'Low'
    })
    
    # 3. Customer Acquisition Cost (CAC) - Simulated
    # In real world, this would come from marketing spend data
    simulated_marketing_spend = sales_df['revenue'].sum() * 0.15
    new_customers = customers_df[customers_df['registration_date'] >= sales_df['date'].min()].shape[0]
    cac = simulated_marketing_spend / new_customers if new_customers > 0 else 0
    kpis.append({
        'metric': 'Esc. Customer Acquisition Cost (CAC)',
        'value': round(cac, 2),
        'unit': 'USD',
        'status': 'Info'
    })
    
    # 4. Customer Lifetime Value (CLV)
    avg_clv = customers_df['lifetime_value'].mean()
    kpis.append({
        'metric': 'Average Customer Lifetime Value (CLV)',
        'value': round(avg_clv, 2),
        'unit': 'USD',
        'status': 'Good' if avg_clv > cac * 3 else 'Review'
    })
    
    # 5. Churn Rate (Simulated based on last purchase date)
    max_date = sales_df['date'].max()
    last_purchases = sales_df.groupby('customer_id')['date'].max()
    churned_customers = (last_purchases < (max_date - pd.Timedelta(days=90))).sum()
    total_customers = sales_df['customer_id'].nunique()
    churn_rate = (churned_customers / total_customers) * 100 if total_customers > 0 else 0
    kpis.append({
        'metric': 'Customer Churn Rate (90-day)',
        'value': round(churn_rate, 2),
        'unit': '%',
        'status': 'Good' if churn_rate < 15 else 'Critical'
    })
    
    # 6. Sales Conversion Rate - Simulated
    conversion_rate = np.random.uniform(2.5, 4.5)
    kpis.append({
        'metric': 'Lead Conversion Rate',
        'value': round(conversion_rate, 2),
        'unit': '%',
        'status': 'Good' if conversion_rate > 3 else 'Review'
    })
    
    # 7. Retention Rate
    retention_rate = 100 - churn_rate
    kpis.append({
        'metric': 'Customer Retention Rate',
        'value': round(retention_rate, 2),
        'unit': '%',
        'status': 'Good' if retention_rate > 85 else 'Review'
    })
    
    # 8. Gross Margin per Product Category
    margins = sales_df.groupby('product_category').apply(
        lambda x: ((x['revenue'] - x['cost']).sum() / x['revenue'].sum()) * 100
    ).reset_index()
    avg_margin = margins[0].mean()
    kpis.append({
        'metric': 'Average Gross Margin',
        'value': round(avg_margin, 2),
        'unit': '%',
        'status': 'Good' if avg_margin > 40 else 'Low'
    })
    
    return pd.DataFrame(kpis), margins

def main():
    print("📊 Running Sales Analytics KPI Calculation...")
    
    sales, customers = load_data()
    if sales is None:
        return
        
    kpi_df, margins_df = calculate_sales_kpis(sales, customers)
    
    # Create output directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save KPIs
    kpi_df.to_csv(os.path.join(output_dir, 'sales_kpis.csv'), index=False)
    margins_df.to_csv(os.path.join(output_dir, 'category_margins.csv'), index=False)
    
    print("\n📈 SALES KPI DASHBOARD SUMMARY")
    print("=" * 50)
    for _, row in kpi_df.iterrows():
        icon = "🟢" if row['status'] == 'Good' else "🔴" if row['status'] == 'Critical' else "🟡"
        print(f"{icon} {row['metric']}: {row['value']}{row['unit']}")
    
    print("\n✅ Analysis complete. Results saved to 01_sales_analytics/outputs/")

if __name__ == '__main__':
    main()
