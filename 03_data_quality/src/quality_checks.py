"""
Data Quality Checks Module
Reusable functions for validating data quality.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional


class DataQualityChecker:
    """Comprehensive data quality checker."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.results = {}
        self.quality_score = 100.0
    
    def check_completeness(self, threshold: float = 0.95) -> Dict[str, Any]:
        """Check for null/missing values."""
        total_cells = len(self.df) * len(self.df.columns)
        null_counts = self.df.isnull().sum()
        total_nulls = null_counts.sum()
        
        completeness = 1 - (total_nulls / total_cells)
        
        result = {
            'check_name': 'Completeness',
            'passed': completeness >= threshold,
            'score': round(completeness * 100, 2),
            'threshold': threshold * 100,
            'total_nulls': int(total_nulls),
            'columns_with_nulls': {
                col: {'count': int(null_counts[col]), 'percent': round(null_counts[col] / len(self.df) * 100, 2)}
                for col in self.df.columns if null_counts[col] > 0
            }
        }
        
        self.results['completeness'] = result
        return result
    
    def check_uniqueness(self, key_columns: List[str]) -> Dict[str, Any]:
        """Check for duplicate records."""
        valid_cols = [c for c in key_columns if c in self.df.columns]
        
        if not valid_cols:
            return {'check_name': 'Uniqueness', 'passed': True, 'message': 'No key columns found'}
        
        total = len(self.df)
        unique = len(self.df.drop_duplicates(subset=valid_cols))
        duplicates = total - unique
        
        result = {
            'check_name': 'Uniqueness',
            'passed': duplicates == 0,
            'score': round((unique / total) * 100, 2),
            'total_records': total,
            'unique_records': unique,
            'duplicate_count': duplicates,
            'key_columns': valid_cols
        }
        
        self.results['uniqueness'] = result
        return result
    
    def check_range(self, column: str, min_val: float, max_val: float) -> Dict[str, Any]:
        """Check if numeric values are within expected range."""
        if column not in self.df.columns:
            return {'check_name': f'Range ({column})', 'passed': False, 'message': 'Column not found'}
        
        col_data = pd.to_numeric(self.df[column], errors='coerce')
        valid = col_data.between(min_val, max_val)
        
        valid_count = valid.sum()
        total_count = len(col_data.dropna())
        
        # Get out-of-range values
        out_of_range = col_data[~valid & col_data.notna()]
        
        result = {
            'check_name': f'Range ({column})',
            'passed': valid_count == total_count,
            'score': round((valid_count / total_count) * 100, 2) if total_count > 0 else 100,
            'column': column,
            'expected_range': {'min': min_val, 'max': max_val},
            'valid_count': int(valid_count),
            'out_of_range_count': len(out_of_range),
            'sample_violations': out_of_range.head(5).tolist() if len(out_of_range) > 0 else []
        }
        
        self.results[f'range_{column}'] = result
        return result
    
    def check_date_format(self, column: str, expected_format: str = '%Y-%m-%d') -> Dict[str, Any]:
        """Validate date format consistency."""
        if column not in self.df.columns:
            return {'check_name': f'Date Format ({column})', 'passed': False, 'message': 'Column not found'}
        
        def is_valid_date(val):
            if pd.isna(val):
                return True
            try:
                if isinstance(val, (datetime, pd.Timestamp)):
                    return True
                datetime.strptime(str(val), expected_format)
                return True
            except:
                return False
        
        valid = self.df[column].apply(is_valid_date)
        valid_count = valid.sum()
        
        result = {
            'check_name': f'Date Format ({column})',
            'passed': valid_count == len(self.df),
            'score': round((valid_count / len(self.df)) * 100, 2),
            'column': column,
            'expected_format': expected_format,
            'valid_count': int(valid_count),
            'invalid_count': int(len(self.df) - valid_count)
        }
        
        self.results[f'date_format_{column}'] = result
        return result
    
    def check_categorical_values(self, column: str, valid_values: List[str]) -> Dict[str, Any]:
        """Check if categorical values are within expected set."""
        if column not in self.df.columns:
            return {'check_name': f'Categorical ({column})', 'passed': False, 'message': 'Column not found'}
        
        actual_values = self.df[column].dropna().unique()
        invalid_values = [v for v in actual_values if v not in valid_values]
        
        result = {
            'check_name': f'Categorical ({column})',
            'passed': len(invalid_values) == 0,
            'column': column,
            'valid_values': valid_values,
            'invalid_values': invalid_values,
            'unique_values_found': len(actual_values)
        }
        
        self.results[f'categorical_{column}'] = result
        return result
    
    def calculate_overall_score(self) -> float:
        """Calculate overall quality score from all checks."""
        scores = []
        for check_name, result in self.results.items():
            if 'score' in result:
                scores.append(result['score'])
        
        self.quality_score = round(np.mean(scores), 2) if scores else 100.0
        return self.quality_score
    
    def run_all_checks(self, config: Dict = None) -> Dict[str, Any]:
        """Run all quality checks with optional configuration."""
        config = config or {}
        
        # Completeness
        self.check_completeness(config.get('completeness_threshold', 0.95))
        
        # Uniqueness
        key_cols = config.get('key_columns', [self.df.columns[0]] if len(self.df.columns) > 0 else [])
        self.check_uniqueness(key_cols)
        
        # Range checks for numeric columns
        for col in self.df.select_dtypes(include=['number']).columns[:5]:  # Check first 5 numeric cols
            col_min = self.df[col].min()
            col_max = self.df[col].max()
            self.check_range(col, col_min, col_max)
        
        # Date format checks
        for col in self.df.columns:
            if 'date' in col.lower():
                self.check_date_format(col)
        
        # Calculate overall score
        self.calculate_overall_score()
        
        return {
            'overall_score': self.quality_score,
            'checks_run': len(self.results),
            'timestamp': datetime.now().isoformat(),
            'total_records': len(self.df),
            'total_columns': len(self.df.columns),
            'results': self.results
        }
    
    def get_summary(self) -> pd.DataFrame:
        """Get summary DataFrame of all check results."""
        summary_data = []
        for check_name, result in self.results.items():
            summary_data.append({
                'Check': result.get('check_name', check_name),
                'Passed': '✅' if result.get('passed', False) else '❌',
                'Score': f"{result.get('score', 'N/A')}%"
            })
        return pd.DataFrame(summary_data)


def run_quality_check(filepath: str) -> Dict[str, Any]:
    """Convenience function to run quality checks on a file."""
    print(f"🔍 Running quality checks on: {filepath}")
    
    # Determine file type and read
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith('.parquet'):
        df = pd.read_parquet(filepath)
    else:
        raise ValueError(f"Unsupported file format: {filepath}")
    
    checker = DataQualityChecker(df)
    results = checker.run_all_checks()
    
    print(f"\n📊 Quality Score: {results['overall_score']}%")
    print(f"   Records checked: {results['total_records']:,}")
    print(f"   Checks performed: {results['checks_run']}")
    
    print("\n📋 Check Summary:")
    print(checker.get_summary().to_string(index=False))
    
    return results


if __name__ == '__main__':
    import os
    
    # Run on sample data
    sample_file = os.path.join(os.path.dirname(__file__), '..', '..', 'shared', 'data', 'sales_with_issues.csv')
    
    if os.path.exists(sample_file):
        results = run_quality_check(sample_file)
    else:
        print("⚠️ Sample data not found. Run shared/generate_all_data.py first.")
