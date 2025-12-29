"""
Bronze Layer - Raw Data Ingestion
Ingests raw data and adds metadata for tracking.
"""

import pandas as pd
import hashlib
import os
from datetime import datetime
import yaml


def load_config():
    """Load pipeline configuration."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'pipeline_config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def generate_record_hash(row: pd.Series) -> str:
    """Generate a unique hash for each record."""
    row_str = '|'.join(str(v) for v in row.values)
    return hashlib.md5(row_str.encode()).hexdigest()


def add_metadata(df: pd.DataFrame, source_file: str) -> pd.DataFrame:
    """Add ingestion metadata to DataFrame."""
    df = df.copy()
    df['ingestion_timestamp'] = datetime.now()
    df['source_file'] = source_file
    df['record_hash'] = df.apply(generate_record_hash, axis=1)
    return df


def ingest_raw_file(filepath: str) -> pd.DataFrame:
    """Ingest a raw CSV file into Bronze layer."""
    print(f"📥 Ingesting: {filepath}")
    
    # Read raw data
    df = pd.read_csv(filepath)
    original_count = len(df)
    
    # Add metadata
    filename = os.path.basename(filepath)
    df = add_metadata(df, filename)
    
    print(f"   ✅ {original_count} records ingested")
    return df


def save_bronze(df: pd.DataFrame, output_path: str, table_name: str):
    """Save Bronze layer data as Parquet."""
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, f'{table_name}_bronze.parquet')
    df.to_parquet(output_file, index=False)
    print(f"   💾 Saved: {output_file}")
    return output_file


def run_bronze_pipeline():
    """Execute Bronze layer pipeline."""
    config = load_config()
    
    print("\n🟤 BRONZE LAYER PIPELINE")
    print("=" * 50)
    
    raw_data_path = os.path.join(os.path.dirname(__file__), '..', config['paths']['raw_data'])
    bronze_output = os.path.join(os.path.dirname(__file__), '..', config['paths']['bronze_output'])
    
    # Process sales data
    sales_file = os.path.join(raw_data_path, 'sales_transactions.csv')
    if os.path.exists(sales_file):
        sales_df = ingest_raw_file(sales_file)
        save_bronze(sales_df, bronze_output, 'sales')
    
    # Process customer data
    customer_file = os.path.join(raw_data_path, 'customers.csv')
    if os.path.exists(customer_file):
        customer_df = ingest_raw_file(customer_file)
        save_bronze(customer_df, bronze_output, 'customers')
    
    # Process telecom data
    telecom_file = os.path.join(raw_data_path, 'telecom_kpis.csv')
    if os.path.exists(telecom_file):
        telecom_df = ingest_raw_file(telecom_file)
        save_bronze(telecom_df, bronze_output, 'telecom')
    
    print("\n✅ Bronze layer complete!")


if __name__ == '__main__':
    run_bronze_pipeline()
