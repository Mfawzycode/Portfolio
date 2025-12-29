import pandas as pd
import sqlite3
import os
import random

def generate_knowledge_base():
    """Generates a rich knowledge base for RAG demonstration"""
    data = [
        # Finance
        {"topic": "Revenue Growth", "category": "Finance", "content": "Q3 Revenue grew by 15% due to increased digital sales.", "value": 15, "metric": "growth_rate"},
        {"topic": "Operating Costs", "category": "Finance", "content": "Operating costs were reduced by 5% through cloud migration.", "value": 5, "metric": "cost_reduction"},
        # Inventory
        {"topic": "Stockout Trends", "category": "Inventory", "content": "Critical stockouts occurred in the electronics category during November.", "value": 12, "metric": "stockout_count"},
        {"topic": "Turnover Efficiency", "category": "Inventory", "content": "Average inventory turnover improved to 8.2x in 2024.", "value": 8.2, "metric": "turnover_ratio"},
        # Customer
        {"topic": "Churn Risk", "category": "Customer", "content": "Churn risk is highest among users with less than 2 logins per month.", "value": 0.72, "metric": "risk_score"},
        {"topic": "Loyalty Growth", "category": "Customer", "content": "The 'Champions' segment increased by 400 members this quarter.", "value": 400, "metric": "member_count"},
        # Healthcare
        {"topic": "Readmission Benchmark", "category": "Clinical", "content": "Cardiology readmission rate stands at 24.5%, requiring intervention.", "value": 24.5, "metric": "readmission_rate"},
        {"topic": "Patient Satisfaction", "category": "Clinical", "content": "Patient satisfaction improved to 4.5/5 after implementing digital intake.", "value": 4.5, "metric": "satisfaction_score"}
    ]
    
    return pd.DataFrame(data)

def seed_database(df):
    """Seeds a SQLite database for SQL-based RAG demonstration"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_path, 'data', 'warehouse.db')
    
    conn = sqlite3.connect(db_path)
    df.to_sql('knowledge_base', conn, if_exists='replace', index=False)
    conn.close()
    print(f"✅ Seeded SQLite database at {db_path}")

def main():
    print("🛠️ Preparing AI RAG Knowledge Base...")
    
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_path, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    df = generate_knowledge_base()
    
    # Save CSV
    csv_path = os.path.join(data_dir, 'knowledge_base.csv')
    df.to_csv(csv_path, index=False)
    print(f"✅ Created CSV knowledge base at {csv_path}")
    
    # Seed SQL
    seed_database(df)
    
    print("\n✨ RAG Data Seeding Complete!")

if __name__ == '__main__':
    main()
