"""
Data Quality Web Application
Interactive dashboard for data validation and quality checks.
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import json
from datetime import datetime

app = Flask(__name__)

# Data paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def get_available_datasets():
    """List available datasets for quality checks."""
    datasets = []
    for layer in ['bronze', 'silver', 'gold']:
        layer_path = os.path.join(DATA_DIR, layer)
        if os.path.exists(layer_path):
            for f in os.listdir(layer_path):
                if f.endswith('.parquet'):
                    datasets.append({
                        'name': f.replace('.parquet', ''),
                        'layer': layer,
                        'path': os.path.join(layer_path, f)
                    })
    return datasets


def run_quality_checks(df: pd.DataFrame) -> dict:
    """Run comprehensive data quality checks."""
    total_rows = len(df)
    total_cols = len(df.columns)
    
    # Completeness check
    null_counts = df.isnull().sum()
    completeness = {
        'total_nulls': int(null_counts.sum()),
        'completeness_score': round((1 - null_counts.sum() / (total_rows * total_cols)) * 100, 2),
        'columns_with_nulls': {col: int(null_counts[col]) for col in df.columns if null_counts[col] > 0}
    }
    
    # Uniqueness check
    unique_counts = df.nunique()
    uniqueness = {
        col: {
            'unique_values': int(unique_counts[col]),
            'uniqueness_ratio': round(unique_counts[col] / total_rows * 100, 2)
        }
        for col in df.columns
    }
    
    # Data types
    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
    
    # Numeric column statistics
    numeric_cols = df.select_dtypes(include=['number']).columns
    numeric_stats = {}
    for col in numeric_cols:
        numeric_stats[col] = {
            'min': float(df[col].min()) if pd.notna(df[col].min()) else None,
            'max': float(df[col].max()) if pd.notna(df[col].max()) else None,
            'mean': round(float(df[col].mean()), 2) if pd.notna(df[col].mean()) else None,
            'std': round(float(df[col].std()), 2) if pd.notna(df[col].std()) else None
        }
    
    # Calculate overall quality score
    quality_score = completeness['completeness_score']
    
    return {
        'summary': {
            'total_rows': total_rows,
            'total_columns': total_cols,
            'quality_score': quality_score,
            'check_timestamp': datetime.now().isoformat()
        },
        'completeness': completeness,
        'uniqueness': uniqueness,
        'data_types': dtypes,
        'numeric_statistics': numeric_stats
    }


@app.route('/')
def dashboard():
    """Main dashboard page."""
    datasets = get_available_datasets()
    return render_template('dashboard.html', datasets=datasets)


@app.route('/api/datasets')
def api_datasets():
    """API endpoint to list datasets."""
    return jsonify(get_available_datasets())


@app.route('/api/quality-check/<layer>/<dataset>')
def api_quality_check(layer, dataset):
    """API endpoint to run quality checks on a dataset."""
    try:
        filepath = os.path.join(DATA_DIR, layer, f'{dataset}.parquet')
        if not os.path.exists(filepath):
            return jsonify({'error': 'Dataset not found'}), 404
        
        df = pd.read_parquet(filepath)
        results = run_quality_checks(df)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sample/<layer>/<dataset>')
def api_sample(layer, dataset):
    """API endpoint to get sample data."""
    try:
        filepath = os.path.join(DATA_DIR, layer, f'{dataset}.parquet')
        if not os.path.exists(filepath):
            return jsonify({'error': 'Dataset not found'}), 404
        
        df = pd.read_parquet(filepath)
        sample = df.head(10).to_dict(orient='records')
        return jsonify({'sample': sample, 'columns': list(df.columns)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("🌐 Starting Data Quality Web App...")
    print("   Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
