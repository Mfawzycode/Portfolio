import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_ts_data(years=3):
    """Generates 3 years of daily sales data with seasonality and trend"""
    start_date = datetime.now() - timedelta(days=365*years)
    date_rng = pd.date_range(start=start_date, periods=365*years, freq='D')
    
    # 1. Base Trend (Linear growth)
    trend = np.linspace(50, 150, len(date_rng))
    
    # 2. Seasonality (Yearly S-wave)
    # Sin wave peaking in late December (Day 355-360)
    day_of_year = date_rng.dayofyear
    seasonality = 40 * np.sin(2 * np.pi * (day_of_year - 20) / 365.25) + \
                  30 * np.sin(2 * np.pi * (day_of_year - 80) / 365.25) # Secondary peak
    
    # 3. Holiday Spikes (Black Friday / Xmas)
    holidays = np.zeros(len(date_rng))
    # Holiday season (Dec 15-25)
    holidays[(date_rng.month == 12) & (date_rng.day >= 15) & (date_rng.day <= 25)] += 60
    # Black Friday (Approx late Nov)
    holidays[(date_rng.month == 11) & (date_rng.day >= 24) & (date_rng.day <= 28)] += 50
    
    # 4. Noise
    noise = np.random.normal(0, 10, len(date_rng))
    
    sales = trend + seasonality + holidays + noise
    sales = np.maximum(sales, 10) # No negative sales
    
    df = pd.DataFrame({'date': date_rng, 'sales': sales})
    return df

def generate_behavioral_data(n_customers=2000):
    """Generates behavioral features for churn prediction"""
    cust_ids = [f"CUST-{i:04d}" for i in range(1, n_customers + 1)]
    
    data = []
    for cid in cust_ids:
        # Features
        tenure_days = np.random.randint(30, 1000)
        avg_spend = np.random.uniform(50, 500)
        login_freq_last_30d = np.random.randint(0, 31)
        support_tickets_30d = np.random.randint(0, 5)
        
        # Target: Real churn logic
        # High risk if low logins and high support tickets or high spend but zero recent activity
        risk_score = 0.3
        if login_freq_last_30d < 5: risk_score += 0.4
        if support_tickets_30d > 2: risk_score += 0.2
        
        churn_target = 1 if risk_score + np.random.normal(0, 0.1) > 0.6 else 0
        
        data.append({
            'customer_id': cid,
            'tenure_days': tenure_days,
            'avg_monthly_spend': avg_spend,
            'logins_30d': login_freq_last_30d,
            'support_tickets_30d': support_tickets_30d,
            'churned': churn_target
        })
        
    return pd.DataFrame(data)

def main():
    print("🚀 Generating Predictive Analytics dataset...")
    
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate Time Series
    ts_df = generate_ts_data()
    ts_df.to_csv(os.path.join(output_dir, 'sales_history.csv'), index=False)
    print(f"📊 Created 'sales_history.csv' with {len(ts_df)} days of history.")
    
    # Generate Behavioral
    beh_df = generate_behavioral_data()
    beh_df.to_csv(os.path.join(output_dir, 'customer_behavior_risk.csv'), index=False)
    print(f"🔄 Created 'customer_behavior_risk.csv' for {len(beh_df)} customers.")
    
    print("\n✨ Data generation complete.")

if __name__ == '__main__':
    main()
