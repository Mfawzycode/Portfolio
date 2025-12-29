"""
Sales Analysis Functions
Reusable analytics functions for the Sales Dashboard project.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def load_sales_data(filepath: str = '../shared/data/sales_transactions.csv') -> pd.DataFrame:
    """Load and prepare sales data."""
    df = pd.read_csv(filepath, parse_dates=['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%B')
    df['quarter'] = df['date'].dt.quarter
    df['week'] = df['date'].dt.isocalendar().week
    df['day_of_week'] = df['date'].dt.day_name()
    return df


def calculate_kpis(df: pd.DataFrame) -> dict:
    """Calculate key performance indicators."""
    return {
        'total_revenue': df['revenue'].sum(),
        'total_profit': df['profit'].sum(),
        'total_transactions': len(df),
        'avg_order_value': df['revenue'].mean(),
        'profit_margin': (df['profit'].sum() / df['revenue'].sum()) * 100,
        'unique_customers': df['customer_id'].nunique(),
        'avg_discount': df['discount_percent'].mean() * 100
    }


def revenue_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly revenue."""
    monthly = df.groupby(['year', 'month']).agg({
        'revenue': 'sum',
        'profit': 'sum',
        'transaction_id': 'count'
    }).reset_index()
    monthly.columns = ['year', 'month', 'revenue', 'profit', 'transactions']
    return monthly


def revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue breakdown by product category."""
    return df.groupby('product_category').agg({
        'revenue': 'sum',
        'profit': 'sum',
        'quantity': 'sum',
        'transaction_id': 'count'
    }).reset_index().sort_values('revenue', ascending=False)


def revenue_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue breakdown by region."""
    return df.groupby('region').agg({
        'revenue': 'sum',
        'profit': 'sum',
        'transaction_id': 'count'
    }).reset_index().sort_values('revenue', ascending=False)


def customer_segment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze performance by customer segment."""
    return df.groupby('customer_segment').agg({
        'revenue': 'sum',
        'profit': 'sum',
        'customer_id': 'nunique',
        'transaction_id': 'count'
    }).reset_index()


def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Get top N products by revenue."""
    return df.groupby(['product_category', 'product_name']).agg({
        'revenue': 'sum',
        'quantity': 'sum'
    }).reset_index().nlargest(n, 'revenue')


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def plot_revenue_trend(df: pd.DataFrame) -> go.Figure:
    """Create monthly revenue trend chart."""
    monthly = revenue_by_month(df)
    monthly['date'] = pd.to_datetime(monthly[['year', 'month']].assign(day=1))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly['date'], y=monthly['revenue'],
        mode='lines+markers', name='Revenue',
        line=dict(color='#2E86AB', width=3)
    ))
    fig.add_trace(go.Bar(
        x=monthly['date'], y=monthly['profit'],
        name='Profit', marker_color='#A23B72', opacity=0.6
    ))
    
    fig.update_layout(
        title='Monthly Revenue & Profit Trend',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        template='plotly_white',
        hovermode='x unified'
    )
    return fig


def plot_category_breakdown(df: pd.DataFrame) -> go.Figure:
    """Create product category pie chart."""
    cat_data = revenue_by_category(df)
    
    fig = px.pie(
        cat_data, values='revenue', names='product_category',
        title='Revenue by Product Category',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_traces(textinfo='percent+label')
    return fig


def plot_region_comparison(df: pd.DataFrame) -> go.Figure:
    """Create regional comparison bar chart."""
    region_data = revenue_by_region(df)
    
    fig = px.bar(
        region_data, x='region', y='revenue',
        color='profit', color_continuous_scale='Viridis',
        title='Revenue by Region (Colored by Profit)'
    )
    fig.update_layout(template='plotly_white')
    return fig


def create_kpi_cards(kpis: dict) -> go.Figure:
    """Create KPI indicator cards."""
    fig = make_subplots(
        rows=1, cols=4,
        specs=[[{'type': 'indicator'}] * 4]
    )
    
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=kpis['total_revenue'],
        title={"text": "Total Revenue"},
        number={'prefix': "$", 'valueformat': ',.0f'},
    ), row=1, col=1)
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis['total_transactions'],
        title={"text": "Transactions"},
    ), row=1, col=2)
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis['profit_margin'],
        title={"text": "Profit Margin"},
        number={'suffix': '%', 'valueformat': '.1f'},
    ), row=1, col=3)
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis['unique_customers'],
        title={"text": "Unique Customers"},
    ), row=1, col=4)
    
    fig.update_layout(height=200, template='plotly_white')
    return fig


if __name__ == '__main__':
    # Quick demo
    print("Loading sales data...")
    df = load_sales_data()
    
    print("\n📊 Key Performance Indicators:")
    kpis = calculate_kpis(df)
    for key, value in kpis.items():
        if 'revenue' in key or 'profit' in key or 'value' in key:
            print(f"   {key}: ${value:,.2f}")
        elif 'margin' in key or 'discount' in key:
            print(f"   {key}: {value:.1f}%")
        else:
            print(f"   {key}: {value:,}")
    
    print("\n📈 Top 5 Products:")
    print(top_products(df, 5).to_string(index=False))
