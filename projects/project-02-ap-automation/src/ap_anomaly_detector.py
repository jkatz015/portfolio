"""
AP Invoice Anomaly Detector
===========================
Automated detection of suspicious AP transactions.

Usage:
    python ap_anomaly_detector.py input_file.csv
    python ap_anomaly_detector.py input_file.xlsx

Output:
    - flagged_invoices.csv (records with anomalies)
    - anomaly_report.csv (summary statistics)
    - anomaly_report.html (formatted report)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import argparse
import sys
from pathlib import Path

# ============================================================
# CONFIGURATION - Adjust column names to match your data
# ============================================================
CONFIG = {
    'invoice_id': 'INVOICE_ID',
    'vendor_id': 'VENDOR_ID',
    'vendor_name': 'VENDOR_NAME',
    'invoice_date': 'INVOICE_DATE',
    'invoice_amount': 'INVOICE_AMOUNT',
    'due_date': 'DUE_DATE',
}

# Detection thresholds
THRESHOLDS = {
    'duplicate_days': 7,           # Days to consider as potential duplicate
    'outlier_std': 3,              # Standard deviations for outlier detection
    'round_number_min': 1000,      # Minimum amount for round number flag
    'new_vendor_spike': 5000,      # First invoice threshold
    'inactive_days': 180,          # Days of inactivity before reactivation flag
    'min_vendor_invoices': 3,      # Minimum invoices to calculate vendor stats
}

# Risk weights for scoring
RISK_WEIGHTS = {
    'duplicate': 3,          # HIGH
    'outlier': 2,            # MEDIUM
    'round_number': 1,       # LOW
    'weekend': 2,            # MEDIUM
    'holiday': 2,            # MEDIUM
    'new_vendor_spike': 2,   # MEDIUM
    'inactive_vendor': 3,    # HIGH
}

# US Federal Holidays (fixed dates)
def get_holidays(year):
    """Generate list of US federal holidays for a given year."""
    holidays = [
        datetime(year, 1, 1),    # New Year's Day
        datetime(year, 7, 4),    # Independence Day
        datetime(year, 12, 25),  # Christmas
        datetime(year, 12, 31),  # New Year's Eve
    ]
    
    # Memorial Day - last Monday in May
    may_end = datetime(year, 5, 31)
    memorial_day = may_end - timedelta(days=(may_end.weekday() + 1) % 7)
    holidays.append(memorial_day)
    
    # Labor Day - first Monday in September
    sep_start = datetime(year, 9, 1)
    labor_day = sep_start + timedelta(days=(7 - sep_start.weekday()) % 7)
    holidays.append(labor_day)
    
    # Thanksgiving - fourth Thursday in November
    nov_start = datetime(year, 11, 1)
    first_thursday = nov_start + timedelta(days=(3 - nov_start.weekday() + 7) % 7)
    thanksgiving = first_thursday + timedelta(weeks=3)
    holidays.append(thanksgiving)
    
    return set(h.date() for h in holidays)


# ============================================================
# DETECTION FUNCTIONS
# ============================================================

def detect_duplicates(df, config, thresholds):
    """Flag potential duplicate invoices (same vendor + amount within N days)."""
    print("  → Detecting duplicates...")
    
    vendor_col = config['vendor_id']
    amount_col = config['invoice_amount']
    date_col = config['invoice_date']
    
    df['FLAG_DUPLICATE'] = 0
    
    # Group by vendor and amount (rounded to 2 decimals)
    df['_amount_key'] = df[amount_col].round(2)
    
    for (vendor, amount), group in df.groupby([vendor_col, '_amount_key']):
        if len(group) > 1:
            indices = group.index.tolist()
            dates = group[date_col].tolist()
            
            for i, idx1 in enumerate(indices):
                for j, idx2 in enumerate(indices[i+1:], i+1):
                    if pd.notna(dates[i]) and pd.notna(dates[j]):
                        day_diff = abs((dates[i] - dates[j]).days)
                        if day_diff <= thresholds['duplicate_days']:
                            df.loc[idx1, 'FLAG_DUPLICATE'] = 1
                            df.loc[idx2, 'FLAG_DUPLICATE'] = 1
    
    df.drop('_amount_key', axis=1, inplace=True)
    return df


def detect_outliers(df, config, thresholds):
    """Flag statistical outliers (amount > N std dev from vendor mean)."""
    print("  → Detecting statistical outliers...")
    
    vendor_col = config['vendor_id']
    amount_col = config['invoice_amount']
    
    df['FLAG_OUTLIER'] = 0
    
    # Calculate vendor statistics
    vendor_stats = df.groupby(vendor_col)[amount_col].agg(['mean', 'std', 'count'])
    vendor_stats = vendor_stats[vendor_stats['count'] >= thresholds['min_vendor_invoices']]
    
    for idx, row in df.iterrows():
        vendor = row[vendor_col]
        amount = row[amount_col]
        
        if vendor in vendor_stats.index:
            mean = vendor_stats.loc[vendor, 'mean']
            std = vendor_stats.loc[vendor, 'std']
            
            if std > 0 and abs(amount - mean) > thresholds['outlier_std'] * std:
                df.loc[idx, 'FLAG_OUTLIER'] = 1
    
    return df


def detect_round_numbers(df, config, thresholds):
    """Flag suspiciously round amounts (ends in 000 and > threshold)."""
    print("  → Detecting round number amounts...")
    
    amount_col = config['invoice_amount']
    
    df['FLAG_ROUND_NUMBER'] = 0
    
    mask = (
        (df[amount_col] >= thresholds['round_number_min']) &
        (df[amount_col] == df[amount_col].astype(int)) &
        (df[amount_col] % 1000 == 0)
    )
    
    df.loc[mask, 'FLAG_ROUND_NUMBER'] = 1
    return df


def detect_weekend_invoices(df, config, thresholds):
    """Flag invoices dated on Saturday or Sunday."""
    print("  → Detecting weekend invoices...")
    
    date_col = config['invoice_date']
    
    df['FLAG_WEEKEND'] = 0
    
    # Weekday: Monday=0, Sunday=6
    mask = df[date_col].dt.weekday.isin([5, 6])
    df.loc[mask, 'FLAG_WEEKEND'] = 1
    
    return df


def detect_holiday_invoices(df, config, thresholds):
    """Flag invoices dated on US federal holidays."""
    print("  → Detecting holiday invoices...")
    
    date_col = config['invoice_date']
    
    df['FLAG_HOLIDAY'] = 0
    
    # Get all years in data
    years = df[date_col].dt.year.dropna().unique()
    all_holidays = set()
    for year in years:
        all_holidays.update(get_holidays(int(year)))
    
    mask = df[date_col].dt.date.isin(all_holidays)
    df.loc[mask, 'FLAG_HOLIDAY'] = 1
    
    return df


def detect_new_vendor_spikes(df, config, thresholds):
    """Flag first invoice from vendor if > threshold amount."""
    print("  → Detecting new vendor spikes...")
    
    vendor_col = config['vendor_id']
    amount_col = config['invoice_amount']
    date_col = config['invoice_date']
    
    df['FLAG_NEW_VENDOR_SPIKE'] = 0
    
    # Find first invoice per vendor
    df_sorted = df.sort_values(date_col)
    first_invoices = df_sorted.groupby(vendor_col).first()
    
    for vendor, first_row in first_invoices.iterrows():
        if first_row[amount_col] > thresholds['new_vendor_spike']:
            # Find the index in original dataframe
            mask = (
                (df[vendor_col] == vendor) &
                (df[date_col] == first_row[date_col]) &
                (df[amount_col] == first_row[amount_col])
            )
            df.loc[mask, 'FLAG_NEW_VENDOR_SPIKE'] = 1
    
    return df


def detect_inactive_vendors(df, config, thresholds):
    """Flag invoices from vendors inactive for N+ days."""
    print("  → Detecting inactive vendor reactivation...")
    
    vendor_col = config['vendor_id']
    date_col = config['invoice_date']
    
    df['FLAG_INACTIVE_VENDOR'] = 0
    
    df_sorted = df.sort_values([vendor_col, date_col])
    
    for vendor, group in df_sorted.groupby(vendor_col):
        if len(group) >= 2:
            dates = group[date_col].tolist()
            indices = group.index.tolist()
            
            for i in range(1, len(dates)):
                if pd.notna(dates[i]) and pd.notna(dates[i-1]):
                    gap = (dates[i] - dates[i-1]).days
                    if gap > thresholds['inactive_days']:
                        df.loc[indices[i], 'FLAG_INACTIVE_VENDOR'] = 1
    
    return df


def calculate_anomaly_score(df, risk_weights):
    """Calculate composite anomaly score and summary."""
    print("  → Calculating anomaly scores...")
    
    df['ANOMALY_SCORE'] = (
        df['FLAG_DUPLICATE'] * risk_weights['duplicate'] +
        df['FLAG_OUTLIER'] * risk_weights['outlier'] +
        df['FLAG_ROUND_NUMBER'] * risk_weights['round_number'] +
        df['FLAG_WEEKEND'] * risk_weights['weekend'] +
        df['FLAG_HOLIDAY'] * risk_weights['holiday'] +
        df['FLAG_NEW_VENDOR_SPIKE'] * risk_weights['new_vendor_spike'] +
        df['FLAG_INACTIVE_VENDOR'] * risk_weights['inactive_vendor']
    )
    
    # Build anomaly type summary
    def get_anomaly_types(row):
        types = []
        if row['FLAG_DUPLICATE'] == 1: types.append('DUPLICATE')
        if row['FLAG_OUTLIER'] == 1: types.append('OUTLIER')
        if row['FLAG_ROUND_NUMBER'] == 1: types.append('ROUND_NUMBER')
        if row['FLAG_WEEKEND'] == 1: types.append('WEEKEND')
        if row['FLAG_HOLIDAY'] == 1: types.append('HOLIDAY')
        if row['FLAG_NEW_VENDOR_SPIKE'] == 1: types.append('NEW_VENDOR_SPIKE')
        if row['FLAG_INACTIVE_VENDOR'] == 1: types.append('INACTIVE_VENDOR')
        return ';'.join(types) if types else ''
    
    df['ANOMALY_TYPES'] = df.apply(get_anomaly_types, axis=1)
    
    # Risk category
    def get_risk_category(score):
        if score >= 5: return 'HIGH'
        elif score >= 3: return 'MEDIUM'
        elif score >= 1: return 'LOW'
        else: return 'CLEAN'
    
    df['RISK_CATEGORY'] = df['ANOMALY_SCORE'].apply(get_risk_category)
    
    return df


def generate_report(df, output_dir):
    """Generate summary report."""
    print("  → Generating summary report...")
    
    total_records = len(df)
    flagged_records = len(df[df['ANOMALY_SCORE'] > 0])
    
    report = {
        'Metric': [],
        'Value': [],
        'Percentage': []
    }
    
    # Summary stats
    report['Metric'].append('Total Records')
    report['Value'].append(total_records)
    report['Percentage'].append('100.00%')
    
    report['Metric'].append('Records with Anomalies')
    report['Value'].append(flagged_records)
    report['Percentage'].append(f'{flagged_records/total_records*100:.2f}%')
    
    report['Metric'].append('Clean Records')
    report['Value'].append(total_records - flagged_records)
    report['Percentage'].append(f'{(total_records-flagged_records)/total_records*100:.2f}%')
    
    # Risk distribution
    report['Metric'].append('---')
    report['Value'].append('---')
    report['Percentage'].append('---')
    
    for risk in ['HIGH', 'MEDIUM', 'LOW']:
        count = len(df[df['RISK_CATEGORY'] == risk])
        report['Metric'].append(f'{risk} Risk')
        report['Value'].append(count)
        report['Percentage'].append(f'{count/total_records*100:.2f}%')
    
    # Anomaly breakdown
    report['Metric'].append('---')
    report['Value'].append('---')
    report['Percentage'].append('---')
    
    flag_cols = [
        ('FLAG_DUPLICATE', 'Potential Duplicates'),
        ('FLAG_OUTLIER', 'Statistical Outliers'),
        ('FLAG_ROUND_NUMBER', 'Round Number Amounts'),
        ('FLAG_WEEKEND', 'Weekend Invoices'),
        ('FLAG_HOLIDAY', 'Holiday Invoices'),
        ('FLAG_NEW_VENDOR_SPIKE', 'New Vendor Spikes'),
        ('FLAG_INACTIVE_VENDOR', 'Inactive Vendor Reactivation'),
    ]
    
    for col, name in flag_cols:
        count = df[col].sum()
        report['Metric'].append(name)
        report['Value'].append(int(count))
        report['Percentage'].append(f'{count/total_records*100:.2f}%')
    
    report_df = pd.DataFrame(report)
    
    # Save CSV
    report_df.to_csv(output_dir / 'anomaly_report.csv', index=False)
    
    # Generate HTML report
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AP Invoice Anomaly Detection Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
            h2 {{ color: #666; margin-top: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background: #4CAF50; color: white; }}
            tr:hover {{ background: #f5f5f5; }}
            .high {{ color: #d32f2f; font-weight: bold; }}
            .medium {{ color: #f57c00; font-weight: bold; }}
            .low {{ color: #388e3c; }}
            .summary-box {{ background: #e8f5e9; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .stat {{ font-size: 24px; font-weight: bold; color: #333; }}
            .timestamp {{ color: #999; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 AP Invoice Anomaly Detection Report</h1>
            <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <div class="summary-box">
                <p><span class="stat">{total_records:,}</span> records analyzed</p>
                <p><span class="stat">{flagged_records:,}</span> anomalies detected ({flagged_records/total_records*100:.1f}%)</p>
            </div>
            
            <h2>Risk Distribution</h2>
            <table>
                <tr><th>Risk Level</th><th>Count</th><th>Percentage</th></tr>
                <tr class="high"><td>🔴 HIGH (Score ≥ 5)</td><td>{len(df[df['RISK_CATEGORY']=='HIGH']):,}</td><td>{len(df[df['RISK_CATEGORY']=='HIGH'])/total_records*100:.2f}%</td></tr>
                <tr class="medium"><td>🟡 MEDIUM (Score 3-4)</td><td>{len(df[df['RISK_CATEGORY']=='MEDIUM']):,}</td><td>{len(df[df['RISK_CATEGORY']=='MEDIUM'])/total_records*100:.2f}%</td></tr>
                <tr class="low"><td>🟢 LOW (Score 1-2)</td><td>{len(df[df['RISK_CATEGORY']=='LOW']):,}</td><td>{len(df[df['RISK_CATEGORY']=='LOW'])/total_records*100:.2f}%</td></tr>
            </table>
            
            <h2>Anomaly Breakdown</h2>
            <table>
                <tr><th>Anomaly Type</th><th>Count</th><th>% of Total</th><th>Risk Weight</th></tr>
                <tr><td>Potential Duplicates</td><td>{int(df['FLAG_DUPLICATE'].sum()):,}</td><td>{df['FLAG_DUPLICATE'].sum()/total_records*100:.2f}%</td><td class="high">HIGH (3)</td></tr>
                <tr><td>Statistical Outliers</td><td>{int(df['FLAG_OUTLIER'].sum()):,}</td><td>{df['FLAG_OUTLIER'].sum()/total_records*100:.2f}%</td><td class="medium">MEDIUM (2)</td></tr>
                <tr><td>Round Number Amounts</td><td>{int(df['FLAG_ROUND_NUMBER'].sum()):,}</td><td>{df['FLAG_ROUND_NUMBER'].sum()/total_records*100:.2f}%</td><td class="low">LOW (1)</td></tr>
                <tr><td>Weekend Invoices</td><td>{int(df['FLAG_WEEKEND'].sum()):,}</td><td>{df['FLAG_WEEKEND'].sum()/total_records*100:.2f}%</td><td class="medium">MEDIUM (2)</td></tr>
                <tr><td>Holiday Invoices</td><td>{int(df['FLAG_HOLIDAY'].sum()):,}</td><td>{df['FLAG_HOLIDAY'].sum()/total_records*100:.2f}%</td><td class="medium">MEDIUM (2)</td></tr>
                <tr><td>New Vendor Spikes</td><td>{int(df['FLAG_NEW_VENDOR_SPIKE'].sum()):,}</td><td>{df['FLAG_NEW_VENDOR_SPIKE'].sum()/total_records*100:.2f}%</td><td class="medium">MEDIUM (2)</td></tr>
                <tr><td>Inactive Vendor Reactivation</td><td>{int(df['FLAG_INACTIVE_VENDOR'].sum()):,}</td><td>{df['FLAG_INACTIVE_VENDOR'].sum()/total_records*100:.2f}%</td><td class="high">HIGH (3)</td></tr>
            </table>
            
            <h2>Recommended Actions</h2>
            <ul>
                <li><strong>HIGH Risk:</strong> Immediate review required - potential fraud or significant errors</li>
                <li><strong>MEDIUM Risk:</strong> Review within 48 hours - possible issues requiring investigation</li>
                <li><strong>LOW Risk:</strong> Batch review weekly - minor flags for awareness</li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    with open(output_dir / 'anomaly_report.html', 'w') as f:
        f.write(html)
    
    return report_df


# ============================================================
# MAIN EXECUTION
# ============================================================

def run_detection(input_file, output_dir=None):
    """Run all anomaly detection on input file."""
    
    input_path = Path(input_file)
    
    if output_dir is None:
        output_dir = input_path.parent
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print("AP INVOICE ANOMALY DETECTOR")
    print(f"{'='*60}")
    print(f"Input: {input_path}")
    print(f"Output: {output_dir}")
    print(f"{'='*60}\n")
    
    # Load data
    print("Loading data...")
    if input_path.suffix.lower() == '.csv':
        df = pd.read_csv(input_path)
    elif input_path.suffix.lower() in ['.xlsx', '.xls', '.xlsm']:
        df = pd.read_excel(input_path)
    else:
        raise ValueError(f"Unsupported file type: {input_path.suffix}")
    
    print(f"  Loaded {len(df):,} records\n")
    
    # Parse dates
    date_col = CONFIG['invoice_date']
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    
    # Run all detection rules
    print("Running detection rules...")
    df = detect_duplicates(df, CONFIG, THRESHOLDS)
    df = detect_outliers(df, CONFIG, THRESHOLDS)
    df = detect_round_numbers(df, CONFIG, THRESHOLDS)
    df = detect_weekend_invoices(df, CONFIG, THRESHOLDS)
    df = detect_holiday_invoices(df, CONFIG, THRESHOLDS)
    df = detect_new_vendor_spikes(df, CONFIG, THRESHOLDS)
    df = detect_inactive_vendors(df, CONFIG, THRESHOLDS)
    
    # Calculate scores
    df = calculate_anomaly_score(df, RISK_WEIGHTS)
    
    # Generate outputs
    print("\nGenerating outputs...")
    
    # Save full results
    output_file = output_dir / 'invoices_with_flags.csv'
    df.to_csv(output_file, index=False)
    print(f"  → Full results: {output_file}")
    
    # Save flagged only
    flagged = df[df['ANOMALY_SCORE'] > 0].copy()
    flagged_file = output_dir / 'flagged_invoices.csv'
    flagged.to_csv(flagged_file, index=False)
    print(f"  → Flagged records: {flagged_file} ({len(flagged):,} records)")
    
    # Generate report
    report_df = generate_report(df, output_dir)
    print(f"  → Report: {output_dir / 'anomaly_report.html'}")
    
    # Print summary
    print(f"\n{'='*60}")
    print("DETECTION COMPLETE")
    print(f"{'='*60}")
    print(f"Total Records:     {len(df):,}")
    print(f"Flagged Records:   {len(flagged):,} ({len(flagged)/len(df)*100:.1f}%)")
    print(f"High Risk:         {len(df[df['RISK_CATEGORY']=='HIGH']):,}")
    print(f"Medium Risk:       {len(df[df['RISK_CATEGORY']=='MEDIUM']):,}")
    print(f"Low Risk:          {len(df[df['RISK_CATEGORY']=='LOW']):,}")
    print(f"{'='*60}\n")
    
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AP Invoice Anomaly Detector')
    parser.add_argument('input_file', help='Path to input CSV or Excel file')
    parser.add_argument('-o', '--output', help='Output directory (default: same as input)')
    
    args = parser.parse_args()
    
    run_detection(args.input_file, args.output)
