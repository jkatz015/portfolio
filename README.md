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
| 3 | [Executive Dashboard](./projects/project-03-executive-dashboard/) | **Complete** | Tableau dashboard with KPIs, revenue trends, profitability analysis |
| 4 | [Financial Modeling](./projects/project-04-financial-modeling/) | **Complete** | Python 3-statement model with Base/Upside/Downside scenarios |
| 5 | [Finance Copilot App](./projects/project-05-finance-copilot-app/) | Not Started | Streamlit app: upload → clean → analyze → visualize |

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
- [x] Build Tableau dashboard:
  - KPI tiles (Revenue, Profit, Margin)
  - Revenue trend over time
  - Profit by category
  - Sales vs Profit scatter plot
- [x] Create step-by-step build guide

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

### Phase 6: Project 5 — Finance Copilot App
- [ ] Design app architecture
- [ ] Build Streamlit interface
- [ ] Implement data processing pipeline
- [ ] Add visualization components
- [ ] Deploy to Railway
- [ ] Document API/usage

### Phase 7: Portfolio Website
- [ ] Design wireframes in Figma
- [ ] Build UI components
- [ ] Develop Next.js site
- [ ] Deploy to Railway
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

## Portfolio Website Plan

### Pages
1. **Home** — Hero section, brief intro, featured projects
2. **About** — Background, skills, experience
3. **Projects** — Grid of project cards with previews
4. **Individual Project Pages** — Deep dive into each project
5. **Contact** — Email, LinkedIn, GitHub links

### Design Goals
- Clean, minimal typography
- Professional color palette (finance/tech aesthetic)
- Modular components
- Mobile responsive
- Fast loading

### Tech Stack
- **Design**: Figma
- **Framework**: Next.js (React)
- **Styling**: Tailwind CSS
- **Hosting**: Railway

---

## Progress Tracker

| Date | Milestone | Notes |
|------|-----------|-------|
| Nov 2024 | Repository created | Initial setup |
| Nov 2024 | Project 1 complete | Pizza sales forecasting with R |
| Dec 2024 | Project 2 complete | Python AP anomaly detector (50K records, 7 detection rules) |
| Dec 2024 | Project 3 complete | Tableau executive dashboard (KPIs, trends, scatter) |
| Dec 2024 | Project 4 complete | Python 3-statement financial model with scenarios |
| TBD | Project 5 complete | Finance Copilot |
| TBD | Website live | Portfolio deployed |

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
