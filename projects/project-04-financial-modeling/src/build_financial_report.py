"""
Financial Model Report Generator
================================
Generates an HTML report from the financial model outputs.

Usage:
    python build_financial_report.py

Output:
    - ../reports/financial_model_report.html
"""

import pandas as pd
from datetime import datetime
from pathlib import Path

# File paths
BASE_DIR = Path(__file__).parent.parent
MODEL_FILE = BASE_DIR / "model" / "financial_model.xlsx"
OUTPUT_DIR = BASE_DIR / "reports"

def format_currency(val):
    if val >= 1_000_000:
        return f"${val/1_000_000:.2f}M"
    elif val >= 1_000:
        return f"${val/1_000:.1f}K"
    else:
        return f"${val:,.0f}"

def format_pct(val):
    return f"{val*100:.1f}%"

def main():
    print("Building Financial Model Report...")

    # Load data from Excel
    income_stmt = pd.read_excel(MODEL_FILE, sheet_name='Income Statement')
    balance_sheet = pd.read_excel(MODEL_FILE, sheet_name='Balance Sheet')
    cash_flow = pd.read_excel(MODEL_FILE, sheet_name='Cash Flow')
    ratios = pd.read_excel(MODEL_FILE, sheet_name='Key Ratios')
    exec_summary = pd.read_excel(MODEL_FILE, sheet_name='Executive Summary')
    assumptions = pd.read_excel(MODEL_FILE, sheet_name='Assumptions')

    # Get scenario data
    base = exec_summary[exec_summary['Scenario'] == 'Base'].iloc[0]
    upside = exec_summary[exec_summary['Scenario'] == 'Upside'].iloc[0]
    downside = exec_summary[exec_summary['Scenario'] == 'Downside'].iloc[0]

    # Get base scenario income statement for trend
    base_income = income_stmt[income_stmt['Scenario'] == 'Base']

    # Build HTML
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Model - 3-Statement Analysis</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            color: #333;
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
            border-bottom: 2px solid #4CAF50;
            margin-bottom: 30px;
        }}

        .header h1 {{
            font-size: 2.5em;
            font-weight: 400;
            margin-bottom: 10px;
            color: #333;
        }}

        .header .subtitle {{
            color: #666;
            font-size: 1.1em;
        }}

        .timestamp {{
            color: #999;
            font-size: 0.9em;
            margin-top: 10px;
        }}

        /* Scenario Cards */
        .scenario-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}

        .scenario-card {{
            background: white;
            border-radius: 8px;
            padding: 25px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #ddd;
        }}

        .scenario-card.base {{
            border-left-color: #4CAF50;
        }}

        .scenario-card.upside {{
            border-left-color: #2196F3;
        }}

        .scenario-card.downside {{
            border-left-color: #f57c00;
        }}

        .scenario-title {{
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #ddd;
        }}

        .scenario-title.base {{ color: #4CAF50; }}
        .scenario-title.upside {{ color: #2196F3; }}
        .scenario-title.downside {{ color: #f57c00; }}

        .metric-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}

        .metric-label {{
            color: #666;
            font-size: 0.9em;
        }}

        .metric-value {{
            font-weight: 600;
            color: #333;
        }}

        /* KPI Cards */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .kpi-card {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .kpi-label {{
            font-size: 0.8em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }}

        .kpi-value {{
            font-size: 1.8em;
            font-weight: 600;
            color: #333;
        }}

        .kpi-subtext {{
            font-size: 0.8em;
            color: #999;
            margin-top: 5px;
        }}

        /* Section styling */
        .section {{
            background: white;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .section h2 {{
            font-size: 1.3em;
            font-weight: 500;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #4CAF50;
        }}

        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th {{
            text-align: left;
            padding: 12px 15px;
            background: #4CAF50;
            color: white;
            font-weight: 500;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
            color: #333;
        }}

        tr:hover td {{
            background: #f5f5f5;
        }}

        .text-right {{
            text-align: right;
        }}

        .positive {{
            color: #388e3c;
        }}

        .negative {{
            color: #d32f2f;
        }}

        /* Two column layout */
        .two-col {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
        }}

        /* Assumptions table */
        .assumptions-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
        }}

        .assumption-item {{
            background: #e8f5e9;
            padding: 15px;
            border-radius: 8px;
        }}

        .assumption-label {{
            font-size: 0.85em;
            color: #666;
            margin-bottom: 5px;
        }}

        .assumption-value {{
            font-size: 1.1em;
            color: #333;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 30px;
            color: #999;
            font-size: 0.9em;
            border-top: 1px solid #ddd;
            margin-top: 30px;
        }}

        /* Responsive */
        @media (max-width: 992px) {{
            .scenario-grid {{
                grid-template-columns: 1fr;
            }}
            .two-col {{
                grid-template-columns: 1fr;
            }}
            .assumptions-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>Financial Model Report</h1>
            <div class="subtitle">3-Statement Model with Scenario Analysis | Restaurant Business</div>
            <div class="timestamp">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        </div>

        <!-- Executive Summary KPIs -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Base Case Revenue (2028)</div>
                <div class="kpi-value">{format_currency(base['Year_5_Revenue'])}</div>
                <div class="kpi-subtext">5Y CAGR: {format_pct(base['Revenue_CAGR'])}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Base Case EBITDA (2028)</div>
                <div class="kpi-value">{format_currency(base['Year_5_EBITDA'])}</div>
                <div class="kpi-subtext">Margin: {format_pct(base['Year_5_EBITDA_Margin'])}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Base Case Net Income (2028)</div>
                <div class="kpi-value">{format_currency(base['Year_5_Net_Income'])}</div>
                <div class="kpi-subtext">Margin: {format_pct(base['Year_5_Net_Margin'])}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">5Y Total FCF (Base)</div>
                <div class="kpi-value">{format_currency(base['5Y_Total_Free_Cash_Flow'])}</div>
                <div class="kpi-subtext">Cumulative</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Ending Cash (2028)</div>
                <div class="kpi-value">{format_currency(base['Year_5_Ending_Cash'])}</div>
                <div class="kpi-subtext">Base Case</div>
            </div>
        </div>

        <!-- Scenario Comparison -->
        <div class="scenario-grid">
            <div class="scenario-card base">
                <div class="scenario-title base">Base Case</div>
                <div class="metric-row">
                    <span class="metric-label">Year 5 Revenue</span>
                    <span class="metric-value">{format_currency(base['Year_5_Revenue'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Year 5 EBITDA</span>
                    <span class="metric-value">{format_currency(base['Year_5_EBITDA'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">EBITDA Margin</span>
                    <span class="metric-value">{format_pct(base['Year_5_EBITDA_Margin'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Year 5 Net Income</span>
                    <span class="metric-value">{format_currency(base['Year_5_Net_Income'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Net Margin</span>
                    <span class="metric-value">{format_pct(base['Year_5_Net_Margin'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">5Y Total Net Income</span>
                    <span class="metric-value">{format_currency(base['5Y_Total_Net_Income'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">5Y Total FCF</span>
                    <span class="metric-value">{format_currency(base['5Y_Total_Free_Cash_Flow'])}</span>
                </div>
            </div>

            <div class="scenario-card upside">
                <div class="scenario-title upside">Upside Case</div>
                <div class="metric-row">
                    <span class="metric-label">Year 5 Revenue</span>
                    <span class="metric-value">{format_currency(upside['Year_5_Revenue'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Year 5 EBITDA</span>
                    <span class="metric-value">{format_currency(upside['Year_5_EBITDA'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">EBITDA Margin</span>
                    <span class="metric-value">{format_pct(upside['Year_5_EBITDA_Margin'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Year 5 Net Income</span>
                    <span class="metric-value">{format_currency(upside['Year_5_Net_Income'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Net Margin</span>
                    <span class="metric-value">{format_pct(upside['Year_5_Net_Margin'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">5Y Total Net Income</span>
                    <span class="metric-value">{format_currency(upside['5Y_Total_Net_Income'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">5Y Total FCF</span>
                    <span class="metric-value">{format_currency(upside['5Y_Total_Free_Cash_Flow'])}</span>
                </div>
            </div>

            <div class="scenario-card downside">
                <div class="scenario-title downside">Downside Case</div>
                <div class="metric-row">
                    <span class="metric-label">Year 5 Revenue</span>
                    <span class="metric-value">{format_currency(downside['Year_5_Revenue'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Year 5 EBITDA</span>
                    <span class="metric-value">{format_currency(downside['Year_5_EBITDA'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">EBITDA Margin</span>
                    <span class="metric-value">{format_pct(downside['Year_5_EBITDA_Margin'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Year 5 Net Income</span>
                    <span class="metric-value">{format_currency(downside['Year_5_Net_Income'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Net Margin</span>
                    <span class="metric-value">{format_pct(downside['Year_5_Net_Margin'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">5Y Total Net Income</span>
                    <span class="metric-value">{format_currency(downside['5Y_Total_Net_Income'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">5Y Total FCF</span>
                    <span class="metric-value">{format_currency(downside['5Y_Total_Free_Cash_Flow'])}</span>
                </div>
            </div>
        </div>

        <!-- Income Statement Projection (Base Case) -->
        <div class="section">
            <h2>Income Statement Projection - Base Case</h2>
            <table>
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th class="text-right">2024</th>
                        <th class="text-right">2025</th>
                        <th class="text-right">2026</th>
                        <th class="text-right">2027</th>
                        <th class="text-right">2028</th>
                    </tr>
                </thead>
                <tbody>
"""

    # Add income statement rows
    metrics = [
        ('Revenue', 'Revenue'),
        ('COGS', 'COGS'),
        ('Gross Profit', 'Gross_Profit'),
        ('Total OpEx', 'Total_OpEx'),
        ('EBITDA', 'EBITDA'),
        ('Net Income', 'Net_Income'),
    ]

    for label, col in metrics:
        html += f"<tr><td>{label}</td>"
        for _, row in base_income.iterrows():
            val = row[col]
            html += f'<td class="text-right">{format_currency(val)}</td>'
        html += "</tr>"

    # Add margin rows
    html += f"<tr><td>Gross Margin %</td>"
    for _, row in base_income.iterrows():
        html += f'<td class="text-right">{format_pct(row["Gross_Margin_Pct"])}</td>'
    html += "</tr>"

    html += f"<tr><td>EBITDA Margin %</td>"
    for _, row in base_income.iterrows():
        html += f'<td class="text-right">{format_pct(row["EBITDA_Margin_Pct"])}</td>'
    html += "</tr>"

    html += f"<tr><td>Net Margin %</td>"
    for _, row in base_income.iterrows():
        html += f'<td class="text-right">{format_pct(row["Net_Margin_Pct"])}</td>'
    html += "</tr>"

    html += """
                </tbody>
            </table>
        </div>

        <!-- Key Ratios -->
        <div class="section">
            <h2>Key Financial Ratios - Base Case (2028)</h2>
"""

    # Get 2028 ratios for base case
    base_ratios = ratios[(ratios['Scenario'] == 'Base') & (ratios['Year'] == 2028)].iloc[0]

    html += """
            <div class="assumptions-grid">
                <div class="assumption-item">
                    <div class="assumption-label">Gross Margin</div>
                    <div class="assumption-value">""" + format_pct(base_ratios['Gross_Margin']) + """</div>
                </div>
                <div class="assumption-item">
                    <div class="assumption-label">EBITDA Margin</div>
                    <div class="assumption-value">""" + format_pct(base_ratios['EBITDA_Margin']) + """</div>
                </div>
                <div class="assumption-item">
                    <div class="assumption-label">Net Margin</div>
                    <div class="assumption-value">""" + format_pct(base_ratios['Net_Margin']) + """</div>
                </div>
                <div class="assumption-item">
                    <div class="assumption-label">Prime Cost %</div>
                    <div class="assumption-value">""" + format_pct(base_ratios['Prime_Cost_Pct']) + """</div>
                </div>
                <div class="assumption-item">
                    <div class="assumption-label">Current Ratio</div>
                    <div class="assumption-value">""" + f"{base_ratios['Current_Ratio']:.2f}x" + """</div>
                </div>
                <div class="assumption-item">
                    <div class="assumption-label">Quick Ratio</div>
                    <div class="assumption-value">""" + f"{base_ratios['Quick_Ratio']:.2f}x" + """</div>
                </div>
                <div class="assumption-item">
                    <div class="assumption-label">Debt to Equity</div>
                    <div class="assumption-value">""" + f"{base_ratios['Debt_to_Equity']:.2f}x" + """</div>
                </div>
                <div class="assumption-item">
                    <div class="assumption-label">Interest Coverage</div>
                    <div class="assumption-value">""" + f"{base_ratios['Interest_Coverage']:.1f}x" + """</div>
                </div>
                <div class="assumption-item">
                    <div class="assumption-label">ROE</div>
                    <div class="assumption-value">""" + format_pct(base_ratios['ROE']) + """</div>
                </div>
            </div>
        </div>

        <!-- Model Assumptions -->
        <div class="section">
            <h2>Key Assumptions - Base Case</h2>
            <table>
                <thead>
                    <tr>
                        <th>Assumption</th>
                        <th class="text-right">2024</th>
                        <th class="text-right">2025</th>
                        <th class="text-right">2026</th>
                        <th class="text-right">2027</th>
                        <th class="text-right">2028</th>
                    </tr>
                </thead>
                <tbody>
"""

    base_assumptions = assumptions[assumptions['Scenario'] == 'Base']

    html += "<tr><td>Revenue Growth</td>"
    for _, row in base_assumptions.iterrows():
        html += f'<td class="text-right">{format_pct(row["Revenue_Growth"])}</td>'
    html += "</tr>"

    html += "<tr><td>Food Cost %</td>"
    for _, row in base_assumptions.iterrows():
        html += f'<td class="text-right">{format_pct(row["Food_Cost_Pct"])}</td>'
    html += "</tr>"

    html += "<tr><td>Labor Cost %</td>"
    for _, row in base_assumptions.iterrows():
        html += f'<td class="text-right">{format_pct(row["Labor_Cost_Pct"])}</td>'
    html += "</tr>"

    html += "<tr><td>CapEx</td>"
    for _, row in base_assumptions.iterrows():
        html += f'<td class="text-right">{format_currency(row["CapEx"])}</td>'
    html += "</tr>"

    html += """
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>Financial Model Report | 5-Year Projection (2024-2028) | 3 Scenarios Analyzed</p>
            <p style="margin-top: 10px;">Built with Python | Portfolio Project</p>
        </div>
    </div>
</body>
</html>
"""

    # Save report
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / 'financial_model_report.html'
    with open(output_file, 'w') as f:
        f.write(html)

    print(f"Saved: {output_file}")

    # Also copy as index.html
    index_file = BASE_DIR / 'index.html'
    with open(index_file, 'w') as f:
        f.write(html)

    print(f"Saved: {index_file}")
    print("Done!")

if __name__ == '__main__':
    main()
