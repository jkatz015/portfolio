# Project 3: Executive Finance Dashboard

> CFO-ready interactive dashboard for financial KPIs, trends, and variance analysis.

**Status:** Complete

---

## Problem Statement

Executives need real-time visibility into financial performance but often rely on:
- Static Excel reports
- Delayed month-end closes
- Scattered data across systems
- Non-interactive presentations

**Goal:** Build an interactive dashboard that provides instant insights into revenue, margins, expenses, and forecasts.

---

## Dataset

**Source:** [Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) (9,994 records)

| Column | Description |
|--------|-------------|
| Order Date | Transaction date |
| Sales | Revenue amount |
| Profit | Profit amount |
| Category | Product category |
| Region | Geographic region |
| Segment | Consumer, Corporate, Home Office |

---

## Tools & Skills Demonstrated

### Technical
- Python (pandas, numpy)
- HTML/CSS dashboard generation
- Data modeling and calculated fields
- Automated report generation
- Dashboard design principles

### Financial Concepts
- Revenue analysis
- Gross margin calculation
- YoY variance analysis
- KPI frameworks
- Trend analysis
- Customer and product profitability

---

## Dashboard Components

### Executive Summary
- [x] Total Revenue with YoY growth
- [x] Total Profit with YoY growth
- [x] Gross Margin %
- [x] Total Orders and Customers
- [x] Average Order Value
- [x] Average Ship Days

### Revenue Breakdown
- [x] Revenue by Region (bar chart)
- [x] Revenue by Category (bar chart)
- [x] Revenue by Segment (bar chart)

### Performance Tables
- [x] Regional Performance (Revenue, Profit, Margin, Orders)
- [x] Category Performance (Revenue, Profit, Margin, Orders)
- [x] Top 10 Customers by Revenue
- [x] Top 10 Products by Revenue
- [x] Shipping Performance by Mode

---

## Results

Analysis of 9,994 transactions (2014-2017):

| Metric | Value |
|--------|-------|
| Total Revenue | $2.3M |
| Total Profit | $286K |
| Gross Margin | 12.5% |
| Total Orders | 5,009 |
| Total Customers | 793 |
| Avg Order Value | $459 |
| YoY Revenue Growth | +20.4% |
| YoY Profit Growth | +14.2% |

### By Region
| Region | Revenue | Margin |
|--------|---------|--------|
| West | $725K | 14.0% |
| East | $678K | 13.0% |
| Central | $501K | 6.0% |
| South | $392K | 14.0% |

### By Category
| Category | Revenue | Margin |
|----------|---------|--------|
| Technology | $836K | 14.5% |
| Furniture | $742K | 2.5% |
| Office Supplies | $719K | 17.5% |

---

## Design Principles

1. **Clean layout** — Dark theme, clear hierarchy
2. **Consistent colors** — Professional blue palette
3. **Mobile responsive** — Works on all devices
4. **Visual KPIs** — Cards with trend indicators
5. **Drill-down tables** — Summary to detail
6. **Clear labels** — No ambiguity

---

## Deliverables

- [x] `data/superstore_tableau_ready.csv` — Prepared dataset with calculated fields
- [x] `data/prep_data.py` — Data transformation script
- [x] `data/build_kpi_dashboard.py` — Dashboard generator script
- [x] `reports/executive_dashboard.html` — Interactive HTML dashboard
- [x] `reports/kpi_metrics.csv` — Summary KPIs
- [x] `reports/region_metrics.csv` — Regional breakdown
- [x] `reports/category_metrics.csv` — Category breakdown

---

## Usage

```bash
# Prepare data
cd data
python prep_data.py

# Generate dashboard
python build_kpi_dashboard.py
```

Output files are saved to `reports/` folder.

---

## Business Interpretation

- **West region leads** — Highest revenue ($725K) with healthy 14% margin
- **Central region underperforms** — Only 6% margin despite $501K revenue
- **Furniture margins are thin** — 2.5% margin vs 17.5% for Office Supplies
- **Strong YoY growth** — 20.4% revenue growth indicates healthy business trajectory
- **Technology drives profit** — Highest revenue category with good margins

### Recommended Actions
1. Investigate Central region cost structure
2. Review Furniture pricing strategy
3. Focus on Office Supplies for margin improvement
4. Maintain Technology investment

---

## Future Enhancements

- Real-time data connection
- Automated refresh schedule
- Tableau/Power BI version
- Custom alerts/notifications
- Streamlit interactive version

---

## References

- [Tableau Best Practices](https://www.tableau.com/learn/whitepapers/tableau-visual-guidebook)
- [Financial Dashboard Examples](https://public.tableau.com/app/search/vizzes/finance)
- [pandas Documentation](https://pandas.pydata.org/docs/)
