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
| 1 | [Revenue Forecasting](./projects/project-01-revenue-forecasting/) | Not Started | Time series forecasting using retail sales data |
| 2 | [AP/Invoice Automation](./projects/project-02-ap-automation/) | Not Started | OCR + validation + anomaly detection pipeline |
| 3 | [Executive Dashboard](./projects/project-03-executive-dashboard/) | Not Started | CFO-ready Tableau/Power BI dashboard |
| 4 | [Financial Modeling](./projects/project-04-financial-modeling/) | Not Started | Multi-scenario 3-5 year projection model |
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

### Phase 1: Setup (Current)
- [x] Create folder structure
- [x] Initialize GitHub repository
- [ ] Document dependencies
- [ ] Set up Python/R environments

### Phase 2: Project 1 — Revenue Forecasting
- [ ] Download Kaggle retail sales dataset
- [ ] Exploratory data analysis
- [ ] Build forecasting models (ARIMA, Prophet)
- [ ] Compare model accuracy
- [ ] Create visualizations
- [ ] Write project README
- [ ] Generate report/case study

### Phase 3: Project 2 — AP Automation
- [ ] Obtain invoice dataset
- [ ] Build OCR extraction pipeline
- [ ] Create validation rules
- [ ] Implement anomaly detection
- [ ] Build Streamlit demo app
- [ ] Document workflow

### Phase 4: Project 3 — Executive Dashboard
- [ ] Select dataset (Superstore or similar)
- [ ] Design KPI framework
- [ ] Build Tableau/Power BI dashboard
- [ ] Publish to Tableau Public
- [ ] Create screenshots for portfolio

### Phase 5: Project 4 — Financial Modeling
- [ ] Build Excel + Python hybrid model
- [ ] Implement scenario analysis
- [ ] Create 3-5 year projections
- [ ] Document assumptions
- [ ] Generate report

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
forecast
tsibble
fable
ggplot2
```

### Tools
- Python 3.11+
- R 4.3+
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
| TBD | Repository created | Initial setup |
| TBD | Project 1 complete | Revenue forecasting |
| TBD | Project 2 complete | AP automation |
| TBD | Project 3 complete | Dashboard |
| TBD | Project 4 complete | Financial model |
| TBD | Project 5 complete | Finance Copilot |
| TBD | Website live | Portfolio deployed |

---

## Resources

### Datasets
- [Kaggle Store Sales Forecasting](https://www.kaggle.com/competitions/store-sales-time-series-forecasting)
- [Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
- [Synthetic Invoice Data](https://www.kaggle.com/datasets) (TBD)

### Learning
- [Prophet Documentation](https://facebook.github.io/prophet/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Tableau Public](https://public.tableau.com/)

---

## License

This portfolio is for educational and professional demonstration purposes.

---

*Last updated: November 2024*
