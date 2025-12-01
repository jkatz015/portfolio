# Project 1: Pizza Sales Revenue Forecasting

> Analyzing pizza restaurant sales patterns and forecasting 7-day revenue using R.

**Status:** In Progress

---

## Problem Statement

A pizza restaurant wants to better understand their sales patterns and forecast future revenue to improve:
- Staffing decisions (when to schedule more employees)
- Inventory planning (how much dough, cheese, toppings to order)
- Operational efficiency (prep schedules, delivery capacity)

**Goal:** Answer key business questions about sales patterns and forecast the next 7 days of revenue.

---

## Questions We're Answering

1. **What will total sales revenue be for the next 7 days?**
2. What are the peak hours for orders?
3. Which day of the week has the highest sales?
4. What is the best-selling pizza?
5. What is the most popular pizza size?
6. What is the average order value?

---

## Dataset

**Source:** [Kaggle Pizza Restaurant Sales](https://www.kaggle.com/datasets/shilongzhuang/pizza-sales)

| Column | Description |
|--------|-------------|
| order_id | Unique order identifier |
| order_date | Date of order (2015) |
| order_time | Time of order |
| pizza_name | Name of pizza |
| pizza_category | Category (Classic, Veggie, etc.) |
| pizza_size | Size (S, M, L, XL, XXL) |
| quantity | Number of pizzas |
| unit_price | Price per pizza |
| total_price | Revenue for line item |

**Size:** 48,620 rows × 12 columns (full year 2015)

---

## Tools & Skills Demonstrated

### Technical
- R (tidyverse, lubridate, ggplot2)
- Time series analysis
- Data visualization
- RStudio / R Markdown

### Business Concepts
- Revenue forecasting
- Peak hour analysis
- Product mix analysis
- Average order value
- Day-of-week patterns

---

## Methodology

### 1. Exploratory Data Analysis
- [x] Load and clean data
- [x] Identify peak hours for orders
- [x] Analyze sales by day of week
- [x] Find best-selling pizzas
- [x] Determine most popular pizza size
- [x] Calculate average order value

### 2. Forecasting (Next Step)
- [ ] Aggregate daily revenue
- [ ] Build time series forecast
- [ ] Predict next 7 days
- [ ] Evaluate forecast accuracy

---

## Deliverables

- [x] `notebooks/01_eda.Rmd` — Exploratory data analysis
- [ ] `notebooks/02_forecasting.Rmd` — 7-day revenue forecast
- [ ] `reports/pizza_sales_report.pdf` — Final report

---

## Key Findings

| Question | Answer | Business Action |
|----------|--------|-----------------|
| Peak hours? | 12pm (lunch), 5-7pm (dinner) | Full staffing during peak hours |
| Best day of week? | Friday | Run promotions on slow days (Sunday) |
| Best-selling pizza? | The Classic Deluxe Pizza | Ensure ingredients always stocked |
| Most popular size? | Large (L) - 46% of sales | Optimize Large pizza pricing and inventory |
| Average order value? | $38.31 | Set delivery minimum at $35-40 |

---

## Future Enhancements

- Add holiday/event features to forecast
- Build interactive Streamlit dashboard
- Automate weekly forecast reports

---

## References

- [Kaggle Pizza Sales Dataset](https://www.kaggle.com/datasets/shilongzhuang/pizza-sales)
- [R for Data Science](https://r4ds.had.co.nz/)
