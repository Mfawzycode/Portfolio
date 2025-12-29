"""
Clinical Analytics Engine
Advanced analysis of healthcare operations, focusing on readmission rates,
operational bottlenecks, and clinical outcomes.
"""

import pandas as pd
import numpy as np
import os

def load_data():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'patient_visits.csv')
    
    if not os.path.exists(data_path):
        print(f"❌ Error: {data_path} not found.")
        return None
        
    df = pd.read_csv(data_path)
    df['visit_date'] = pd.to_datetime(df['visit_date'])
    return df

def analyze_readmissions(df):
    """Deep dive into readmission patterns by department"""
    readmission_stats = df.groupby('department').agg({
        'is_readmission': ['sum', 'count']
    }).reset_index()
    
    readmission_stats.columns = ['department', 'readmissions', 'total_visits']
    readmission_stats['readmission_rate'] = (readmission_stats['readmissions'] / readmission_stats['total_visits'] * 100).round(2)
    
    return readmission_stats.sort_values('readmission_rate', ascending=False)

def analyze_operational_efficiency(df):
    """Correlation between wait times, severity, and satisfaction"""
    # Filter completed visits for quality analysis
    completed = df[df['status'] == 'Completed'].copy()
    
    efficiency = completed.groupby('department').agg({
        'wait_time_minutes': 'mean',
        'severity_level': 'mean',
        'satisfaction_score': 'mean',
        'outcome_score': 'mean'
    }).reset_index()
    
    # Treatment Efficiency Index (Lower is better: High severity handled with low wait time and good outcome)
    # Scaled metric: (Wait Time / Severity) * Outcome
    efficiency['efficiency_index'] = (
        (efficiency['wait_time_minutes'] / efficiency['severity_level']) * (6 - efficiency['outcome_score'])
    ).round(2)
    
    return efficiency

def main():
    print("🏥 Running Clinical Intelligence Engine...")
    df = load_data()
    if df is None: return
    
    readmissions = analyze_readmissions(df)
    efficiency = analyze_operational_efficiency(df)
    
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    readmissions.to_csv(os.path.join(output_dir, 'readmission_analysis.csv'), index=False)
    efficiency.to_csv(os.path.join(output_dir, 'clinical_efficiency.csv'), index=False)
    
    print("✅ Clinical analytics complete. Saved to 'outputs/'")
    print("\n--- High Risk Readmission Depts ---")
    print(readmissions.head(3))
    
    print("\n--- Most Efficient Depts ---")
    print(efficiency.sort_values('efficiency_index').head(3))

if __name__ == '__main__':
    main()
