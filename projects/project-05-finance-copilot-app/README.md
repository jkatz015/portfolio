# Project 5: D.A.T.A.

> **D**ashboard & **A**nalytics **T**ool for **A**ccounting

Streamlit application that automates financial data analysis: upload, clean, analyze, visualize, export.

**Status:** Complete

**Live Demo:** https://finance-copilot-production-38c7.up.railway.app (Password: `demo2024`)

---

## Problem Statement

Financial analysts spend 60-80% of their time on:
- Data cleaning and formatting
- Manual categorization
- Repetitive calculations
- Creating the same charts repeatedly

**Goal:** Build D.A.T.A. to automate routine analysis tasks, letting analysts focus on insights and decisions.

---

## Features

### 1. Data Upload
- CSV/Excel file upload
- Automatic column type detection (date, amount, category, entity)
- Smart data preview

### 2. Auto-Detection & Cleaning
- Identifies column types by name patterns and data analysis
- Parses dates and extracts Year/Month components
- Cleans currency formatting ($, commas, parentheses for negatives)
- Handles missing values

### 3. KPI Dashboard
- Total amounts (positive/negative breakdown)
- Transaction count
- Average, median, min, max values
- Real-time calculations

### 4. Interactive Visualizations
- **Trend Analysis**: Monthly line charts with area fills
- **Category Breakdown**: Pie charts and horizontal bar charts
- **Top Entities**: Ranked bar charts for vendors/customers
- **Monthly Comparison**: Year-over-year comparison when multiple years present

### 5. Export Options
- Processed data (CSV)
- Summary report (CSV)
- Excel workbook with multiple sheets

### 6. Security
- Password protection via environment variable
- Configurable for production deployment

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Streamlit |
| Charts | Plotly |
| Data Processing | Pandas, NumPy |
| Excel Export | openpyxl |
| Deployment | Railway |
| Styling | Custom CSS |

---

## Design System

### Colors
- **Primary**: Navy #1E3A5F
- **Accent**: Teal #2DD4BF
- **Success**: Green #10B981
- **Warning**: Amber #F59E0B
- **Error**: Red #EF4444

### Typography
- **Headlines**: Inter (600-700 weight)
- **Body**: Inter (400-500 weight)
- **Numbers**: JetBrains Mono

---

## Project Structure

```
project-05-data-app/
├── app/
│   ├── streamlit_app.py    # Main application (350+ lines)
│   ├── styles.py           # Custom CSS and Plotly config
│   └── utils.py            # Data processing utilities
├── requirements.txt        # Python dependencies
├── Procfile               # Railway start command
├── railway.json           # Railway configuration
├── .gitignore
└── README.md
```

---

## Quick Start

### Local Development

```bash
cd projects/project-05-data-app
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Default password: `demo2024`

### Railway Deployment

1. Connect GitHub repo to Railway
2. Set environment variable: `APP_PASSWORD=your_secure_password`
3. Railway auto-deploys using Procfile

---

## Supported Data

| Type | Examples |
|------|----------|
| File Formats | CSV, Excel (.xlsx, .xls) |
| Transaction Data | AP invoices, AR receipts, bank statements |
| Budget Data | Department budgets, cost center reports |
| Sales Data | Revenue by category, product sales |

---

## Key Functions

### `detect_column_types(df)`
Auto-detects columns by:
- Name pattern matching (date, amount, category keywords)
- Data type analysis (numeric vs object)
- Cardinality analysis for category vs entity distinction

### `clean_data(df, date_col, amount_col)`
- Parses dates and extracts time components
- Removes currency symbols and handles parentheses notation
- Adds derived columns: Year, Month, Month_Name, Year_Month

### `calculate_kpis(df, amount_col)`
Computes: total, positive sum, negative sum, average, median, min, max, count, std dev

### Chart Functions
- `create_trend_chart()` - Monthly trend with area fill
- `create_category_chart()` - Pie or horizontal bar
- `create_entity_chart()` - Top N ranking
- `create_monthly_comparison_chart()` - Year-over-year bars

---

## Business Value

1. **Time Savings**: Eliminates repetitive data prep and chart creation
2. **Consistency**: Same analysis framework applied to any dataset
3. **Accessibility**: Non-technical users can perform complex analysis
4. **Portability**: Works with any financial CSV/Excel data

---

## Future Enhancements

- [ ] AI-powered categorization (LLM integration)
- [ ] Natural language queries
- [ ] PDF report generation
- [ ] Multi-user authentication
- [ ] Database integration
- [ ] API endpoints for automation

---

## References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Railway Deployment](https://docs.railway.app/)
- [Plotly Python](https://plotly.com/python/)
