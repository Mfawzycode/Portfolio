"""
Customer Advanced Analytics Script
Implements RFM Segmentation and Cohort Retention Analysis.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_data():
    """Load the advanced customer dataset"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    txns = pd.read_csv(os.path.join(base_dir, 'data', 'customer_transactions.csv'))
    profiles = pd.read_csv(os.path.join(base_dir, 'data', 'customer_profiles.csv'))
    behavior = pd.read_csv(os.path.join(base_dir, 'data', 'behavior_logs.csv'))
    
    txns['date'] = pd.to_datetime(txns['date'])
    return txns, profiles, behavior

def calculate_rfm(df):
    """Perform RFM (Recency, Frequency, Monetary) Analysis"""
    print("🔢 Calculating RFM Scores...")
    
    # Snapshot date (latest date in dataset + 1)
    snapshot_date = df['date'].max() + pd.Timedelta(days=1)
    
    # Aggregate at customer level
    rfm = df.groupby('customer_id').agg({
        'date': lambda x: (snapshot_date - x.max()).days, # Recency
        'transaction_id': 'count',                       # Frequency
        'amount': 'sum'                                  # Monetary
    }).rename(columns={
        'date': 'Recency',
        'transaction_id': 'Frequency',
        'amount': 'Monetary'
    })
    
    # Assign scores (1-5, where 5 is better)
    # Frequency and Monetary: Higher is better -> labels [1,2,3,4,5]
    # Recency: Lower is better -> labels [5,4,3,2,1]
    
    r_labels = [5, 4, 3, 2, 1]
    f_labels = [1, 2, 3, 4, 5]
    m_labels = [1, 2, 3, 4, 5]
    
    rfm['R'] = pd.qcut(rfm['Recency'], q=5, labels=r_labels)
    rfm['F'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=5, labels=f_labels)
    rfm['M'] = pd.qcut(rfm['Monetary'], q=5, labels=m_labels)
    
    # Combined RFM Score
    rfm['RFM_Score'] = rfm[['R', 'F', 'M']].sum(axis=1)
    
    # Define Segments based on R and F scores
    def segment_customer(df):
        r = int(df['R'])
        f = int(df['F'])
        
        if r >= 4 and f >= 4:
            return 'Champions'
        elif r >= 3 and f >= 3:
            return 'Loyal Customers'
        elif r >= 4 and f <= 2:
            return 'Promising (New)'
        elif r <= 2 and f >= 4:
            return 'At Risk (Big Spenders)'
        elif r <= 2 and f <= 2:
            return 'Hibernating'
        else:
            return 'Others'
            
    rfm['Segment'] = rfm.apply(segment_customer, axis=1)
    return rfm

def calculate_cohorts(df):
    """Perform Cohort Analysis (Monthly Retention)"""
    print("📉 Calculating Cohort Matrix...")
    
    # 1. Month of purchase
    df['order_month'] = df['date'].dt.to_period('M')
    
    # 2. Month of first purchase (Cohort)
    df['cohort'] = df.groupby('customer_id')['date'].transform('min').dt.to_period('M')
    
    # 3. Aggregate by cohort and month
    cohort_data = df.groupby(['cohort', 'order_month']).agg(n_customers=('customer_id', 'nunique')).reset_index()
    
    # 4. Period index (Months since first purchase)
    cohort_data['period_number'] = (cohort_data.order_month - cohort_data.cohort).apply(lambda x: x.n)
    
    # 5. Pivot for heatmap
    cohort_pivot = cohort_data.pivot_table(index='cohort', columns='period_number', values='n_customers')
    
    # 6. Convert to percentages
    cohort_size = cohort_pivot.iloc[:, 0]
    retention_matrix = cohort_pivot.divide(cohort_size, axis=0)
    
    return retention_matrix

def main():
    print("🧪 Running Customer Analytics Logic...")
    
    txns, profiles, behavior = load_data()
    
    # 1. RFM
    rfm_df = calculate_rfm(txns)
    
    # 2. Cohorts
    cohort_df = calculate_cohorts(txns)
    
    # Save Outputs
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    rfm_df.to_csv(os.path.join(output_dir, 'customer_segments.csv'))
    cohort_df.to_csv(os.path.join(output_dir, 'cohort_matrix.csv'))
    
    print("\n✅ Analytics complete. Summaries created in 07_customer_analysis/outputs/")
    
    # Peak stats for console
    print("\n📊 Segment Distribution:")
    print(rfm_df['Segment'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%')

if __name__ == '__main__':
    main()
