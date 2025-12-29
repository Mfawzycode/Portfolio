import nbformat as nbf
import os

def create_predictive_nb():
    nb = nbf.v4.new_notebook()
    
    # 1. Header
    nb.cells.append(nbf.v4.new_markdown_cell("# 🔮 Demand Intelligence & Predictive Risk Dashboard\n\nThis dashboard provides a forward-looking view of business operations, combining time-series forecasting with customer churn risk modeling."))
    
    # 2. Imports
    nb.cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

pio.templates.default = "plotly_white"
pio.renderers.default = "notebook_connected"

# Load Data
forecast = pd.read_csv('../outputs/sales_forecast_results.csv')
history = pd.read_csv('../data/sales_history.csv')
churn = pd.read_csv('../outputs/customer_risk_scores.csv')

history['date'] = pd.to_datetime(history['date'])
forecast['date'] = pd.to_datetime(forecast['date'])

print("✅ Predictive data loaded successfully")"""))

    # 3. Forecast Visualization
    nb.cells.append(nbf.v4.new_markdown_cell("## 📈 1. Demand Forecasting (Next 30 Days)\nVisualizing actual historical performance vs. predicted future demand with confidence intervals."))
    nb.cells.append(nbf.v4.new_code_cell("""# Combine context history (last 60 days) with forecast
recent_history = history.tail(60)

fig = go.Figure()

# Actual History
fig.add_trace(go.Scatter(
    x=recent_history['date'], y=recent_history['sales'],
    name='Actual Sales', line=dict(color='royalblue', width=2)
))

# Predicted Forecast
fig.add_trace(go.Scatter(
    x=forecast['date'], y=forecast['predicted_sales'],
    name='Predicted Forecast', line=dict(color='firebrick', width=3, dash='dot')
))

# Confidence Intervals
fig.add_trace(go.Scatter(
    x=pd.concat([forecast['date'], forecast['date'][::-1]]),
    y=pd.concat([forecast['confidence_upper'], forecast['confidence_lower'][::-1]]),
    fill='toself', fillcolor='rgba(178, 34, 34, 0.1)',
    line=dict(color='rgba(255,255,255,0)'),
    name='90% Confidence Interval', showlegend=False
))

fig.update_layout(
    title='<b>Sales Demand Forecast</b><br><sup>Forward-looking prediction vs Historical baseline</sup>',
    xaxis_title='Date', yaxis_title='Sales Volume',
    height=500, margin=dict(t=80, b=50, l=50, r=50)
)
fig.show()"""))

    # 4. Churn Risk Analysis
    nb.cells.append(nbf.v4.new_markdown_cell("## 🔄 2. Customer Retention & Churn Risk\nIdentifying 'At-Risk' customers by analyzing behavioral engagement signals."))
    nb.cells.append(nbf.v4.new_code_cell("""# Risk Distribution
risk_counts = churn['risk_tier'].value_counts().reset_index()
risk_counts.columns = ['Risk Tier', 'Customer Count']

fig_pie = px.pie(
    risk_counts, values='Customer Count', names='Risk Tier',
    color='Risk Tier',
    color_discrete_map={'Low':'#2ecc71', 'Medium':'#f1c40f', 'High':'#e74c3c'},
    hole=0.4,
    title='<b>Portfolio Risk Profile</b>'
)

# Login vs Spend vs Risk
fig_scatter = px.scatter(
    churn.sample(500), # Sample for performance
    x='logins_30d', y='avg_monthly_spend',
    color='risk_tier', size='tenure_days',
    labels={'logins_30d': 'Recent Logins', 'avg_monthly_spend': 'Avg Monthly Spend ($)'},
    title='<b>Risk Clusters: Engagement vs Value</b>',
    color_discrete_map={'Low':'#2ecc71', 'Medium':'#f1c40f', 'High':'#e74c3c'}
)

fig_pie.show()
fig_scatter.show()"""))

    # 5. Risk Correlation Heatmap
    nb.cells.append(nbf.v4.new_markdown_cell("## 📊 3. Predictive Feature Impact\nUnderstanding which behaviors drive high risk scores."))
    nb.cells.append(nbf.v4.new_code_cell("""# Correlation of numeric features with risk
cols = ['tenure_days', 'avg_monthly_spend', 'logins_30d', 'support_tickets_30d', 'risk_score']
corr = churn[cols].corr()

fig_corr = px.imshow(
    corr, text_auto=".2f",
    color_continuous_scale='RdBu_r',
    title='<b>Predictive Feature Correlation Matrix</b>'
)
fig_corr.show()"""))

    # Save
    nb_dir = "d:/Acode/publicprofile/08_predictive_analytics/notebooks"
    os.makedirs(nb_dir, exist_ok=True)
    with open(os.path.join(nb_dir, 'demand_intelligence_dashboard.ipynb'), 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"✅ Dashboard notebook created at {nb_dir}")

if __name__ == '__main__':
    create_predictive_nb()
