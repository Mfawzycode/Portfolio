"""
Financial Data Generator
Creates synthetic financial datasets for analysis demonstration.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# Configuration
DEPARTMENTS = ['Sales', 'Marketing', 'Engineering', 'HR', 'Operations', 'Finance', 'IT']
EXPENSE_CATEGORIES = ['Salaries', 'Marketing', 'Software', 'Equipment', 'Travel', 'Office', 'Utilities', 'Training']
REVENUE_STREAMS = ['Product Sales', 'Services', 'Subscriptions', 'Consulting', 'Licensing']


def generate_budget_data(year: int = 2024) -> pd.DataFrame:
    """Generate annual budget data by department."""
    data = []
    
    for dept in DEPARTMENTS:
        # Base budget varies by department
        base_budget = {
            'Sales': 500000, 'Marketing': 350000, 'Engineering': 800000,
            'HR': 200000, 'Operations': 450000, 'Finance': 250000, 'IT': 400000
        }[dept]
        
        for month in range(1, 13):
            # Add seasonal variation
            seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * month / 12)
            monthly_budget = base_budget / 12 * seasonal_factor
            
            for category in random.sample(EXPENSE_CATEGORIES, random.randint(4, 7)):
                allocation = random.uniform(0.05, 0.3)
                
                data.append({
                    'year': year,
                    'month': month,
                    'department': dept,
                    'expense_category': category,
                    'budgeted_amount': round(monthly_budget * allocation, 2),
                    'budget_id': f'BUD-{year}-{dept[:3].upper()}-{month:02d}'
                })
    
    return pd.DataFrame(data)


def generate_transactions(year: int = 2024, num_records: int = 5000) -> pd.DataFrame:
    """Generate financial transaction data."""
    start_date = datetime(year, 1, 1)
    
    data = []
    for i in range(num_records):
        dept = random.choice(DEPARTMENTS)
        category = random.choice(EXPENSE_CATEGORIES)
        
        # Transaction amount based on category
        base_amounts = {
            'Salaries': (3000, 15000), 'Marketing': (500, 10000), 'Software': (100, 5000),
            'Equipment': (200, 8000), 'Travel': (100, 3000), 'Office': (50, 1000),
            'Utilities': (200, 2000), 'Training': (200, 3000)
        }
        amount_range = base_amounts.get(category, (100, 5000))
        
        data.append({
            'transaction_id': f'TXN-{i+1:06d}',
            'date': start_date + timedelta(days=random.randint(0, 364)),
            'department': dept,
            'expense_category': category,
            'amount': round(random.uniform(*amount_range), 2),
            'vendor': f'Vendor-{random.randint(1, 100):03d}',
            'payment_method': random.choice(['Credit Card', 'Bank Transfer', 'Check', 'Cash']),
            'approved_by': f'Manager-{random.randint(1, 20):02d}',
            'status': random.choices(['Completed', 'Pending', 'Rejected'], weights=[0.85, 0.10, 0.05])[0]
        })
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    return df.sort_values('date').reset_index(drop=True)


def generate_revenue_data(year: int = 2024) -> pd.DataFrame:
    """Generate monthly revenue data."""
    data = []
    
    for month in range(1, 13):
        for stream in REVENUE_STREAMS:
            # Base revenue with growth trend
            base = {'Product Sales': 200000, 'Services': 150000, 'Subscriptions': 80000, 
                    'Consulting': 60000, 'Licensing': 40000}[stream]
            
            # Add growth and seasonal variation
            growth = 1 + 0.02 * month  # 2% monthly growth
            seasonal = 1 + 0.15 * np.sin(2 * np.pi * (month - 3) / 12)  # Peak in Q2
            
            revenue = base * growth * seasonal * random.uniform(0.9, 1.1)
            
            data.append({
                'year': year,
                'month': month,
                'revenue_stream': stream,
                'revenue': round(revenue, 2),
                'units_sold': random.randint(100, 1000) if stream == 'Product Sales' else None,
                'new_customers': random.randint(10, 100)
            })
    
    return pd.DataFrame(data)


def calculate_financial_kpis(transactions_df: pd.DataFrame, revenue_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate key financial KPIs."""
    # Monthly expenses
    monthly_expenses = transactions_df[transactions_df['status'] == 'Completed'].groupby(['month']).agg({
        'amount': 'sum'
    }).reset_index()
    monthly_expenses.columns = ['month', 'total_expenses']
    
    # Monthly revenue
    monthly_revenue = revenue_df.groupby('month').agg({
        'revenue': 'sum',
        'new_customers': 'sum'
    }).reset_index()
    monthly_revenue.columns = ['month', 'total_revenue', 'new_customers']
    
    # Merge and calculate KPIs
    kpis = pd.merge(monthly_revenue, monthly_expenses, on='month')
    kpis['gross_profit'] = kpis['total_revenue'] - kpis['total_expenses']
    kpis['profit_margin'] = round((kpis['gross_profit'] / kpis['total_revenue']) * 100, 2)
    kpis['expense_ratio'] = round((kpis['total_expenses'] / kpis['total_revenue']) * 100, 2)
    kpis['revenue_per_customer'] = round(kpis['total_revenue'] / kpis['new_customers'], 2)
    
    return kpis


def main():
    """Generate all financial datasets."""
    print("💰 Generating Financial Data...\n")
    
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate data
    budget_df = generate_budget_data()
    transactions_df = generate_transactions()
    revenue_df = generate_revenue_data()
    
    # Save datasets
    budget_df.to_csv(os.path.join(output_dir, 'budget_data.csv'), index=False)
    print(f"✅ Budget data: {len(budget_df)} records")
    
    transactions_df.to_csv(os.path.join(output_dir, 'transactions.csv'), index=False)
    print(f"✅ Transactions: {len(transactions_df)} records")
    
    revenue_df.to_csv(os.path.join(output_dir, 'revenue_data.csv'), index=False)
    print(f"✅ Revenue data: {len(revenue_df)} records")
    
    # Calculate and save KPIs
    kpis_df = calculate_financial_kpis(transactions_df, revenue_df)
    kpis_output = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(kpis_output, exist_ok=True)
    kpis_df.to_csv(os.path.join(kpis_output, 'financial_kpis.csv'), index=False)
    print(f"✅ Financial KPIs calculated and saved")
    
    # Power BI export
    powerbi_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'powerbi_exports')
    os.makedirs(powerbi_dir, exist_ok=True)
    transactions_df.to_csv(os.path.join(powerbi_dir, 'financial_transactions.csv'), index=False)
    kpis_df.to_csv(os.path.join(powerbi_dir, 'financial_kpis.csv'), index=False)
    print(f"✅ Power BI exports saved")
    
    print("\n✨ Financial data generation complete!")


if __name__ == '__main__':
    main()
