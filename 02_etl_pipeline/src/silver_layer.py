"""
Silver Layer - Data Cleansing and Standardization
Cleans, validates, and standardizes Bronze data.
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


def check_nulls(df: pd.DataFrame) -> dict:
    """Check for null values in each column."""
    null_counts = df.isnull().sum()
    null_pct = (null_counts / len(df)) * 100
    return {col: {'count': int(null_counts[col]), 'percent': round(null_pct[col], 2)} 
            for col in df.columns if null_counts[col] > 0}


def check_duplicates(df: pd.DataFrame, key_columns: list) -> dict:
    """Check for duplicate records."""
    if not key_columns:
        return {'duplicates': 0}
    
    dup_count = df.duplicated(subset=key_columns, keep=False).sum()
    return {'duplicates': int(dup_count), 'percent': round((dup_count / len(df)) * 100, 2)}


def deduplicate(df: pd.DataFrame, key_columns: list) -> pd.DataFrame:
    """Remove duplicate records keeping the first occurrence."""
    original = len(df)
    df = df.drop_duplicates(subset=key_columns, keep='first')
    removed = original - len(df)
    if removed > 0:
        print(f"   🔄 Removed {removed} duplicates")
    return df


def standardize_dates(df: pd.DataFrame, date_columns: list) -> pd.DataFrame:
    """Standardize date columns to consistent format."""
    df = df.copy()
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df


def flag_quality_issues(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Add quality flag columns for issues."""
    df = df.copy()
    
    # Flag null values
    df['has_null_values'] = df.isnull().any(axis=1)
    
    # Flag KPI range violations
    kpi_ranges = config.get('quality_checks', {}).get('kpi_ranges', {})
    for col, ranges in kpi_ranges.items():
        if col in df.columns:
            df[f'{col}_out_of_range'] = (df[col] < ranges['min']) | (df[col] > ranges['max'])
    
    return df


def process_silver_table(bronze_path: str, table_name: str, config: dict) -> pd.DataFrame:
    """Process a Bronze table into Silver."""
    print(f"\n📄 Processing: {table_name}")
    
    # Read Bronze data
    bronze_file = os.path.join(bronze_path, f'{table_name}_bronze.parquet')
    if not os.path.exists(bronze_file):
        print(f"   ⚠️ File not found: {bronze_file}")
        return None
    
    df = pd.read_parquet(bronze_file)
    print(f"   📊 Input records: {len(df)}")
    
    # Check quality
    null_report = check_nulls(df)
    if null_report:
        print(f"   ⚠️ Null values found: {null_report}")
    
    # Deduplicate
    silver_config = config.get('silver', {})
    if silver_config.get('deduplication') and silver_config.get('dedup_columns'):
        valid_cols = [c for c in silver_config['dedup_columns'] if c in df.columns]
        if valid_cols:
            df = deduplicate(df, valid_cols)
    
    # Standardize dates
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    df = standardize_dates(df, date_cols)
    
    # Flag quality issues
    df = flag_quality_issues(df, config)
    
    # Add processing metadata
    df['silver_processed_at'] = datetime.now()
    
    print(f"   ✅ Output records: {len(df)}")
    return df


def save_silver(df: pd.DataFrame, output_path: str, table_name: str):
    """Save Silver layer data as Parquet."""
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, f'{table_name}_silver.parquet')
    df.to_parquet(output_file, index=False)
    print(f"   💾 Saved: {output_file}")


def run_silver_pipeline():
    """Execute Silver layer pipeline."""
    config = load_config()
    
    print("\n⚪ SILVER LAYER PIPELINE")
    print("=" * 50)
    
    bronze_path = os.path.join(os.path.dirname(__file__), '..', config['paths']['bronze_output'])
    silver_output = os.path.join(os.path.dirname(__file__), '..', config['paths']['silver_output'])
    
    # Process each table
    for table_name in ['sales', 'customers', 'telecom']:
        df = process_silver_table(bronze_path, table_name, config)
        if df is not None:
            save_silver(df, silver_output, table_name)
    
    print("\n✅ Silver layer complete!")


if __name__ == '__main__':
    run_silver_pipeline()
