"""
Retail Financial Engine
Integrates Sales and Inventory data to produce Financial Statements and Ratios.
Exports a professional, formatted Excel report.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_source_data():
    """Load sales and inventory data from other project modules"""
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    sales_path = os.path.join(base_path, 'shared', 'data', 'sales_transactions.csv')
    inv_path = os.path.join(base_path, '06_inventory_analysis', 'outputs', 'inventory_enriched.csv')
    
    if not os.path.exists(sales_path) or not os.path.exists(inv_path):
        print("❌ Source data missing. Ensure you run shared/generate_all_data.py and 06_inventory_analysis/scripts/inventory_analysis.py")
        return None, None
        
    sales = pd.read_csv(sales_path)
    inventory = pd.read_csv(inv_path)
    
    sales['date'] = pd.to_datetime(sales['date'])
    return sales, inventory

def generate_income_statement(sales_df):
    """Generate a monthly consolidated Income Statement"""
    # Group by month
    sales_df['month'] = sales_df['date'].dt.to_period('M')
    
    monthly_is = sales_df.groupby('month').agg({
        'revenue': 'sum',
        'cost': 'sum',
        'profit': 'sum'
    }).rename(columns={'cost': 'COGS', 'profit': 'Gross Profit'})
    
    # Simulate Operating Expenses (OpEx) - ~15% of revenue
    monthly_is['OpEx (Marketing & Admin)'] = monthly_is['revenue'] * 0.15
    monthly_is['Payroll'] = monthly_is['revenue'] * 0.10
    monthly_is['Rent & Utilities'] = 5000 # Fixed
    
    monthly_is['Total Expenses'] = monthly_is['OpEx (Marketing & Admin)'] + monthly_is['Payroll'] + monthly_is['Rent & Utilities']
    monthly_is['Net Income'] = monthly_is['Gross Profit'] - monthly_is['Total Expenses']
    
    # Calculate Margins
    monthly_is['Gross Margin %'] = (monthly_is['Gross Profit'] / monthly_is['revenue']) * 100
    monthly_is['Net Margin %'] = (monthly_is['Net Income'] / monthly_is['revenue']) * 100
    
    return monthly_is

def calculate_retail_ratios(sales_df, inv_df, income_statement):
    """Calculate key retail performance ratios"""
    
    # 1. GMROI (Gross Margin Return on Investment)
    total_gp = income_statement['Gross Profit'].sum()
    avg_inventory_cost = inv_df['inventory_value'].mean()
    gmroi = total_gp / avg_inventory_cost if avg_inventory_cost > 0 else 0
    
    # 2. Inventory Turnover
    total_cogs = income_statement['COGS'].sum()
    inv_turnover = total_cogs / avg_inventory_cost if avg_inventory_cost > 0 else 0
    
    # 3. Liquidity - Current Ratio (Simulated Assets/Liabilities)
    total_assets = avg_inventory_cost + (income_statement['revenue'].sum() * 0.2) # Stock + Cash/AR
    total_liabs = total_cogs * 0.3 # Accounts Payable
    current_ratio = total_assets / total_liabs if total_liabs > 0 else 0
    
    ratios = {
        'Ratio': ['GMROI', 'Inventory Turnover', 'Current Ratio', 'Avg Gross Margin %', 'Avg Net Margin %'],
        'Value': [gmroi, inv_turnover, current_ratio, income_statement['Gross Margin %'].mean(), income_statement['Net Margin %'].mean()],
        'Benchmark': [2.5, 4.0, 2.0, 40.0, 10.0],
        'Status': [
            'Good' if gmroi > 2.5 else 'Underperform',
            'Good' if inv_turnover > 4 else 'Slow',
            'Healthy' if current_ratio > 1.5 else 'Critical',
            'Good' if income_statement['Gross Margin %'].mean() > 40 else 'Low',
            'Good' if income_statement['Net Margin %'].mean() > 5 else 'Review'
        ]
    }
    
    return pd.DataFrame(ratios)

def export_to_excel(income_statement, ratios_df):
    """Export data to a professional, formatted Excel report"""
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, 'retail_financial_report.xlsx')
    
    # Using xlsxwriter for formatting
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    
    # 1. Income Statement Sheet
    is_formatted = income_statement.copy()
    is_formatted.index = is_formatted.index.astype(str)
    is_formatted.to_excel(writer, sheet_name='Income Statement')
    
    # 2. Ratios Sheet
    ratios_df.to_excel(writer, sheet_name='Financial Ratios', index=False)
    
    workbook  = writer.book
    
    # Formatting styles
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
    currency_fmt = workbook.add_format({'num_format': '$#,##0.00'})
    percent_fmt = workbook.add_format({'num_format': '0.00"%"'})
    
    # Apply to Income Statement
    worksheet = writer.sheets['Income Statement']
    worksheet.set_column('B:I', 15, currency_fmt)
    worksheet.set_column('I:J', 15, percent_fmt)
    
    # Apply to Ratios
    worksheet_r = writer.sheets['Financial Ratios']
    worksheet_r.set_column('B:C', 15)
    
    writer.close()
    return file_path

def main():
    print("💰 Initializing Retail Financial Engine...")
    
    sales, inventory = load_source_data()
    if sales is None:
        return
        
    print("📊 Generating Income Statement...")
    income_statement = generate_income_statement(sales)
    
    print("🔢 Calculating Retail Ratios...")
    ratios_df = calculate_retail_ratios(sales, inventory, income_statement)
    
    print("📗 Exporting Formatted Excel Report...")
    excel_path = export_to_excel(income_statement, ratios_df)
    
    print(f"\n✨ Financial analysis complete!")
    print(f"✅ Excel Report saved to: {excel_path}")
    print("\n--- Key Metrics ---")
    print(ratios_df[['Ratio', 'Value', 'Status']].to_string(index=False))

if __name__ == '__main__':
    main()
