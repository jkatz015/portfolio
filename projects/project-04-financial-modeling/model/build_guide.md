# Financial Model Build Guide

## Project Overview

This is a **3-Statement Financial Model** for a restaurant business with scenario analysis.

**Company Profile:** Urban Bistro - Full-service restaurant
**Historical Data:** 2022-2023 (24 months)
**Projections:** 2024-2028 (5 years)
**Scenarios:** Base, Upside, Downside

---

## Files Created

```
project-04-financial-modeling/
├── data/
│   └── historical_financials.csv    # 24 months of POS/accounting data
├── model/
│   ├── assumptions.md               # All model assumptions documented
│   ├── financial_model.xlsx         # Excel output (7 tabs)
│   └── build_guide.md               # This file
└── src/
    └── financial_model.py           # Python model engine
```

---

## How to Run

```bash
cd ~/repos/portfolio/projects/project-04-financial-modeling
python3 src/financial_model.py
```

This regenerates `model/financial_model.xlsx` with updated projections.

---

## Excel Output Tabs

| Tab | Contents |
|-----|----------|
| **Assumptions** | Revenue growth, cost %, CapEx by scenario/year |
| **Historical** | 2022-2023 actual financials |
| **Income Statement** | Revenue → Net Income (all 3 scenarios) |
| **Balance Sheet** | Assets, Liabilities, Equity (all 3 scenarios) |
| **Cash Flow** | Operating, Investing, Financing cash flows |
| **Key Ratios** | Margins, liquidity, leverage, returns |
| **Sensitivity** | What-if analysis on growth & food cost |
| **Scenario Comparison** | Net Income by scenario side-by-side |

---

## Model Results Summary

### Base Case (2028)
- Revenue: $2.77M
- EBITDA: $438K (15.8% margin)
- Net Income: $297K (10.7% margin)

### Upside Case (2028)
- Revenue: $3.47M
- EBITDA: $699K (20.1% margin)
- Net Income: $475K (13.7% margin)

### Downside Case (2028)
- Revenue: $2.40M
- EBITDA: $254K (10.6% margin)
- Net Income: $164K (6.8% margin)

---

## Key Assumptions

### Revenue Growth
| Scenario | 2024 | 2025 | 2026 | 2027 | 2028 |
|----------|------|------|------|------|------|
| Base | 6% | 5% | 4.5% | 4% | 3.5% |
| Upside | 10% | 12% | 10% | 8% | 7% |
| Downside | 2% | 0% | 1% | 2% | 3% |

### Cost Structure (Base Case)
- Food Cost: 31.5% → 30.5%
- Beverage Cost: 9% → 8.5%
- Labor Cost: 28% → 27%
- Prime Cost Target: <65%

### Capital Expenditures
| Scenario | 5-Year Total |
|----------|--------------|
| Base | $105,000 |
| Upside | $275,000 (expansion) |
| Downside | $60,000 (maintenance only) |

---

## Key Insights

1. **Prime Cost Control is Critical**
   - Upside achieves 63% prime cost
   - Downside hits 72% (unsustainable)

2. **Expansion ROI (Upside)**
   - $275K CapEx investment
   - Yields $475K annual net income by Year 5
   - Strong payback if growth materializes

3. **Downside Stress Test**
   - Even with 0% growth and cost inflation
   - Business remains profitable ($164K)
   - Validates business model resilience

4. **EBITDA Margin Range**
   - 10.6% (Downside) to 20.1% (Upside)
   - Base case 15.8% is healthy for full-service restaurant

---

## How to Modify

### Change Assumptions
Edit `src/financial_model.py` → `SCENARIOS` dictionary:

```python
SCENARIOS = {
    'Base': {
        'revenue_growth': [0.06, 0.05, 0.045, 0.04, 0.035],
        'food_cost_pct': [0.315, 0.31, 0.31, 0.305, 0.305],
        ...
    },
}
```

### Add New Scenario
Add a new key to the `SCENARIOS` dictionary:

```python
'Aggressive': {
    'revenue_growth': [0.15, 0.15, 0.12, 0.10, 0.08],
    ...
}
```

### Change Starting Balance Sheet
Edit `STARTING_BALANCE` dictionary:

```python
STARTING_BALANCE = {
    'cash': 85000,
    'accounts_receivable': 18000,
    ...
}
```

---

## Why Python Instead of Excel?

1. **Reproducibility** - Same inputs always produce same outputs
2. **Version Control** - Track changes in git
3. **Scalability** - Easy to add scenarios, years, complexity
4. **No Formula Errors** - Logic is explicit, not hidden in cells
5. **Automation** - Can run monthly with new actuals
6. **Testing** - Can write unit tests for calculations

---

## Real-World Usage

In practice, you would:

1. Export actuals from POS/accounting system monthly
2. Update `historical_financials.csv`
3. Adjust assumptions based on trends
4. Run `python financial_model.py`
5. Share updated Excel with stakeholders
6. Use for:
   - Board presentations
   - Bank loan applications
   - Investor decks
   - Annual budget planning
   - Strategic decision-making

---

## References

- Model assumptions based on National Restaurant Association benchmarks
- Prime cost targets from industry best practices
- Working capital days typical for restaurant operations
