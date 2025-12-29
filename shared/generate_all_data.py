"""
Shared Data Generator - Creates dummy datasets for all projects
All data is 100% synthetic for portfolio demonstration purposes.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================================
# CONFIGURATION
# ============================================================================

REGIONS = ['North', 'South', 'East', 'West', 'Central']
PRODUCT_CATEGORIES = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
CUSTOMER_SEGMENTS = ['Premium', 'Standard', 'Budget']
PAYMENT_METHODS = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash']

PRODUCTS = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smartwatch'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Dress'],
    'Home & Garden': ['Sofa', 'Table', 'Lamp', 'Plant Pot', 'Rug'],
    'Sports': ['Running Shoes', 'Yoga Mat', 'Dumbbells', 'Bicycle', 'Tennis Racket'],
    'Books': ['Fiction Novel', 'Cookbook', 'Tech Manual', 'Biography', 'Self-Help']
}


def generate_sales_data(num_records: int = 10000, start_date: str = '2024-01-01') -> pd.DataFrame:
    """Generate synthetic sales transaction data."""
    
    start = datetime.strptime(start_date, '%Y-%m-%d')
    
    data = []
    for i in range(num_records):
        category = random.choice(PRODUCT_CATEGORIES)
        product = random.choice(PRODUCTS[category])
        region = random.choice(REGIONS)
        segment = random.choice(CUSTOMER_SEGMENTS)
        
        # Price based on category
        base_price = {
            'Electronics': random.uniform(100, 1500),
            'Clothing': random.uniform(20, 200),
            'Home & Garden': random.uniform(50, 800),
            'Sports': random.uniform(30, 500),
            'Books': random.uniform(10, 50)
        }[category]
        
        quantity = random.randint(1, 5)
        unit_price = round(base_price, 2)
        discount = round(random.uniform(0, 0.3), 2)
        revenue = round(unit_price * quantity * (1 - discount), 2)
        cost = round(revenue * random.uniform(0.4, 0.7), 2)
        profit = round(revenue - cost, 2)
        
        data.append({
            'transaction_id': f'TXN-{i+1:06d}',
            'date': start + timedelta(days=random.randint(0, 365)),
            'customer_id': f'CUST-{random.randint(1, 2000):05d}',
            'customer_segment': segment,
            'region': region,
            'product_category': category,
            'product_name': product,
            'quantity': quantity,
            'unit_price': unit_price,
            'discount_percent': discount,
            'revenue': revenue,
            'cost': cost,
            'profit': profit,
            'payment_method': random.choice(PAYMENT_METHODS)
        })
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date').reset_index(drop=True)


def generate_customer_data(num_customers: int = 2000) -> pd.DataFrame:
    """Generate synthetic customer demographic data."""
    
    first_names = ['John', 'Jane', 'Alex', 'Maria', 'Ahmed', 'Sarah', 'Omar', 'Fatima', 'Michael', 'Lisa']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    data = []
    for i in range(num_customers):
        data.append({
            'customer_id': f'CUST-{i+1:05d}',
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'email': f'customer{i+1}@example.com',
            'age': random.randint(18, 75),
            'gender': random.choice(['Male', 'Female', 'Other']),
            'region': random.choice(REGIONS),
            'segment': random.choice(CUSTOMER_SEGMENTS),
            'registration_date': datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1500)),
            'total_purchases': random.randint(1, 100),
            'lifetime_value': round(random.uniform(100, 10000), 2)
        })
    
    return pd.DataFrame(data)


def generate_telecom_kpi_data(num_records: int = 5000, start_date: str = '2024-01-01') -> pd.DataFrame:
    """Generate synthetic telecom KPI data for network performance."""
    
    start = datetime.strptime(start_date, '%Y-%m-%d')
    technologies = ['4G', '5G', '3G']
    
    data = []
    for i in range(num_records):
        tech = random.choice(technologies)
        
        # KPIs vary by technology
        if tech == '5G':
            availability = round(random.uniform(97, 99.99), 2)
            latency = round(random.uniform(1, 10), 2)
            throughput = round(random.uniform(100, 1000), 2)
        elif tech == '4G':
            availability = round(random.uniform(95, 99.5), 2)
            latency = round(random.uniform(20, 50), 2)
            throughput = round(random.uniform(20, 150), 2)
        else:
            availability = round(random.uniform(90, 98), 2)
            latency = round(random.uniform(80, 200), 2)
            throughput = round(random.uniform(1, 20), 2)
        
        data.append({
            'record_id': f'KPI-{i+1:06d}',
            'date': start + timedelta(days=random.randint(0, 365)),
            'site_id': f'SITE-{random.randint(1, 500):04d}',
            'cell_id': f'CELL-{random.randint(1, 2000):05d}',
            'region': random.choice(REGIONS),
            'technology': tech,
            'availability_percent': availability,
            'latency_ms': latency,
            'throughput_mbps': throughput,
            'call_drop_rate': round(random.uniform(0, 3), 2),
            'handover_success_rate': round(random.uniform(95, 99.9), 2),
            'traffic_volume_gb': round(random.uniform(10, 1000), 2),
            'active_users': random.randint(100, 10000)
        })
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date').reset_index(drop=True)


def generate_data_quality_issues(df: pd.DataFrame, issue_rate: float = 0.05) -> pd.DataFrame:
    """Inject data quality issues for testing validation frameworks."""
    
    df_with_issues = df.copy()
    num_issues = int(len(df) * issue_rate)
    
    # Inject NULL values
    null_indices = random.sample(range(len(df)), num_issues // 3)
    for idx in null_indices:
        col = random.choice(df.columns)
        df_with_issues.at[idx, col] = None
    
    # Inject duplicates
    dup_indices = random.sample(range(len(df)), num_issues // 3)
    duplicates = df.iloc[dup_indices].copy()
    df_with_issues = pd.concat([df_with_issues, duplicates], ignore_index=True)
    
    return df_with_issues


def save_for_powerbi(df: pd.DataFrame, filename: str, output_dir: str = '../powerbi_exports'):
    """Save DataFrame in Power BI friendly format."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save as CSV (Power BI compatible)
    filepath = os.path.join(output_dir, f'{filename}.csv')
    df.to_csv(filepath, index=False)
    print(f"✅ Saved Power BI export: {filepath}")
    
    return filepath


def main():
    """Generate all dummy datasets for the portfolio."""
    
    print("🚀 Generating dummy data for portfolio projects...\n")
    
    # Create output directory
    output_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(output_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate Sales Data
    print("📊 Generating sales data...")
    sales_df = generate_sales_data(10000)
    sales_df.to_csv(os.path.join(data_dir, 'sales_transactions.csv'), index=False)
    print(f"   ✅ {len(sales_df)} sales transactions generated")
    
    # Generate Customer Data
    print("👥 Generating customer data...")
    customers_df = generate_customer_data(2000)
    customers_df.to_csv(os.path.join(data_dir, 'customers.csv'), index=False)
    print(f"   ✅ {len(customers_df)} customers generated")
    
    # Generate Telecom KPI Data
    print("📡 Generating telecom KPI data...")
    telecom_df = generate_telecom_kpi_data(5000)
    telecom_df.to_csv(os.path.join(data_dir, 'telecom_kpis.csv'), index=False)
    print(f"   ✅ {len(telecom_df)} KPI records generated")
    
    # Generate Data with Quality Issues (for testing)
    print("🔍 Generating data with quality issues (for testing)...")
    sales_with_issues = generate_data_quality_issues(sales_df)
    sales_with_issues.to_csv(os.path.join(data_dir, 'sales_with_issues.csv'), index=False)
    print(f"   ✅ {len(sales_with_issues)} records with injected issues")
    
    # Save Power BI exports
    print("\n📈 Creating Power BI exports...")
    powerbi_dir = os.path.join(output_dir, '..', 'powerbi_exports')
    save_for_powerbi(sales_df, 'sales_data', powerbi_dir)
    save_for_powerbi(customers_df, 'customer_data', powerbi_dir)
    save_for_powerbi(telecom_df, 'telecom_kpi_data', powerbi_dir)
    
    print("\n✨ All dummy data generated successfully!")
    print(f"   Data location: {data_dir}")
    print(f"   Power BI exports: {powerbi_dir}")


if __name__ == '__main__':
    main()
