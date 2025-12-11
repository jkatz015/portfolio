"""
Utility functions for D.A.T.A.
Dashboard & Analytics Tool for Accounting
Data processing, analysis, and chart generation
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional, Dict, List
import plotly.express as px
import plotly.graph_objects as go
try:
    from styles import CHART_COLORS, CHART_PALETTE, PLOTLY_LAYOUT
except ImportError:
    from app.styles import CHART_COLORS, CHART_PALETTE, PLOTLY_LAYOUT

# Try to import Streamlit for caching (optional)
try:
    import streamlit as st
    USE_CACHING = True
except ImportError:
    USE_CACHING = False


def detect_column_types(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Auto-detect column types for financial data.
    Returns dict with lists of column names by type.
    """
    detected = {
        'date': [],
        'amount': [],
        'category': [],
        'entity': [],
        'other': []
    }

    # Common column name patterns
    date_keywords = ['date', 'time', 'day', 'month', 'year', 'period']
    amount_keywords = ['amount', 'total', 'revenue', 'sales', 'expense', 'cost',
                       'price', 'value', 'sum', 'payment', 'balance', 'profit']
    category_keywords = ['category', 'type', 'department', 'group', 'class',
                         'segment', 'division', 'status']
    entity_keywords = ['vendor', 'customer', 'name', 'company', 'client',
                       'supplier', 'merchant', 'payee', 'account']

    for col in df.columns:
        col_lower = col.lower()

        # Check for date columns
        if any(kw in col_lower for kw in date_keywords):
            detected['date'].append(col)
        # Check for amount columns
        elif any(kw in col_lower for kw in amount_keywords):
            detected['amount'].append(col)
        # Check for category columns
        elif any(kw in col_lower for kw in category_keywords):
            detected['category'].append(col)
        # Check for entity columns
        elif any(kw in col_lower for kw in entity_keywords):
            detected['entity'].append(col)
        # Infer from data type
        elif df[col].dtype in ['float64', 'int64']:
            # Large numbers likely amounts
            if df[col].abs().mean() > 10:
                detected['amount'].append(col)
            else:
                detected['other'].append(col)
        elif df[col].dtype == 'object':
            # Try to parse as date
            try:
                pd.to_datetime(df[col].head(10), errors='raise')
                detected['date'].append(col)
            except:
                # Check cardinality for category vs entity
                unique_ratio = df[col].nunique() / len(df)
                if unique_ratio < 0.1:  # Low cardinality = category
                    detected['category'].append(col)
                elif unique_ratio < 0.5:  # Medium = entity
                    detected['entity'].append(col)
                else:
                    detected['other'].append(col)
        else:
            detected['other'].append(col)

    return detected


def clean_data(df: pd.DataFrame, date_col: Optional[str] = None,
               amount_col: Optional[str] = None) -> pd.DataFrame:
    """
    Clean and prepare the dataframe for analysis.
    """
    df_clean = df.copy()

    # Parse date column if specified
    if date_col and date_col in df_clean.columns:
        df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')
        df_clean = df_clean.dropna(subset=[date_col])
        df_clean['Year'] = df_clean[date_col].dt.year
        df_clean['Month'] = df_clean[date_col].dt.month
        df_clean['Month_Name'] = df_clean[date_col].dt.strftime('%b')
        df_clean['Year_Month'] = df_clean[date_col].dt.to_period('M').astype(str)

    # Clean amount column if specified
    if amount_col and amount_col in df_clean.columns:
        # Remove currency symbols and commas
        if df_clean[amount_col].dtype == 'object':
            df_clean[amount_col] = df_clean[amount_col].replace(
                r'[\$,€,£,¥]', '', regex=True
            ).replace(r'\(([0-9.]+)\)', r'-\1', regex=True)
            df_clean[amount_col] = pd.to_numeric(df_clean[amount_col], errors='coerce')

    return df_clean


def calculate_kpis(df: pd.DataFrame, amount_col: str) -> Dict[str, any]:
    """
    Calculate key performance indicators from the data.
    """
    if df.empty or amount_col not in df.columns:
        return {
            'total': 0,
            'total_positive': 0,
            'total_negative': 0,
            'average': 0,
            'median': 0,
            'min': 0,
            'max': 0,
            'count': 0,
            'std': 0,
        }

    amounts = df[amount_col].dropna()

    if len(amounts) == 0:
        return {
            'total': 0,
            'total_positive': 0,
            'total_negative': 0,
            'average': 0,
            'median': 0,
            'min': 0,
            'max': 0,
            'count': 0,
            'std': 0,
        }

    # Separate positive (revenue) and negative (expenses)
    positive = amounts[amounts > 0]
    negative = amounts[amounts < 0]

    kpis = {
        'total': amounts.sum(),
        'total_positive': positive.sum() if len(positive) > 0 else 0,
        'total_negative': abs(negative.sum()) if len(negative) > 0 else 0,
        'average': amounts.mean(),
        'median': amounts.median(),
        'min': amounts.min(),
        'max': amounts.max(),
        'count': len(amounts),
        'std': amounts.std() if len(amounts) > 1 else 0,
    }

    return kpis


def get_summary_stats(df: pd.DataFrame, amount_col: str,
                      category_col: Optional[str] = None,
                      date_col: Optional[str] = None) -> Dict:
    """
    Generate summary statistics for the dashboard.
    """
    stats = {
        'kpis': calculate_kpis(df, amount_col),
        'by_category': None,
        'by_month': None,
    }

    # Group by category if available
    if category_col and category_col in df.columns:
        by_cat = df.groupby(category_col)[amount_col].agg(['sum', 'count', 'mean'])
        by_cat = by_cat.sort_values('sum', ascending=False)
        stats['by_category'] = by_cat.reset_index()

    # Group by month if date available
    if date_col and 'Year_Month' in df.columns:
        by_month = df.groupby('Year_Month')[amount_col].agg(['sum', 'count', 'mean'])
        by_month = by_month.reset_index()
        stats['by_month'] = by_month

    return stats


def create_trend_chart(df: pd.DataFrame, date_col: str, amount_col: str) -> Optional[go.Figure]:
    """
    Create a monthly trend line chart.
    """
    if df.empty or 'Year_Month' not in df.columns or amount_col not in df.columns:
        return None

    try:
        monthly = df.groupby('Year_Month')[amount_col].sum().reset_index()
        if len(monthly) == 0:
            return None
        monthly = monthly.sort_values('Year_Month')
    except Exception:
        return None

    fig = go.Figure()

    # Add area fill
    fig.add_trace(go.Scatter(
        x=monthly['Year_Month'],
        y=monthly[amount_col],
        fill='tozeroy',
        fillcolor=f'rgba(45, 212, 191, 0.2)',
        line=dict(color=CHART_COLORS['accent'], width=3),
        mode='lines',
        name='Amount'
    ))

    # Add markers for data points
    fig.add_trace(go.Scatter(
        x=monthly['Year_Month'],
        y=monthly[amount_col],
        mode='markers',
        marker=dict(color=CHART_COLORS['primary'], size=8),
        name='',
        showlegend=False
    ))

    layout = {**PLOTLY_LAYOUT}
    layout['title'] = {'text': 'Monthly Trend', 'font': {'size': 14, 'color': '#1c1917'}, 'x': 0, 'xanchor': 'left'}
    fig.update_layout(
        **layout,
        xaxis_title='',
        yaxis_title='Amount',
        yaxis_tickformat='$,.0f',
        showlegend=False,
        height=350,
    )

    return fig


def create_category_chart(df: pd.DataFrame, category_col: str,
                          amount_col: str, chart_type: str = 'pie') -> Optional[go.Figure]:
    """
    Create a category breakdown chart (pie or bar).
    """
    if df.empty or category_col not in df.columns or amount_col not in df.columns:
        return None

    try:
        by_cat = df.groupby(category_col)[amount_col].sum().reset_index()
        if len(by_cat) == 0:
            return None
        by_cat = by_cat.sort_values(amount_col, ascending=False).head(10)
    except Exception:
        return None

    if chart_type == 'pie':
        fig = go.Figure(data=[go.Pie(
            labels=by_cat[category_col],
            values=by_cat[amount_col],
            hole=0.4,
            marker_colors=CHART_PALETTE,
            textinfo='percent+label',
            textposition='outside',
            textfont=dict(size=11),
        )])

        layout = {**PLOTLY_LAYOUT}
        layout['title'] = {'text': 'By Category', 'font': {'size': 14, 'color': '#1c1917'}, 'x': 0, 'xanchor': 'left'}
        fig.update_layout(
            **layout,
            showlegend=False,
            height=350,
        )
    else:
        fig = go.Figure(data=[go.Bar(
            x=by_cat[amount_col],
            y=by_cat[category_col],
            orientation='h',
            marker_color=CHART_COLORS['primary'],
            text=by_cat[amount_col].apply(lambda x: f'${x:,.0f}'),
            textposition='outside',
        )])

        layout = {**PLOTLY_LAYOUT}
        layout['title'] = {'text': 'By Category', 'font': {'size': 14, 'color': '#1c1917'}, 'x': 0, 'xanchor': 'left'}
        # Merge yaxis configuration properly
        if 'yaxis' in layout:
            layout['yaxis'].update({'categoryorder': 'total ascending', 'title': ''})
        else:
            layout['yaxis'] = {'categoryorder': 'total ascending', 'title': ''}

        fig.update_layout(
            **layout,
            xaxis_title='Amount',
            xaxis_tickformat='$,.0f',
            height=350,
        )

    return fig


def create_entity_chart(df: pd.DataFrame, entity_col: str,
                        amount_col: str, top_n: int = 10) -> Optional[go.Figure]:
    """
    Create a top entities horizontal bar chart.
    """
    if df.empty or entity_col not in df.columns or amount_col not in df.columns:
        return None

    try:
        by_entity = df.groupby(entity_col)[amount_col].sum().reset_index()
        if len(by_entity) == 0:
            return None
        by_entity = by_entity.nlargest(top_n, amount_col)
    except Exception:
        return None

    fig = go.Figure(data=[go.Bar(
        x=by_entity[amount_col],
        y=by_entity[entity_col],
        orientation='h',
        marker_color=CHART_COLORS['accent'],
        text=by_entity[amount_col].apply(lambda x: f'${x:,.0f}'),
        textposition='outside',
    )])

    layout = {**PLOTLY_LAYOUT}
    layout['title'] = {'text': f'Top {top_n} by Amount', 'font': {'size': 14, 'color': '#1c1917'}, 'x': 0, 'xanchor': 'left'}
    # Merge yaxis configuration properly
    if 'yaxis' in layout:
        layout['yaxis'].update({'categoryorder': 'total ascending', 'title': ''})
    else:
        layout['yaxis'] = {'categoryorder': 'total ascending', 'title': ''}

    fig.update_layout(
        **layout,
        xaxis_title='Amount',
        xaxis_tickformat='$,.0f',
        height=350,
    )

    return fig


def create_monthly_comparison_chart(df: pd.DataFrame, date_col: str,
                                    amount_col: str) -> Optional[go.Figure]:
    """
    Create a monthly comparison bar chart (grouped by year if multiple years).
    """
    if df.empty or 'Year' not in df.columns or 'Month_Name' not in df.columns or amount_col not in df.columns:
        return None

    # Check if we have multiple years
    years = df['Year'].unique()

    try:
        if len(years) > 1:
            # Group by year and month
            monthly = df.groupby(['Year', 'Month'])[amount_col].sum().reset_index()
            if len(monthly) == 0:
                return None
            monthly['Month_Name'] = monthly['Month'].apply(
                lambda x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][x-1]
            )

            fig = go.Figure()
            for i, year in enumerate(sorted(years)):
                year_data = monthly[monthly['Year'] == year]
                if len(year_data) > 0:
                    fig.add_trace(go.Bar(
                        x=year_data['Month_Name'],
                        y=year_data[amount_col],
                        name=str(int(year)),
                        marker_color=CHART_PALETTE[i % len(CHART_PALETTE)],
                    ))

            layout = {**PLOTLY_LAYOUT}
            layout['title'] = {'text': 'Monthly Comparison by Year', 'font': {'size': 14, 'color': '#1c1917'}, 'x': 0, 'xanchor': 'left'}
            fig.update_layout(
                **layout,
                xaxis_title='',
                yaxis_title='Amount',
                yaxis_tickformat='$,.0f',
                barmode='group',
                height=350,
            )
        else:
            # Single year - show monthly bars
            monthly = df.groupby('Month_Name')[amount_col].sum().reset_index()
            if len(monthly) == 0:
                return None
            # Sort by month order
            month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthly['Month_Order'] = monthly['Month_Name'].apply(
                lambda x: month_order.index(x) if x in month_order else 12
            )
            monthly = monthly.sort_values('Month_Order')

            fig = go.Figure(data=[go.Bar(
                x=monthly['Month_Name'],
                y=monthly[amount_col],
                marker_color=CHART_COLORS['primary'],
                text=monthly[amount_col].apply(lambda x: f'${x:,.0f}'),
                textposition='outside',
            )])

            layout = {**PLOTLY_LAYOUT}
            layout['title'] = {'text': 'Monthly Totals', 'font': {'size': 14, 'color': '#1c1917'}, 'x': 0, 'xanchor': 'left'}
            fig.update_layout(
                **layout,
                xaxis_title='',
                yaxis_title='Amount',
                yaxis_tickformat='$,.0f',
                height=350,
            )

        return fig
    except Exception:
        return None


def format_currency(value: float) -> str:
    """Format a number as currency."""
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:,.1f}M"
    elif abs(value) >= 1_000:
        return f"${value/1_000:,.1f}K"
    else:
        return f"${value:,.0f}"


def generate_summary_report(df: pd.DataFrame, amount_col: str,
                            category_col: Optional[str] = None) -> pd.DataFrame:
    """
    Generate a summary report dataframe for download.
    """
    kpis = calculate_kpis(df, amount_col)

    report_data = [
        {'Metric': 'Total Amount', 'Value': f"${kpis['total']:,.2f}"},
        {'Metric': 'Total Positive (Revenue)', 'Value': f"${kpis['total_positive']:,.2f}"},
        {'Metric': 'Total Negative (Expenses)', 'Value': f"${kpis['total_negative']:,.2f}"},
        {'Metric': 'Average Transaction', 'Value': f"${kpis['average']:,.2f}"},
        {'Metric': 'Median Transaction', 'Value': f"${kpis['median']:,.2f}"},
        {'Metric': 'Minimum', 'Value': f"${kpis['min']:,.2f}"},
        {'Metric': 'Maximum', 'Value': f"${kpis['max']:,.2f}"},
        {'Metric': 'Transaction Count', 'Value': f"{kpis['count']:,}"},
        {'Metric': 'Standard Deviation', 'Value': f"${kpis['std']:,.2f}"},
    ]

    return pd.DataFrame(report_data)
