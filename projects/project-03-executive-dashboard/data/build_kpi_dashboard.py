"""
Executive KPI Dashboard Generator
=================================
Generates an interactive HTML dashboard from Superstore data.

Usage:
    python build_kpi_dashboard.py

Output:
    - ../reports/executive_dashboard.html
    - ../reports/kpi_metrics.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# Load prepared data
df = pd.read_csv('superstore_tableau_ready.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'])

print(f"Building KPI Dashboard from {len(df):,} records...")

# ============================================================
# CALCULATE KPIs
# ============================================================

# Overall metrics
total_revenue = df['Revenue'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
total_customers = df['Customer ID'].nunique()
avg_order_value = total_revenue / total_orders
overall_margin = (total_profit / total_revenue) * 100

# Year-over-Year comparison (using most recent full year)
years = sorted(df['Year'].unique())
current_year = years[-1]
prior_year = years[-2] if len(years) > 1 else current_year

cy_revenue = df[df['Year'] == current_year]['Revenue'].sum()
py_revenue = df[df['Year'] == prior_year]['Revenue'].sum()
yoy_growth = ((cy_revenue - py_revenue) / py_revenue * 100) if py_revenue > 0 else 0

cy_profit = df[df['Year'] == current_year]['Profit'].sum()
py_profit = df[df['Year'] == prior_year]['Profit'].sum()
profit_yoy = ((cy_profit - py_profit) / py_profit * 100) if py_profit > 0 else 0

# By Region
region_metrics = df.groupby('Region').agg({
    'Revenue': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique'
}).round(2)
region_metrics['Margin %'] = (region_metrics['Profit'] / region_metrics['Revenue'] * 100).round(1)
region_metrics = region_metrics.sort_values('Revenue', ascending=False)

# By Category
category_metrics = df.groupby('Category').agg({
    'Revenue': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique'
}).round(2)
category_metrics['Margin %'] = (category_metrics['Profit'] / category_metrics['Revenue'] * 100).round(1)
category_metrics = category_metrics.sort_values('Revenue', ascending=False)

# By Segment
segment_metrics = df.groupby('Segment').agg({
    'Revenue': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique'
}).round(2)
segment_metrics['Margin %'] = (segment_metrics['Profit'] / segment_metrics['Revenue'] * 100).round(1)
segment_metrics = segment_metrics.sort_values('Revenue', ascending=False)

# Monthly Trend
monthly = df.groupby(['Year', 'Month']).agg({
    'Revenue': 'sum',
    'Profit': 'sum'
}).round(2).reset_index()
monthly['Year-Month'] = monthly['Year'].astype(str) + '-' + monthly['Month'].astype(str).str.zfill(2)

# Top 10 Customers
top_customers = df.groupby(['Customer ID', 'Customer Name']).agg({
    'Revenue': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique'
}).round(2).reset_index()
top_customers = top_customers.sort_values('Revenue', ascending=False).head(10)

# Top 10 Products by Revenue
top_products = df.groupby('Product Name').agg({
    'Revenue': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).round(2).reset_index()
top_products = top_products.sort_values('Revenue', ascending=False).head(10)

# Shipping Performance
avg_ship_days = df['Ship Days'].mean()
ship_mode_metrics = df.groupby('Ship Mode').agg({
    'Ship Days': 'mean',
    'Order ID': 'nunique',
    'Revenue': 'sum'
}).round(2)
ship_mode_metrics = ship_mode_metrics.sort_values('Revenue', ascending=False)

# ============================================================
# GENERATE HTML DASHBOARD
# ============================================================

def format_currency(val):
    if val >= 1_000_000:
        return f"${val/1_000_000:.1f}M"
    elif val >= 1_000:
        return f"${val/1_000:.1f}K"
    else:
        return f"${val:,.0f}"

def format_number(val):
    if val >= 1_000_000:
        return f"{val/1_000_000:.1f}M"
    elif val >= 1_000:
        return f"{val/1_000:.1f}K"
    else:
        return f"{val:,.0f}"

def trend_indicator(val):
    if val > 0:
        return f'<span class="trend-up">▲ {val:.1f}%</span>'
    elif val < 0:
        return f'<span class="trend-down">▼ {abs(val):.1f}%</span>'
    else:
        return f'<span class="trend-flat">● {val:.1f}%</span>'

# Create bar chart HTML (CSS-based)
def create_bar_chart(data, value_col, label_col, max_val=None):
    if max_val is None:
        max_val = data[value_col].max()

    html = '<div class="bar-chart">'
    for _, row in data.iterrows():
        pct = (row[value_col] / max_val * 100) if max_val > 0 else 0
        html += f'''
        <div class="bar-row">
            <div class="bar-label">{row[label_col]}</div>
            <div class="bar-container">
                <div class="bar" style="width: {pct}%"></div>
            </div>
            <div class="bar-value">{format_currency(row[value_col])}</div>
        </div>
        '''
    html += '</div>'
    return html

# Region chart data
region_chart_data = region_metrics.reset_index()

# Category chart data
category_chart_data = category_metrics.reset_index()

# Segment chart data
segment_chart_data = segment_metrics.reset_index()

html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Executive Finance Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #ffffff;
            min-height: 100vh;
            padding: 20px;
        }}

        .dashboard {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .header {{
            text-align: center;
            padding: 30px 0;
            border-bottom: 2px solid #4a90a4;
            margin-bottom: 30px;
        }}

        .header h1 {{
            font-size: 2.5em;
            font-weight: 300;
            margin-bottom: 10px;
            color: #4fc3f7;
        }}

        .header .subtitle {{
            color: #90caf9;
            font-size: 1.1em;
        }}

        .timestamp {{
            color: #78909c;
            font-size: 0.9em;
            margin-top: 10px;
        }}

        /* KPI Cards */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .kpi-card {{
            background: linear-gradient(145deg, #1e3a5f 0%, #1a2d47 100%);
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            border: 1px solid #2d4a6f;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .kpi-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}

        .kpi-label {{
            font-size: 0.85em;
            color: #90caf9;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}

        .kpi-value {{
            font-size: 2.2em;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 8px;
        }}

        .kpi-subtext {{
            font-size: 0.85em;
            color: #78909c;
        }}

        .trend-up {{
            color: #4caf50;
            font-weight: 600;
        }}

        .trend-down {{
            color: #f44336;
            font-weight: 600;
        }}

        .trend-flat {{
            color: #ffc107;
        }}

        /* Section styling */
        .section {{
            background: linear-gradient(145deg, #1e3a5f 0%, #1a2d47 100%);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid #2d4a6f;
        }}

        .section h2 {{
            font-size: 1.3em;
            font-weight: 500;
            color: #4fc3f7;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #2d4a6f;
        }}

        /* Grid layouts */
        .two-col {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
        }}

        .three-col {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }}

        /* Bar chart styling */
        .bar-chart {{
            width: 100%;
        }}

        .bar-row {{
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }}

        .bar-label {{
            width: 100px;
            font-size: 0.9em;
            color: #b0bec5;
            flex-shrink: 0;
        }}

        .bar-container {{
            flex-grow: 1;
            height: 24px;
            background: #1a2d47;
            border-radius: 4px;
            margin: 0 15px;
            overflow: hidden;
        }}

        .bar {{
            height: 100%;
            background: linear-gradient(90deg, #4fc3f7 0%, #29b6f6 100%);
            border-radius: 4px;
            transition: width 0.5s ease;
        }}

        .bar-value {{
            width: 80px;
            text-align: right;
            font-size: 0.9em;
            color: #ffffff;
            font-weight: 500;
        }}

        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th {{
            text-align: left;
            padding: 12px 15px;
            background: #1a2d47;
            color: #4fc3f7;
            font-weight: 500;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #2d4a6f;
            color: #e0e0e0;
        }}

        tr:hover td {{
            background: rgba(79, 195, 247, 0.1);
        }}

        .text-right {{
            text-align: right;
        }}

        .positive {{
            color: #4caf50;
        }}

        .negative {{
            color: #f44336;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 30px;
            color: #78909c;
            font-size: 0.9em;
            border-top: 1px solid #2d4a6f;
            margin-top: 30px;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .kpi-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}

            .two-col, .three-col {{
                grid-template-columns: 1fr;
            }}

            .bar-label {{
                width: 70px;
                font-size: 0.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>Executive Finance Dashboard</h1>
            <div class="subtitle">Financial Performance Overview | {years[0]} - {years[-1]}</div>
            <div class="timestamp">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        </div>

        <!-- KPI Cards -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Total Revenue</div>
                <div class="kpi-value">{format_currency(total_revenue)}</div>
                <div class="kpi-subtext">{trend_indicator(yoy_growth)} YoY</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Total Profit</div>
                <div class="kpi-value">{format_currency(total_profit)}</div>
                <div class="kpi-subtext">{trend_indicator(profit_yoy)} YoY</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Gross Margin</div>
                <div class="kpi-value">{overall_margin:.1f}%</div>
                <div class="kpi-subtext">Target: 15%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Total Orders</div>
                <div class="kpi-value">{format_number(total_orders)}</div>
                <div class="kpi-subtext">{total_customers:,} customers</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Avg Order Value</div>
                <div class="kpi-value">${avg_order_value:.0f}</div>
                <div class="kpi-subtext">Per transaction</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Avg Ship Days</div>
                <div class="kpi-value">{avg_ship_days:.1f}</div>
                <div class="kpi-subtext">Order to delivery</div>
            </div>
        </div>

        <!-- Revenue Breakdown -->
        <div class="three-col">
            <div class="section">
                <h2>Revenue by Region</h2>
                {create_bar_chart(region_chart_data, 'Revenue', 'Region')}
            </div>
            <div class="section">
                <h2>Revenue by Category</h2>
                {create_bar_chart(category_chart_data, 'Revenue', 'Category')}
            </div>
            <div class="section">
                <h2>Revenue by Segment</h2>
                {create_bar_chart(segment_chart_data, 'Revenue', 'Segment')}
            </div>
        </div>

        <!-- Detailed Tables -->
        <div class="two-col">
            <div class="section">
                <h2>Regional Performance</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Region</th>
                            <th class="text-right">Revenue</th>
                            <th class="text-right">Profit</th>
                            <th class="text-right">Margin %</th>
                            <th class="text-right">Orders</th>
                        </tr>
                    </thead>
                    <tbody>
"""

for region, row in region_metrics.iterrows():
    margin_class = 'positive' if row['Margin %'] > 10 else ('negative' if row['Margin %'] < 5 else '')
    html += f"""
                        <tr>
                            <td>{region}</td>
                            <td class="text-right">{format_currency(row['Revenue'])}</td>
                            <td class="text-right">{format_currency(row['Profit'])}</td>
                            <td class="text-right {margin_class}">{row['Margin %']:.1f}%</td>
                            <td class="text-right">{int(row['Order ID']):,}</td>
                        </tr>
    """

html += """
                    </tbody>
                </table>
            </div>

            <div class="section">
                <h2>Category Performance</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Category</th>
                            <th class="text-right">Revenue</th>
                            <th class="text-right">Profit</th>
                            <th class="text-right">Margin %</th>
                            <th class="text-right">Orders</th>
                        </tr>
                    </thead>
                    <tbody>
"""

for category, row in category_metrics.iterrows():
    margin_class = 'positive' if row['Margin %'] > 10 else ('negative' if row['Margin %'] < 5 else '')
    html += f"""
                        <tr>
                            <td>{category}</td>
                            <td class="text-right">{format_currency(row['Revenue'])}</td>
                            <td class="text-right">{format_currency(row['Profit'])}</td>
                            <td class="text-right {margin_class}">{row['Margin %']:.1f}%</td>
                            <td class="text-right">{int(row['Order ID']):,}</td>
                        </tr>
    """

html += """
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Top Customers -->
        <div class="section">
            <h2>Top 10 Customers by Revenue</h2>
            <table>
                <thead>
                    <tr>
                        <th>Customer</th>
                        <th class="text-right">Revenue</th>
                        <th class="text-right">Profit</th>
                        <th class="text-right">Margin %</th>
                        <th class="text-right">Orders</th>
                    </tr>
                </thead>
                <tbody>
"""

for _, row in top_customers.iterrows():
    margin = (row['Profit'] / row['Revenue'] * 100) if row['Revenue'] > 0 else 0
    margin_class = 'positive' if margin > 10 else ('negative' if margin < 5 else '')
    html += f"""
                    <tr>
                        <td>{row['Customer Name']}</td>
                        <td class="text-right">{format_currency(row['Revenue'])}</td>
                        <td class="text-right">{format_currency(row['Profit'])}</td>
                        <td class="text-right {margin_class}">{margin:.1f}%</td>
                        <td class="text-right">{int(row['Order ID']):,}</td>
                    </tr>
    """

html += """
                </tbody>
            </table>
        </div>

        <!-- Top Products -->
        <div class="section">
            <h2>Top 10 Products by Revenue</h2>
            <table>
                <thead>
                    <tr>
                        <th>Product</th>
                        <th class="text-right">Revenue</th>
                        <th class="text-right">Profit</th>
                        <th class="text-right">Units Sold</th>
                    </tr>
                </thead>
                <tbody>
"""

for _, row in top_products.iterrows():
    profit_class = 'positive' if row['Profit'] > 0 else 'negative'
    html += f"""
                    <tr>
                        <td>{row['Product Name'][:50]}{'...' if len(row['Product Name']) > 50 else ''}</td>
                        <td class="text-right">{format_currency(row['Revenue'])}</td>
                        <td class="text-right {profit_class}">{format_currency(row['Profit'])}</td>
                        <td class="text-right">{int(row['Quantity']):,}</td>
                    </tr>
    """

html += """
                </tbody>
            </table>
        </div>

        <!-- Shipping Performance -->
        <div class="section">
            <h2>Shipping Performance by Mode</h2>
            <table>
                <thead>
                    <tr>
                        <th>Ship Mode</th>
                        <th class="text-right">Avg Days</th>
                        <th class="text-right">Orders</th>
                        <th class="text-right">Revenue</th>
                    </tr>
                </thead>
                <tbody>
"""

for mode, row in ship_mode_metrics.iterrows():
    html += f"""
                    <tr>
                        <td>{mode}</td>
                        <td class="text-right">{row['Ship Days']:.1f}</td>
                        <td class="text-right">{int(row['Order ID']):,}</td>
                        <td class="text-right">{format_currency(row['Revenue'])}</td>
                    </tr>
    """

html += f"""
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>Executive Finance Dashboard | Data Period: {years[0]} - {years[-1]} | {len(df):,} transactions analyzed</p>
            <p style="margin-top: 10px;">Built with Python | Portfolio Project</p>
        </div>
    </div>
</body>
</html>
"""

# ============================================================
# SAVE OUTPUTS
# ============================================================

output_dir = Path('../reports')
output_dir.mkdir(parents=True, exist_ok=True)

# Save HTML dashboard
html_file = output_dir / 'executive_dashboard.html'
with open(html_file, 'w') as f:
    f.write(html)
print(f"Saved: {html_file}")

# Save KPI metrics CSV
kpi_data = {
    'Metric': [
        'Total Revenue',
        'Total Profit',
        'Gross Margin %',
        'Total Orders',
        'Total Customers',
        'Avg Order Value',
        'YoY Revenue Growth %',
        'YoY Profit Growth %',
        'Avg Ship Days'
    ],
    'Value': [
        f"${total_revenue:,.2f}",
        f"${total_profit:,.2f}",
        f"{overall_margin:.1f}%",
        f"{total_orders:,}",
        f"{total_customers:,}",
        f"${avg_order_value:,.2f}",
        f"{yoy_growth:.1f}%",
        f"{profit_yoy:.1f}%",
        f"{avg_ship_days:.1f}"
    ]
}
pd.DataFrame(kpi_data).to_csv(output_dir / 'kpi_metrics.csv', index=False)
print(f"Saved: {output_dir / 'kpi_metrics.csv'}")

# Save detailed breakdown CSVs
region_metrics.to_csv(output_dir / 'region_metrics.csv')
print(f"Saved: {output_dir / 'region_metrics.csv'}")

category_metrics.to_csv(output_dir / 'category_metrics.csv')
print(f"Saved: {output_dir / 'category_metrics.csv'}")

print(f"\n{'='*60}")
print("DASHBOARD BUILD COMPLETE")
print(f"{'='*60}")
print(f"Records Analyzed: {len(df):,}")
print(f"Date Range: {years[0]} - {years[-1]}")
print(f"Output Location: {output_dir.absolute()}")
print(f"{'='*60}")
