"""
Inventory Data Generator
Generates synthetic inventory data for portfolio demonstration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

def generate_products(n_products=200):
    """Generate product master data with ABC classification"""
    
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Food & Beverage', 'Office Supplies']
    
    products = []
    for i in range(1, n_products + 1):
        category = np.random.choice(categories)
        
        # Price ranges by category
        price_ranges = {
            'Electronics': (50, 2000),
            'Clothing': (15, 200),
            'Home & Garden': (10, 500),
            'Sports': (20, 400),
            'Food & Beverage': (2, 50),
            'Office Supplies': (1, 100)
        }
        
        min_price, max_price = price_ranges[category]
        unit_cost = round(np.random.uniform(min_price, max_price), 2)
        
        products.append({
            'product_id': f'SKU-{i:04d}',
            'product_name': f'{category} Item {i}',
            'category': category,
            'unit_cost': unit_cost,
            'unit_price': round(unit_cost * np.random.uniform(1.2, 1.8), 2),
            'lead_time_days': np.random.choice([3, 5, 7, 10, 14, 21]),
            'min_order_qty': np.random.choice([10, 25, 50, 100]),
            'supplier_id': f'SUP-{np.random.randint(1, 21):03d}'
        })
    
    return pd.DataFrame(products)


def generate_suppliers(n_suppliers=20):
    """Generate supplier master data"""
    
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
    reliability_scores = [0.85, 0.88, 0.9, 0.92, 0.95, 0.97, 0.99]
    
    suppliers = []
    for i in range(1, n_suppliers + 1):
        suppliers.append({
            'supplier_id': f'SUP-{i:03d}',
            'supplier_name': f'Supplier {i} Inc.',
            'region': np.random.choice(regions),
            'reliability_score': np.random.choice(reliability_scores),
            'avg_lead_time_days': np.random.randint(3, 21),
            'payment_terms_days': np.random.choice([15, 30, 45, 60])
        })
    
    return pd.DataFrame(suppliers)


def generate_inventory_transactions(products_df, start_date, end_date):
    """Generate daily inventory transactions"""
    
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    transactions = []
    
    # Initialize inventory levels
    current_inventory = {}
    for _, product in products_df.iterrows():
        product_id = product['product_id']
        # Initial stock based on price tier
        initial_stock = np.random.randint(50, 500)
        current_inventory[product_id] = initial_stock
    
    transaction_id = 1
    for date in date_range:
        for _, product in products_df.iterrows():
            product_id = product['product_id']
            
            # Daily sales (with some randomness and weekday pattern)
            weekday_multiplier = 1.2 if date.weekday() < 5 else 0.8
            base_sales = np.random.poisson(lam=5) * weekday_multiplier
            
            # Adjust for seasonality (higher sales in Q4)
            if date.month in [10, 11, 12]:
                base_sales *= 1.5
            
            daily_sales = int(min(base_sales, current_inventory[product_id]))
            
            if daily_sales > 0:
                transactions.append({
                    'transaction_id': transaction_id,
                    'date': date.strftime('%Y-%m-%d'),
                    'product_id': product_id,
                    'transaction_type': 'SALE',
                    'quantity': -daily_sales,
                    'unit_cost': product['unit_cost'],
                    'unit_price': product['unit_price']
                })
                current_inventory[product_id] -= daily_sales
                transaction_id += 1
            
            # Reorder when stock is low
            reorder_point = product['min_order_qty'] * 2
            if current_inventory[product_id] < reorder_point:
                reorder_qty = product['min_order_qty'] * np.random.randint(2, 5)
                transactions.append({
                    'transaction_id': transaction_id,
                    'date': date.strftime('%Y-%m-%d'),
                    'product_id': product_id,
                    'transaction_type': 'PURCHASE',
                    'quantity': reorder_qty,
                    'unit_cost': product['unit_cost'],
                    'unit_price': 0
                })
                current_inventory[product_id] += reorder_qty
                transaction_id += 1
    
    return pd.DataFrame(transactions)


def generate_inventory_snapshot(products_df, transactions_df):
    """Generate current inventory status with calculated metrics"""
    
    inventory_data = []
    
    for _, product in products_df.iterrows():
        product_id = product['product_id']
        product_txns = transactions_df[transactions_df['product_id'] == product_id]
        
        # Calculate current inventory
        current_qty = product_txns['quantity'].sum()
        if current_qty < 0:
            current_qty = np.random.randint(10, 100)  # Ensure positive inventory
        
        # Calculate metrics
        sales_txns = product_txns[product_txns['transaction_type'] == 'SALE']
        total_sales_qty = abs(sales_txns['quantity'].sum())
        total_sales_value = total_sales_qty * product['unit_price']
        
        # Days in analysis period
        days_in_period = 365
        avg_daily_sales = total_sales_qty / days_in_period if days_in_period > 0 else 0
        
        # Calculate DSI
        dsi = current_qty / avg_daily_sales if avg_daily_sales > 0 else 999
        
        # Calculate stockout events (simulated)
        stockout_events = np.random.poisson(lam=2) if current_qty < 20 else 0
        
        # Calculate inventory value
        inventory_value = current_qty * product['unit_cost']
        
        # ABC Classification based on sales value
        revenue_rank_value = total_sales_value
        
        inventory_data.append({
            'product_id': product_id,
            'product_name': product['product_name'],
            'category': product['category'],
            'current_quantity': int(current_qty),
            'unit_cost': product['unit_cost'],
            'inventory_value': round(inventory_value, 2),
            'total_sales_qty': int(total_sales_qty),
            'total_sales_value': round(total_sales_value, 2),
            'avg_daily_sales': round(avg_daily_sales, 2),
            'days_of_inventory': round(dsi, 1),
            'stockout_events': stockout_events,
            'lead_time_days': product['lead_time_days'],
            'reorder_point': int(avg_daily_sales * product['lead_time_days'] * 1.5),
            'safety_stock': int(avg_daily_sales * product['lead_time_days'] * 0.5),
            'supplier_id': product['supplier_id'],
            'revenue_rank_value': revenue_rank_value
        })
    
    df = pd.DataFrame(inventory_data)
    
    # ABC Classification
    df = df.sort_values('revenue_rank_value', ascending=False)
    df['cumulative_revenue_pct'] = df['revenue_rank_value'].cumsum() / df['revenue_rank_value'].sum() * 100
    
    def assign_abc(pct):
        if pct <= 80:
            return 'A'
        elif pct <= 95:
            return 'B'
        else:
            return 'C'
    
    df['abc_class'] = df['cumulative_revenue_pct'].apply(assign_abc)
    df = df.drop(columns=['revenue_rank_value', 'cumulative_revenue_pct'])
    
    return df


def main():
    """Generate all inventory datasets"""
    
    print("🏭 Generating Inventory Analysis Data...")
    
    # Create output directories
    os.makedirs('../data', exist_ok=True)
    os.makedirs('../outputs', exist_ok=True)
    
    # Date range for analysis
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Generate data
    print("  📦 Generating products...")
    products_df = generate_products(200)
    
    print("  🚚 Generating suppliers...")
    suppliers_df = generate_suppliers(20)
    
    print("  📊 Generating transactions (this may take a moment)...")
    transactions_df = generate_inventory_transactions(products_df, start_date, end_date)
    
    print("  📈 Calculating inventory metrics...")
    inventory_df = generate_inventory_snapshot(products_df, transactions_df)
    
    # Save data files
    print("  💾 Saving data files...")
    products_df.to_csv('../data/products.csv', index=False)
    suppliers_df.to_csv('../data/suppliers.csv', index=False)
    transactions_df.to_csv('../data/sales_transactions.csv', index=False)
    inventory_df.to_csv('../data/inventory_data.csv', index=False)
    
    # Summary statistics
    print("\n✅ Data generation complete!")
    print(f"   Products: {len(products_df)} SKUs")
    print(f"   Suppliers: {len(suppliers_df)}")
    print(f"   Transactions: {len(transactions_df):,}")
    print(f"   Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # ABC Classification summary
    abc_summary = inventory_df.groupby('abc_class').agg({
        'product_id': 'count',
        'total_sales_value': 'sum',
        'inventory_value': 'sum'
    }).round(2)
    print("\n📊 ABC Classification Summary:")
    print(abc_summary)


if __name__ == '__main__':
    main()
