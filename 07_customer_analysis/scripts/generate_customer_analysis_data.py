"""
Advanced Customer Data Generator
Creates high-fidelity behavioral and transactional data for Senior Data Science analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_customer_profiles(num_customers=5000):
    """Generate detailed customer demographics and behavioral traits"""
    sources = ['Search', 'Social Media', 'Referral', 'Direct', 'Email']
    tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']
    
    data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(num_customers):
        customer_id = f'C-ADV-{i+1:05d}'
        join_date = start_date + timedelta(days=random.randint(0, 365))
        
        # User Persona Factors
        loyalty_factor = np.random.beta(2, 5) # Most are not super loyal
        spend_power = np.random.lognormal(mean=4, sigma=1) # Log-normal spending
        
        data.append({
            'customer_id': customer_id,
            'join_date': join_date,
            'acquisition_channel': random.choice(sources),
            'age': random.randint(18, 70),
            'loyalty_score': round(loyalty_factor, 2),
            'spend_potential': round(spend_power, 2),
            'tier': random.choice(tiers),
            'is_active': random.choice([True, True, True, False]) # 25% inactive
        })
    
    return pd.DataFrame(data)

def generate_transactions(customers_df, num_txns=25000):
    """Generate transactional history based on loyalty and spend power"""
    txns = []
    end_date = datetime(2024, 12, 31)
    
    for _, cust in customers_df.iterrows():
        # Number of transactions depends on loyalty
        num_c_txns = int(cust['loyalty_score'] * 50) + random.randint(1, 5)
        
        for _ in range(num_c_txns):
            txn_date = cust['join_date'] + timedelta(days=random.randint(0, (end_date - cust['join_date']).days))
            if txn_date > end_date: continue
            
            # Amount depends on spend_potential
            amount = cust['spend_potential'] * random.uniform(0.5, 2.0)
            
            txns.append({
                'transaction_id': f'T-ADV-{len(txns)+1:06d}',
                'customer_id': cust['customer_id'],
                'date': txn_date,
                'amount': round(amount, 2),
                'category': random.choice(['Grocery', 'Tech', 'Fashion', 'Home', 'Health'])
            })
            
    df = pd.DataFrame(txns)
    return df.sort_values('date').reset_index(drop=True)

def generate_behavior_logs(customers_df):
    """Generate session frequency and app usage logs"""
    logs = []
    for _, cust in customers_df.iterrows():
        # High fidelity sessions
        avg_sessions_per_month = random.randint(1, 20)
        total_sessions = avg_sessions_per_month * 12 # Roughly a year
        
        logs.append({
            'customer_id': cust['customer_id'],
            'avg_session_duration': random.uniform(2, 45),
            'bounce_rate': random.uniform(0.1, 0.6),
            'last_login': datetime(2024, 12, 31) - timedelta(days=random.randint(0, 180))
        })
    return pd.DataFrame(logs)

def main():
    print("🚀 Generating high-fidelity customer analysis data...")
    
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # 1. Profiles
    profiles = generate_customer_profiles(3000)
    profiles.to_csv(os.path.join(data_dir, 'customer_profiles.csv'), index=False)
    print(f"   ✅ {len(profiles)} Customer Profiles created")
    
    # 2. Transactions
    transactions = generate_transactions(profiles)
    transactions.to_csv(os.path.join(data_dir, 'customer_transactions.csv'), index=False)
    print(f"   ✅ {len(transactions)} Transaction Records created")
    
    # 3. Behavior
    behavior = generate_behavior_logs(profiles)
    behavior.to_csv(os.path.join(data_dir, 'behavior_logs.csv'), index=False)
    print(f"   ✅ Behavioral data logged")
    
    print("\n✨ Data generation for Senior Customer Analysis complete!")
    print(f"   Location: {data_dir}")

if __name__ == '__main__':
    main()
