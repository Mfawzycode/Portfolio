"""
Healthcare Data Generator
Creates synthetic healthcare visit datasets for analysis demonstration.
All data is 100% synthetic - no real patient information.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# Configuration
DEPARTMENTS = ['General Medicine', 'Cardiology', 'Orthopedics', 'Pediatrics', 'Dermatology', 'Ophthalmology', 'Neurology']
VISIT_TYPES = ['New Patient', 'Follow-up', 'Routine Checkup', 'Emergency', 'Specialist Referral']
INSURANCE_TYPES = ['Private', 'Medicare', 'Medicaid', 'Self-Pay', 'Corporate']
VISIT_STATUS = ['Completed', 'No-Show', 'Cancelled', 'Rescheduled']


def generate_patients(num_patients: int = 1000) -> pd.DataFrame:
    """Generate synthetic patient data."""
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'James', 'Emma', 'Robert', 'Olivia',
                   'Ahmed', 'Fatima', 'Mohammed', 'Aisha', 'Omar', 'Layla', 'Hassan', 'Maryam']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                  'Khan', 'Ali', 'Hassan', 'Ahmed', 'Ibrahim', 'Rahman']
    
    data = []
    for i in range(num_patients):
        birth_year = random.randint(1940, 2020)
        age = 2024 - birth_year
        
        data.append({
            'patient_id': f'PAT-{i+1:06d}',
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'date_of_birth': datetime(birth_year, random.randint(1, 12), random.randint(1, 28)),
            'age': age,
            'gender': random.choice(['Male', 'Female']),
            'insurance_type': random.choice(INSURANCE_TYPES),
            'primary_phone': f'555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
            'city': random.choice(['Dubai', 'Abu Dhabi', 'Sharjah', 'Ajman', 'Al Ain']),
            'registration_date': datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1400)),
            'chronic_conditions': random.randint(0, 3)
        })
    
    return pd.DataFrame(data)


def generate_providers(num_providers: int = 50) -> pd.DataFrame:
    """Generate synthetic healthcare provider data."""
    specialties = DEPARTMENTS
    
    data = []
    for i in range(num_providers):
        data.append({
            'provider_id': f'DOC-{i+1:04d}',
            'provider_name': f'Dr. {random.choice(["Smith", "Johnson", "Ali", "Khan", "Ahmed", "Williams", "Garcia"])}',
            'specialty': random.choice(specialties),
            'years_experience': random.randint(2, 30),
            'daily_capacity': random.randint(15, 30),
            'rating': round(random.uniform(3.5, 5.0), 1)
        })
    
    return pd.DataFrame(data)


def generate_visits(patients_df: pd.DataFrame, providers_df: pd.DataFrame, 
                    year: int = 2024, num_visits: int = 10000) -> pd.DataFrame:
    """Generate synthetic patient visit data."""
    start_date = datetime(year, 1, 1)
    
    data = []
    for i in range(num_visits):
        patient = patients_df.sample(1).iloc[0]
        provider = providers_df.sample(1).iloc[0]
        
        # Visit date and time
        visit_date = start_date + timedelta(days=random.randint(0, 364))
        # Higher probability of visits during business hours
        hour = random.choices(range(8, 18), weights=[1, 2, 3, 3, 3, 2, 1, 3, 3, 2])[0]
        minute = random.choice([0, 15, 30, 45])
        
        # Status with realistic distribution
        status = random.choices(VISIT_STATUS, weights=[0.80, 0.10, 0.07, 0.03])[0]
        
        # Wait time (only for completed visits)
        if status == 'Completed':
            wait_time = int(np.random.exponential(20)) + 5  # Average ~25 min
            visit_duration = random.randint(10, 45)
            satisfaction = random.choices([1, 2, 3, 4, 5], weights=[0.02, 0.05, 0.15, 0.40, 0.38])[0]
        else:
            wait_time = None
            visit_duration = None
            satisfaction = None
        
        data.append({
            'visit_id': f'VIS-{i+1:07d}',
            'patient_id': patient['patient_id'],
            'provider_id': provider['provider_id'],
            'department': provider['specialty'],
            'visit_date': visit_date,
            'scheduled_time': f'{hour:02d}:{minute:02d}',
            'visit_type': random.choice(VISIT_TYPES),
            'status': status,
            'wait_time_minutes': wait_time,
            'visit_duration_minutes': visit_duration,
            'satisfaction_score': satisfaction,
            'insurance_type': patient['insurance_type'],
            'is_new_patient': 1 if random.random() < 0.2 else 0,
            'follow_up_required': 1 if random.random() < 0.3 else 0
        })
    
    df = pd.DataFrame(data)
    df['visit_date'] = pd.to_datetime(df['visit_date'])
    df['day_of_week'] = df['visit_date'].dt.day_name()
    df['month'] = df['visit_date'].dt.month
    df['hour'] = df['scheduled_time'].str.split(':').str[0].astype(int)
    
    return df.sort_values('visit_date').reset_index(drop=True)


def calculate_healthcare_kpis(visits_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate healthcare KPIs by month."""
    monthly = visits_df.groupby('month').agg({
        'visit_id': 'count',
        'wait_time_minutes': 'mean',
        'satisfaction_score': 'mean',
        'is_new_patient': 'sum',
        'follow_up_required': 'sum'
    }).reset_index()
    
    # Calculate no-show rate
    status_counts = visits_df.groupby(['month', 'status']).size().unstack(fill_value=0)
    if 'No-Show' in status_counts.columns:
        monthly['no_show_rate'] = round((status_counts['No-Show'] / status_counts.sum(axis=1) * 100).values, 2)
    else:
        monthly['no_show_rate'] = 0
    
    # Completed visits
    completed = visits_df[visits_df['status'] == 'Completed'].groupby('month').size()
    monthly['completed_visits'] = completed.values
    
    monthly.columns = ['month', 'total_appointments', 'avg_wait_time', 'avg_satisfaction', 
                       'new_patients', 'follow_ups_scheduled', 'no_show_rate', 'completed_visits']
    
    monthly['completion_rate'] = round((monthly['completed_visits'] / monthly['total_appointments']) * 100, 2)
    
    return monthly


def main():
    """Generate all healthcare datasets."""
    print("🏥 Generating Healthcare Data...\n")
    
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate data
    patients_df = generate_patients(1000)
    providers_df = generate_providers(50)
    visits_df = generate_visits(patients_df, providers_df, num_visits=10000)
    
    # Save datasets
    patients_df.to_csv(os.path.join(output_dir, 'patients.csv'), index=False)
    print(f"✅ Patients: {len(patients_df)} records")
    
    providers_df.to_csv(os.path.join(output_dir, 'providers.csv'), index=False)
    print(f"✅ Providers: {len(providers_df)} records")
    
    visits_df.to_csv(os.path.join(output_dir, 'patient_visits.csv'), index=False)
    print(f"✅ Patient visits: {len(visits_df)} records")
    
    # Calculate and save KPIs
    kpis_df = calculate_healthcare_kpis(visits_df)
    kpis_output = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(kpis_output, exist_ok=True)
    kpis_df.to_csv(os.path.join(kpis_output, 'healthcare_kpis.csv'), index=False)
    print(f"✅ Healthcare KPIs calculated and saved")
    
    # Power BI export
    powerbi_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'powerbi_exports')
    os.makedirs(powerbi_dir, exist_ok=True)
    visits_df.to_csv(os.path.join(powerbi_dir, 'healthcare_visits.csv'), index=False)
    kpis_df.to_csv(os.path.join(powerbi_dir, 'healthcare_kpis.csv'), index=False)
    print(f"✅ Power BI exports saved")
    
    print("\n✨ Healthcare data generation complete!")
    print("\n📊 Quick Stats:")
    print(f"   Total Visits: {len(visits_df):,}")
    print(f"   Completion Rate: {(visits_df['status'] == 'Completed').mean() * 100:.1f}%")
    print(f"   Avg Wait Time: {visits_df['wait_time_minutes'].mean():.1f} min")
    print(f"   Avg Satisfaction: {visits_df['satisfaction_score'].mean():.1f}/5")


if __name__ == '__main__':
    main()
