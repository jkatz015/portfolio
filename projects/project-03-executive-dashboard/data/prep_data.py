"""
Superstore Data Prep for Executive Dashboard
Adds calculated fields for Tableau
"""
import pandas as pd
from datetime import datetime

# Load data
df = pd.read_csv('Sample - Superstore.csv', encoding='latin-1')

print(f"Loaded {len(df):,} records")
print(f"Date range: {df['Order Date'].min()} to {df['Order Date'].max()}")

# Parse dates
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y')

# Add calculated fields
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['Month Name'] = df['Order Date'].dt.strftime('%b')
df['Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
df['Quarter'] = df['Order Date'].dt.quarter
df['Day of Week'] = df['Order Date'].dt.day_name()

# Financial metrics
df['Revenue'] = df['Sales']  # Rename for clarity
df['Gross Margin'] = df['Profit'] / df['Sales']
df['Gross Margin %'] = (df['Profit'] / df['Sales'] * 100).round(2)
df['Cost'] = df['Sales'] - df['Profit']
df['Discount Amount'] = df['Sales'] * df['Discount'] / (1 - df['Discount'])

# Handle edge cases
df['Gross Margin %'] = df['Gross Margin %'].fillna(0)
df['Gross Margin'] = df['Gross Margin'].fillna(0)

# Shipping days
df['Ship Days'] = (df['Ship Date'] - df['Order Date']).dt.days

# Create a synthetic budget (for variance analysis)
# Budget = Prior year actual * 1.1 (10% growth target)
df_sorted = df.sort_values('Order Date')
df['Budget'] = df['Revenue'] * 1.1  # Simplified - in real world this would come from planning

# Add prior year for YoY comparison (shift by creating lookup)
df['Prior Year'] = df['Year'] - 1

# Summary stats
print(f"\nData Summary:")
print(f"  Years: {sorted(df['Year'].unique())}")
print(f"  Regions: {df['Region'].unique().tolist()}")
print(f"  Categories: {df['Category'].unique().tolist()}")
print(f"  Segments: {df['Segment'].unique().tolist()}")
print(f"\n  Total Revenue: ${df['Revenue'].sum():,.2f}")
print(f"  Total Profit: ${df['Profit'].sum():,.2f}")
print(f"  Overall Margin: {df['Profit'].sum() / df['Revenue'].sum() * 100:.1f}%")

# Save prepped data
output_file = 'superstore_tableau_ready.csv'
df.to_csv(output_file, index=False)
print(f"\nSaved: {output_file}")

# Also create summary tables for KPI cards
summary = {
    'Metric': ['Total Revenue', 'Total Profit', 'Total Orders', 'Avg Order Value', 'Overall Margin %'],
    'Value': [
        f"${df['Revenue'].sum():,.0f}",
        f"${df['Profit'].sum():,.0f}",
        f"{df['Order ID'].nunique():,}",
        f"${df['Revenue'].sum() / df['Order ID'].nunique():,.2f}",
        f"{df['Profit'].sum() / df['Revenue'].sum() * 100:.1f}%"
    ]
}
pd.DataFrame(summary).to_csv('kpi_summary.csv', index=False)
print("Saved: kpi_summary.csv")
