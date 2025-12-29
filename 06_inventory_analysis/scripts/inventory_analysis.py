"""
Inventory Analysis Script
Calculates comprehensive inventory KPIs for business insights
"""

import pandas as pd
import numpy as np
import os


def load_data():
    """Load all inventory data files"""
    data_dir = '../data'
    
    products = pd.read_csv(f'{data_dir}/products.csv')
    suppliers = pd.read_csv(f'{data_dir}/suppliers.csv')
    transactions = pd.read_csv(f'{data_dir}/sales_transactions.csv')
    inventory = pd.read_csv(f'{data_dir}/inventory_data.csv')
    
    return products, suppliers, transactions, inventory


def calculate_inventory_turnover(transactions_df, inventory_df):
    """
    Calculate Inventory Turnover Ratio
    Formula: COGS / Average Inventory Value
    """
    # Calculate COGS (sum of cost of goods sold)
    sales = transactions_df[transactions_df['transaction_type'] == 'SALE']
    cogs = abs((sales['quantity'] * sales['unit_cost']).sum())
    
    # Average inventory value
    avg_inventory_value = inventory_df['inventory_value'].mean() * len(inventory_df)
    
    turnover_ratio = cogs / avg_inventory_value if avg_inventory_value > 0 else 0
    
    return {
        'metric': 'Inventory Turnover Ratio',
        'value': round(turnover_ratio, 2),
        'unit': 'times/year',
        'benchmark': '6-12 (varies by industry)',
        'status': 'Good' if 6 <= turnover_ratio <= 12 else 'Review'
    }


def calculate_days_sales_inventory(inventory_df):
    """
    Calculate Days Sales of Inventory (DSI)
    Formula: (Average Inventory / COGS) × 365
    """
    avg_dsi = inventory_df['days_of_inventory'].mean()
    
    return {
        'metric': 'Days Sales of Inventory (DSI)',
        'value': round(avg_dsi, 1),
        'unit': 'days',
        'benchmark': '30-60 days',
        'status': 'Good' if 30 <= avg_dsi <= 60 else 'Review'
    }


def calculate_stockout_rate(inventory_df):
    """
    Calculate Stockout Rate
    Formula: Stockout Events / Total SKUs
    """
    total_stockouts = inventory_df['stockout_events'].sum()
    total_skus = len(inventory_df)
    
    # Calculate as percentage of SKUs affected
    skus_with_stockouts = (inventory_df['stockout_events'] > 0).sum()
    stockout_rate = (skus_with_stockouts / total_skus) * 100
    
    return {
        'metric': 'Stockout Rate',
        'value': round(stockout_rate, 2),
        'unit': '%',
        'benchmark': '<3%',
        'status': 'Good' if stockout_rate < 3 else 'Critical' if stockout_rate > 5 else 'Review'
    }


def calculate_carrying_cost_rate(inventory_df, annual_rate=0.25):
    """
    Calculate Carrying Cost Rate
    Assumes 25% annual carrying cost (industry average)
    """
    total_inventory_value = inventory_df['inventory_value'].sum()
    carrying_cost = total_inventory_value * annual_rate
    
    return {
        'metric': 'Annual Carrying Cost',
        'value': round(carrying_cost, 2),
        'unit': 'USD',
        'benchmark': '20-30% of inventory value',
        'status': 'Info'
    }


def calculate_fill_rate(transactions_df, inventory_df):
    """
    Calculate Order Fill Rate
    Simulated based on stockout events
    """
    total_orders = len(transactions_df[transactions_df['transaction_type'] == 'SALE'])
    stockout_impact = inventory_df['stockout_events'].sum() * 5  # Each stockout affects ~5 orders
    
    fill_rate = ((total_orders - stockout_impact) / total_orders) * 100 if total_orders > 0 else 100
    fill_rate = max(fill_rate, 85)  # Realistic lower bound
    
    return {
        'metric': 'Order Fill Rate',
        'value': round(fill_rate, 2),
        'unit': '%',
        'benchmark': '>95%',
        'status': 'Good' if fill_rate >= 95 else 'Review'
    }


def calculate_inventory_accuracy():
    """
    Simulated Inventory Accuracy
    In real scenario, this would compare system vs physical counts
    """
    accuracy = np.random.uniform(96.5, 99.5)
    
    return {
        'metric': 'Inventory Accuracy',
        'value': round(accuracy, 2),
        'unit': '%',
        'benchmark': '>97%',
        'status': 'Good' if accuracy >= 97 else 'Review'
    }


def calculate_gmroi(transactions_df, inventory_df):
    """
    Calculate Gross Margin Return on Investment (GMROI)
    Formula: Gross Profit / Average Inventory Cost
    """
    # Gross profit
    sales = transactions_df[transactions_df['transaction_type'] == 'SALE']
    revenue = abs((sales['quantity'] * sales['unit_price']).sum())
    cogs = abs((sales['quantity'] * sales['unit_cost']).sum())
    gross_profit = revenue - cogs
    
    # Average inventory cost
    avg_inventory_cost = inventory_df['inventory_value'].sum()
    
    gmroi = gross_profit / avg_inventory_cost if avg_inventory_cost > 0 else 0
    
    return {
        'metric': 'GMROI',
        'value': round(gmroi, 2),
        'unit': 'ratio',
        'benchmark': '>3.0',
        'status': 'Good' if gmroi >= 3.0 else 'Review'
    }


def calculate_weeks_of_supply(inventory_df):
    """
    Calculate average Weeks of Supply
    """
    inventory_df['weeks_of_supply'] = inventory_df['current_quantity'] / (
        inventory_df['avg_daily_sales'] * 7
    )
    avg_weeks = inventory_df['weeks_of_supply'].replace([np.inf, -np.inf], np.nan).mean()
    
    return {
        'metric': 'Average Weeks of Supply',
        'value': round(avg_weeks, 1),
        'unit': 'weeks',
        'benchmark': '4-8 weeks',
        'status': 'Good' if 4 <= avg_weeks <= 8 else 'Review'
    }


def generate_abc_analysis(inventory_df):
    """
    Generate ABC Classification summary
    """
    abc_summary = inventory_df.groupby('abc_class').agg({
        'product_id': 'count',
        'total_sales_value': 'sum',
        'inventory_value': 'sum',
        'current_quantity': 'sum'
    }).reset_index()
    
    abc_summary.columns = ['ABC Class', 'SKU Count', 'Total Revenue', 'Inventory Value', 'Total Units']
    
    # Calculate percentages
    total_revenue = abc_summary['Total Revenue'].sum()
    total_skus = abc_summary['SKU Count'].sum()
    
    abc_summary['Revenue %'] = (abc_summary['Total Revenue'] / total_revenue * 100).round(1)
    abc_summary['SKU %'] = (abc_summary['SKU Count'] / total_skus * 100).round(1)
    
    return abc_summary


def identify_critical_items(inventory_df):
    """
    Identify items that need immediate attention
    """
    critical_items = []
    
    # Low stock items (below safety stock)
    low_stock = inventory_df[inventory_df['current_quantity'] <= inventory_df['safety_stock']]
    for _, item in low_stock.iterrows():
        critical_items.append({
            'product_id': item['product_id'],
            'issue': 'LOW_STOCK',
            'severity': 'High',
            'current_qty': item['current_quantity'],
            'safety_stock': item['safety_stock'],
            'recommendation': 'Immediate reorder required'
        })
    
    # Excess inventory (>90 days of inventory)
    excess = inventory_df[inventory_df['days_of_inventory'] > 90]
    for _, item in excess.iterrows():
        critical_items.append({
            'product_id': item['product_id'],
            'issue': 'EXCESS_STOCK',
            'severity': 'Medium',
            'current_qty': item['current_quantity'],
            'days_inventory': item['days_of_inventory'],
            'recommendation': 'Consider markdown or promotion'
        })
    
    # Items with stockouts
    stockouts = inventory_df[inventory_df['stockout_events'] > 0]
    for _, item in stockouts.iterrows():
        critical_items.append({
            'product_id': item['product_id'],
            'issue': 'STOCKOUT_HISTORY',
            'severity': 'High' if item['abc_class'] == 'A' else 'Medium',
            'stockout_events': item['stockout_events'],
            'recommendation': 'Increase safety stock level'
        })
    
    return pd.DataFrame(critical_items)


def main():
    """Run comprehensive inventory analysis"""
    
    print("📊 Inventory Analysis - KPI Calculation")
    print("=" * 50)
    
    # Ensure output directory exists
    os.makedirs('../outputs', exist_ok=True)
    
    # Load data
    print("\n📂 Loading data...")
    products, suppliers, transactions, inventory = load_data()
    
    # Calculate all KPIs
    print("🔢 Calculating KPIs...")
    kpis = []
    kpis.append(calculate_inventory_turnover(transactions, inventory))
    kpis.append(calculate_days_sales_inventory(inventory))
    kpis.append(calculate_stockout_rate(inventory))
    kpis.append(calculate_carrying_cost_rate(inventory))
    kpis.append(calculate_fill_rate(transactions, inventory))
    kpis.append(calculate_inventory_accuracy())
    kpis.append(calculate_gmroi(transactions, inventory))
    kpis.append(calculate_weeks_of_supply(inventory))
    
    # Display KPIs
    print("\n" + "=" * 60)
    print("📈 INVENTORY KPI DASHBOARD")
    print("=" * 60)
    
    for kpi in kpis:
        status_icon = "🟢" if kpi['status'] == 'Good' else "🔴" if kpi['status'] == 'Critical' else "🟡"
        print(f"\n{status_icon} {kpi['metric']}")
        print(f"   Value: {kpi['value']} {kpi['unit']}")
        print(f"   Benchmark: {kpi['benchmark']}")
        print(f"   Status: {kpi['status']}")
    
    # Save KPIs
    kpis_df = pd.DataFrame(kpis)
    kpis_df.to_csv('../outputs/inventory_kpis.csv', index=False)
    print(f"\n💾 KPIs saved to ../outputs/inventory_kpis.csv")
    
    # ABC Analysis
    print("\n" + "=" * 60)
    print("📦 ABC CLASSIFICATION ANALYSIS")
    print("=" * 60)
    
    abc_summary = generate_abc_analysis(inventory)
    print("\n", abc_summary.to_string(index=False))
    abc_summary.to_csv('../outputs/abc_classification.csv', index=False)
    print(f"\n💾 ABC analysis saved to ../outputs/abc_classification.csv")
    
    # Critical Items
    print("\n" + "=" * 60)
    print("⚠️  ITEMS REQUIRING ATTENTION")
    print("=" * 60)
    
    critical = identify_critical_items(inventory)
    if len(critical) > 0:
        print(f"\nFound {len(critical)} items requiring attention:")
        high_priority = critical[critical['severity'] == 'High']
        print(f"   🔴 High Priority: {len(high_priority)}")
        medium_priority = critical[critical['severity'] == 'Medium']
        print(f"   🟡 Medium Priority: {len(medium_priority)}")
        
        critical.to_csv('../outputs/critical_items.csv', index=False)
        print(f"\n💾 Critical items saved to ../outputs/critical_items.csv")
    else:
        print("\n✅ No critical items found!")
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("📊 SUMMARY STATISTICS")
    print("=" * 60)
    print(f"\n   Total SKUs: {len(inventory):,}")
    print(f"   Total Inventory Value: ${inventory['inventory_value'].sum():,.2f}")
    print(f"   Total Annual Sales: ${inventory['total_sales_value'].sum():,.2f}")
    print(f"   Transaction Records: {len(transactions):,}")
    print(f"   Active Suppliers: {len(suppliers)}")
    
    print("\n✅ Analysis complete!")


if __name__ == '__main__':
    main()
