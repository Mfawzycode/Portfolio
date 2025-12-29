"""
Gold Layer - Business Aggregations
Creates business-level aggregations and KPIs.
"""

import pandas as pd
import os
import yaml
from datetime import datetime


def load_config():
    """Load pipeline configuration."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'pipeline_config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def aggregate_daily_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Create daily revenue aggregation."""
    # Ensure date is datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    agg_df = df.groupby(['date', 'region']).agg({
        'revenue': 'sum',
        'profit': 'sum',
        'transaction_id': 'count',
        'customer_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    
    agg_df.columns = ['date', 'region', 'total_revenue', 'total_profit', 
                      'transaction_count', 'unique_customers', 'total_quantity']
    
    # Add derived metrics
    agg_df['avg_order_value'] = agg_df['total_revenue'] / agg_df['transaction_count']
    agg_df['profit_margin'] = (agg_df['total_profit'] / agg_df['total_revenue']) * 100
    
    return agg_df


def aggregate_category_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Create category-level performance metrics."""
    agg_df = df.groupby('product_category').agg({
        'revenue': 'sum',
        'profit': 'sum',
        'unit_price': 'mean',
        'quantity': 'sum',
        'transaction_id': 'count',
        'customer_id': 'nunique'
    }).reset_index()
    
    agg_df.columns = ['product_category', 'total_revenue', 'total_profit',
                      'avg_unit_price', 'total_quantity', 'transaction_count', 'unique_customers']
    
    # Rank categories
    agg_df['revenue_rank'] = agg_df['total_revenue'].rank(ascending=False)
    
    return agg_df.sort_values('total_revenue', ascending=False)


def aggregate_customer_segment(df: pd.DataFrame) -> pd.DataFrame:
    """Create customer segment metrics."""
    agg_df = df.groupby('customer_segment').agg({
        'revenue': 'sum',
        'profit': 'sum',
        'transaction_id': 'count',
        'customer_id': 'nunique',
        'discount_percent': 'mean'
    }).reset_index()
    
    agg_df.columns = ['customer_segment', 'total_revenue', 'total_profit',
                      'transaction_count', 'unique_customers', 'avg_discount']
    
    agg_df['revenue_per_customer'] = agg_df['total_revenue'] / agg_df['unique_customers']
    
    return agg_df


def aggregate_telecom_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Create telecom KPI aggregations by region and technology."""
    agg_df = df.groupby(['region', 'technology']).agg({
        'availability_percent': 'mean',
        'latency_ms': 'mean',
        'throughput_mbps': 'mean',
        'call_drop_rate': 'mean',
        'handover_success_rate': 'mean',
        'traffic_volume_gb': 'sum',
        'active_users': 'sum',
        'record_id': 'count'
    }).reset_index()
    
    agg_df.columns = ['region', 'technology', 'avg_availability', 'avg_latency',
                      'avg_throughput', 'avg_call_drop_rate', 'avg_handover_success',
                      'total_traffic_gb', 'total_active_users', 'record_count']
    
    return agg_df


def save_gold(df: pd.DataFrame, output_path: str, table_name: str):
    """Save Gold layer data."""
    os.makedirs(output_path, exist_ok=True)
    
    # Save as Parquet
    parquet_file = os.path.join(output_path, f'{table_name}_gold.parquet')
    df.to_parquet(parquet_file, index=False)
    
    # Also save as CSV for Power BI
    csv_file = os.path.join(output_path, f'{table_name}_gold.csv')
    df.to_csv(csv_file, index=False)
    
    print(f"   💾 Saved: {table_name} ({len(df)} records)")


def run_gold_pipeline():
    """Execute Gold layer pipeline."""
    config = load_config()
    
    print("\n🟡 GOLD LAYER PIPELINE")
    print("=" * 50)
    
    silver_path = os.path.join(os.path.dirname(__file__), '..', config['paths']['silver_output'])
    gold_output = os.path.join(os.path.dirname(__file__), '..', config['paths']['gold_output'])
    
    # Process Sales aggregations
    sales_file = os.path.join(silver_path, 'sales_silver.parquet')
    if os.path.exists(sales_file):
        print("\n📊 Creating Sales Aggregations...")
        sales_df = pd.read_parquet(sales_file)
        
        daily_revenue = aggregate_daily_revenue(sales_df)
        save_gold(daily_revenue, gold_output, 'daily_revenue')
        
        category_perf = aggregate_category_performance(sales_df)
        save_gold(category_perf, gold_output, 'category_performance')
        
        segment_metrics = aggregate_customer_segment(sales_df)
        save_gold(segment_metrics, gold_output, 'customer_segments')
    
    # Process Telecom aggregations
    telecom_file = os.path.join(silver_path, 'telecom_silver.parquet')
    if os.path.exists(telecom_file):
        print("\n📡 Creating Telecom Aggregations...")
        telecom_df = pd.read_parquet(telecom_file)
        
        telecom_kpis = aggregate_telecom_kpis(telecom_df)
        save_gold(telecom_kpis, gold_output, 'telecom_regional_kpis')
    
    print("\n✅ Gold layer complete!")


if __name__ == '__main__':
    run_gold_pipeline()
