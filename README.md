# Financial Analytics Portfolio

> **Single Source of Truth (SSOT)** — Master plan for building a comprehensive financial data analyst portfolio.

---

## Portfolio Overview

### Purpose
Develop a professional portfolio demonstrating expertise in:
- Financial modeling & forecasting
- AP/AR automation
- Business intelligence & dashboarding
- Data cleaning & validation
- Applied AI/ML workflows
- Python/R analytics
- SQL data modeling
- Operational finance

### Target Outcome
4-6 deep, end-to-end projects that prove technical competence and business acumen to recruiters and hiring managers.

---

## Project List

| # | Project | Status | Description |
|---|---------|--------|-------------|
| 1 | [Pizza Sales Revenue Forecasting](./projects/project-01-revenue-forecasting/) | **Complete** | Time series forecasting using R (ARIMA) |
| 2 | [Invoice Anomaly Detection](./projects/project-02-ap-automation/) | **Complete** | Python anomaly detector for AP transactions (duplicates, outliers, weekend/holiday flags) |
| 3 | [Executive Dashboard](./projects/project-03-executive-dashboard/) | **Complete** | Python KPI dashboard with revenue trends, profitability analysis |
| 4 | [Financial Modeling](./projects/project-04-financial-modeling/) | **Complete** | Python 3-statement model with Base/Upside/Downside scenarios |
| 5 | [D.A.T.A.](./projects/project-05-DATA/) | **Complete** | Dashboard & Analytics Tool for Accounting — Streamlit app deployed on Railway |

---

## Project Template (Standard Structure)

Each project follows this structure:

```
project-XX-name/
├── data/
│   ├── raw/           # Original datasets
│   └── processed/     # Cleaned/transformed data
├── notebooks/         # Jupyter/R notebooks
├── src/               # Python/R scripts
├── dashboards/        # Tableau workbooks, screenshots
├── reports/           # Final writeups, PDFs
└── README.md          # Project-specific documentation
```

### Required Sections in Each Project README

1. **Problem Statement** — Clear business problem and why it matters
2. **Dataset Overview** — Source, contents, columns, known issues
3. **Tools & Skills** — Technologies and financial concepts demonstrated
4. **Data Cleaning & Prep** — Missing values, validation, feature engineering
5. **Analysis/Model/Automation** — Technical workflow details
6. **Visualizations** — Charts, dashboards, KPI summaries
7. **Business Interpretation** — Translated into decision-making language
8. **Deliverables** — Links to notebooks, dashboards, apps
9. **Future Enhancements** — Potential improvements

---

## Execution Plan

### Phase 1: Setup
- [x] Create folder structure
- [x] Initialize GitHub repository
- [x] Document dependencies
- [x] Set up Python/R environments

### Phase 2: Project 1 — Pizza Sales Revenue Forecasting
- [x] Download Kaggle pizza sales dataset
- [x] Exploratory data analysis (6 business questions)
- [x] Build forecasting model (ARIMA)
- [x] Evaluate model accuracy
- [x] Create visualizations
- [x] Write project README
- [x] Generate final report (HTML + PDF)
- [x] Document lessons learned (Christmas seasonality)

### Phase 3: Project 2 — Invoice Anomaly Detection
- [x] Find AP/invoice transaction dataset (50K records)
- [x] Build Python anomaly detection script
- [x] Create anomaly detection rules:
  - Duplicate invoices (same vendor + amount within 7 days)
  - Statistical outliers (>3 std dev from vendor mean)
  - Round number amounts (fraud indicator)
  - Weekend/holiday invoice dates
  - New vendor spikes (first invoice > $5K)
  - Inactive vendor reactivation (>180 days gap)
- [x] Generate HTML report and CSV outputs
- [x] Document methodology (python_vs_excel_summary.txt)

### Phase 4: Project 3 — Executive Dashboard
- [x] Download Superstore dataset from Kaggle
- [x] Prep data with Python (calculated fields, margins)
- [x] Build Python KPI dashboard:
  - KPI tiles (Revenue, Profit, Margin, Orders)
  - Revenue trend over time
  - Profit by category breakdown
  - Top products and regions analysis
- [x] Generate interactive HTML report

### Phase 5: Project 4 — Financial Modeling
- [x] Create historical restaurant financials (24 months)
- [x] Build Python 3-statement model:
  - Income Statement
  - Balance Sheet
  - Cash Flow Statement
- [x] Implement 3 scenarios (Base/Upside/Downside)
- [x] Create 5-year projections (2024-2028)
- [x] Document assumptions (assumptions.md)
- [x] Generate formatted Excel workbook with Executive Summary
- [x] Add sensitivity analysis

### Phase 6: Project 5 — D.A.T.A. (Dashboard & Analytics Tool for Accounting)
- [x] Design app architecture
- [x] Build Streamlit interface with password protection
- [x] Implement smart column detection (dates, amounts, categories, entities)
- [x] Add data cleaning pipeline (currencies, dates, missing values)
- [x] Create KPI dashboard with real-time calculations
- [x] Add interactive Plotly visualizations (trends, pie charts, bar charts)
- [x] Deploy to Railway (live at https://finance-copilot-production-38c7.up.railway.app)
- [x] Create landing page with demo password for hiring managers

### Phase 7: Portfolio Website (GitHub Pages)
- [x] Configure GitHub Pages with Jekyll
- [x] Apply Leap Day theme for professional appearance
- [x] Create index.html landing pages for each project
- [x] Ensure all reports visible directly on project pages
- [ ] Connect custom domain (optional)

---

## Technical Dependencies

### Python
```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0
scikit-learn>=1.2.0
statsmodels>=0.14.0
prophet>=1.1.0
streamlit>=1.22.0
pytesseract>=0.3.10
opencv-python>=4.7.0
python-dotenv>=1.0.0
```

### R (for forecasting)
```
tidyverse
lubridate
forecast
readxl
scales
knitr
kableExtra
```

### Tools
- Python 3.11+
- R 4.3+
- RStudio
- VS Code / Cursor
- Tableau Public or Power BI
- Figma (design)
- Railway (deployment)
- GitHub (version control)

---

## Portfolio Website

### Live Site
**GitHub Pages**: https://jkatz015.github.io/portfolio

### Structure
1. **Home** — README renders as main landing page
2. **Project Pages** — Each project has its own index.html with interactive reports
3. **Live Demo** — D.A.T.A. app hosted on Railway with demo access

### Design
- Leap Day Jekyll theme for professional appearance
- Light theme across all reports (#f5f5f5 background, #4CAF50 green accents)
- Mobile responsive
- Fast loading static HTML

### Tech Stack
- **Theme**: Jekyll Leap Day
- **Reports**: Python-generated HTML with Plotly
- **App Hosting**: Railway (Streamlit)
- **Version Control**: GitHub

---

## Progress Tracker

| Date | Milestone | Notes |
|------|-----------|-------|
| Nov 2024 | Repository created | Initial setup |
| Nov 2024 | Project 1 complete | Pizza sales forecasting with R |
| Dec 2024 | Project 2 complete | Python AP anomaly detector (50K records, 7 detection rules) |
| Dec 2024 | Project 3 complete | Python KPI executive dashboard (revenue trends, profitability) |
| Dec 2024 | Project 4 complete | Python 3-statement financial model with scenarios |
| Dec 2024 | Project 5 complete | D.A.T.A. Streamlit app deployed to Railway |
| Dec 2024 | GitHub Pages live | Leap Day theme, all projects with landing pages |

---

## Resources

### Datasets
- [Kaggle Pizza Sales](https://www.kaggle.com/datasets/shilongzhuang/pizza-sales) — Project 1
- [Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
- [Synthetic Invoice Data](https://www.kaggle.com/datasets) (TBD)

### Learning
- [R for Data Science](https://r4ds.had.co.nz/)
- [Forecast Package Documentation](https://pkg.robjhyndman.com/forecast/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Tableau Public](https://public.tableau.com/)

---

## License

This portfolio is for educational and professional demonstration purposes.

---

*Last updated: December 2024*
