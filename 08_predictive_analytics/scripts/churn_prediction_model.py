"""
Churn Prediction Model
Analyzes customer behavior metrics to predict churn probability.
Outputs risk scores for proactive retention.
"""

import pandas as pd
import numpy as np
import os

def load_data():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'customer_behavior_risk.csv')
    
    if not os.path.exists(data_path):
        print(f"❌ Error: {data_path} not found.")
        return None
        
    return pd.read_csv(data_path)

def predict_churn(df):
    """Calculates a Churn Risk Score normalized between 0 and 1"""
    # Feature weighting (simulating a trained model)
    df['risk_score'] = (
        (1 - (df['logins_30d'] / 30)) * 0.5 + # Low logins is bad
        (df['support_tickets_30d'] / 5) * 0.3 + # High tickets is bad
        (1 - (df['tenure_days'] / 1000).clip(0, 1)) * 0.2 # New customers are riskier
    )
    
    # Scale to 0-1
    df['risk_score'] = df['risk_score'].clip(0, 1)
    
    # Segment Risky Customers
    df['risk_tier'] = pd.cut(df['risk_score'], 
                             bins=[0, 0.4, 0.7, 1.0], 
                             labels=['Low', 'Medium', 'High'])
    
    return df

def main():
    print("🔄 Running Churn Prediction Model...")
    df = load_data()
    if df is None: return
    
    results = predict_churn(df)
    
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    results.to_csv(os.path.join(output_dir, 'customer_risk_scores.csv'), index=False)
    print(f"✅ Prediction complete. Saved to 'outputs/customer_risk_scores.csv'")
    
    risk_summary = results['risk_tier'].value_counts()
    print("\n--- Risk Distribution ---")
    print(risk_summary)

if __name__ == '__main__':
    main()
