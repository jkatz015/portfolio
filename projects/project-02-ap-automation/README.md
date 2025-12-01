# Project 2: Invoice Anomaly Detection

> Excel-based tool using Power Query and VBA to automatically flag suspicious AP transactions.

**Status:** Not Started

---

## Problem Statement

Accounts Payable teams process thousands of invoices monthly, and manual review can't catch everything:
- Duplicate payments cost companies 0.1-0.5% of revenue
- Fraudulent invoices often slip through
- Unusual patterns go unnoticed until audit
- Manual spot-checking is time-consuming and inconsistent

**Goal:** Build an Excel tool that automatically scans AP transaction data and flags suspicious invoices for review.

---

## Questions We're Answering

1. **Are there duplicate invoices?** (same vendor + amount + date)
2. **Are there unusual amounts?** (outliers vs. vendor history)
3. **Are there suspicious timing patterns?** (invoices on weekends, holidays, month-end)
4. **Are there round number red flags?** ($5,000.00 exactly — common fraud indicator)
5. **Are there vendor anomalies?** (new vendors, inactive vendors suddenly billing)
6. **What's the overall health of the AP process?** (summary metrics)

---

## Dataset

**Source:** Kaggle AP/Invoice transaction dataset (TBD)

| Column | Description |
|--------|-------------|
| invoice_id | Unique invoice identifier |
| vendor_id | Vendor identifier |
| vendor_name | Vendor name |
| invoice_date | Date of invoice |
| due_date | Payment due date |
| amount | Invoice amount |
| gl_code | General ledger code |
| payment_date | Date paid (if paid) |
| status | Paid, pending, etc. |

---

## Tools & Skills Demonstrated

### Technical
- Excel Power Query (data cleaning, transformation)
- Excel VBA (automation)
- Conditional formatting (visual flags)
- Pivot tables (summary analysis)
- Statistical outlier detection

### Financial/Business Concepts
- AP workflow and controls
- Duplicate payment detection
- Fraud indicators (Benford's Law, round numbers)
- Vendor management
- Internal controls

---

## Methodology

### 1. Data Import & Cleaning (Power Query)
- [ ] Import transaction data
- [ ] Standardize vendor names
- [ ] Parse dates correctly
- [ ] Handle missing values
- [ ] Create calculated columns (day of week, month, etc.)

### 2. Anomaly Detection Rules
- [ ] **Duplicates:** Same vendor + amount + date (±3 days)
- [ ] **Outliers:** Amount > 2 standard deviations from vendor average
- [ ] **Round numbers:** Amounts ending in 000 or 00
- [ ] **Weekend invoices:** Invoice date falls on Saturday/Sunday
- [ ] **New vendors:** Vendor not in historical master list
- [ ] **Inactive vendors:** No activity in 6+ months, then sudden invoice

### 3. VBA Automation
- [ ] One-click button to run all checks
- [ ] Generate flagged items on new sheet
- [ ] Color-code by severity (red = high, yellow = medium)
- [ ] Summary count of flags by type

### 4. Dashboard
- [ ] Total invoices scanned
- [ ] Number of flags by category
- [ ] Top flagged vendors
- [ ] Trend over time (if multiple periods)

---

## Deliverables

- [ ] `Invoice_Anomaly_Detector.xlsm` — Main Excel tool with Power Query + VBA
- [ ] `data/sample_transactions.csv` — Sample dataset
- [ ] `reports/anomaly_detection_report.pdf` — Methodology documentation
- [ ] `README.md` — This file with instructions

---

## How It Works (User Flow)

```
1. User opens Excel file
2. Pastes or imports AP transaction data
3. Clicks "Run Anomaly Check" button
4. Tool scans data and flags suspicious items
5. Results appear on "Flagged Items" sheet
6. Dashboard shows summary metrics
```

---

## Business Interpretation

*To be completed after development*

- Number of duplicates caught
- Estimated cost savings
- Time saved vs. manual review
- False positive rate

---

## Future Enhancements

- Benford's Law analysis for first-digit distribution
- Machine learning anomaly detection (Python integration)
- Email alert for high-severity flags
- Integration with accounting software exports
- Historical trend tracking

---

## References

- [ACFE Fraud Prevention](https://www.acfe.com/)
- [Benford's Law for Fraud Detection](https://en.wikipedia.org/wiki/Benford%27s_law)
- [Excel Power Query Documentation](https://docs.microsoft.com/en-us/power-query/)
