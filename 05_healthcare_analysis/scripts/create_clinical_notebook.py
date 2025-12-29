import nbformat as nbf
import os

def create_clinical_nb():
    nb = nbf.v4.new_notebook()
    
    # 1. Header
    nb.cells.append(nbf.v4.new_markdown_cell("# 🏥 Clinical Intelligence & Patient Outcomes Dashboard\n\nThis dashboard provides advanced clinical analytics focusing on operational efficiency, patient outcomes, and readmission risk management."))
    
    # 2. Imports
    nb.cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "plotly_white"
pio.renderers.default = "notebook_connected"

# Load Data
visits = pd.read_csv('../data/patient_visits.csv')
readmissions = pd.read_csv('../outputs/readmission_analysis.csv')
efficiency = pd.read_csv('../outputs/clinical_efficiency.csv')

visits['visit_date'] = pd.to_datetime(visits['visit_date'])

print("✅ Clinical analytics data loaded successfully")"""))

    # 3. Readmission Analytics
    nb.cells.append(nbf.v4.new_markdown_cell("## 🔄 1. 30-Day Readmission Analysis\nMonitoring clinical departments for high readmission rates—a key indicator of treatment efficacy and follow-up quality."))
    nb.cells.append(nbf.v4.new_code_cell("""fig_readmission = px.bar(
    readmissions, x='department', y='readmission_rate',
    text_auto='.1f',
    color='readmission_rate',
    color_continuous_scale='Reds',
    title='<b>Readmission Rate by Clinical Department</b>'
)
fig_readmission.add_hline(y=15, line_dash="dot", annotation_text="Industry Benchmark (15%)")
fig_readmission.show()"""))

    # 4. Operational Bottlenecks
    nb.cells.append(nbf.v4.new_markdown_cell("## ⏳ 2. Operational Efficiency & Wait Times\nMapping wait times against clinical severity to identify bottlenecks in patient care."))
    nb.cells.append(nbf.v4.new_code_cell("""# Wait Time vs Outcome by Department
fig_bubble = px.scatter(
    efficiency, x='wait_time_minutes', y='outcome_score',
    size='efficiency_index', color='department',
    hover_name='department',
    labels={'wait_time_minutes': 'Avg Wait (Mins)', 'outcome_score': 'Treatment Outcome (Lower is Better)'},
    title='<b>Efficiency Matrix: Wait Time vs Treatment Success</b><br><sup>Bubble size represents Efficiency Index</sup>'
)
fig_bubble.show()"""))

    # 5. Patient Satisfaction & Severity
    nb.cells.append(nbf.v4.new_markdown_cell("## ⭐ 3. Satisfaction & Severity Correlation\nUnderstanding how patient severity impacts their perceived quality of care."))
    nb.cells.append(nbf.v4.new_code_cell("""# Sample visits for visualization
sample_visits = visits[visits['status'] == 'Completed'].sample(1000)

fig_box = px.box(
    sample_visits, x='severity_level', y='satisfaction_score',
    color='severity_level',
    title='<b>Satisfaction Distribution by Criticality</b>',
    labels={'severity_level': 'Clinical Severity (1-5)', 'satisfaction_score': 'Satisfaction Score'}
)
fig_box.show()"""))

    # 6. Clinical Outcome Trend
    nb.cells.append(nbf.v4.new_markdown_cell("## 🛡️ 4. Clinical Quality Metrics\nSummary of high-level clinical performance indicators."))
    nb.cells.append(nbf.v4.new_code_cell("""avg_satisfaction = visits['satisfaction_score'].mean()
avg_outcome = visits['outcome_score'].mean()
readmission_total = visits['is_readmission'].mean() * 100

summary_data = pd.DataFrame({
    'Metric': ['Patient Satisfaction', 'Treatment Success (1-5)', 'Readmission Rate (%)'],
    'Value': [f"{avg_satisfaction:.2f}/5", f"{avg_outcome:.2f}/5", f"{readmission_total:.1f}%"]
})

print("--- Clinical Performance Summary ---")
print(summary_data)"""))

    # Save
    nb_dir = "d:/Acode/publicprofile/05_healthcare_analysis/notebooks"
    os.makedirs(nb_dir, exist_ok=True)
    with open(os.path.join(nb_dir, 'clinical_intelligence_dashboard.ipynb'), 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"✅ Healthcare dashboard created at {nb_dir}")

if __name__ == '__main__':
    create_clinical_nb()
