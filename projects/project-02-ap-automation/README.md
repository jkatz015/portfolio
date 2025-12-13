# Project 2: Invoice Anomaly Detection

> Python-based tool to automatically flag suspicious AP transactions using statistical analysis.

**Status:** Complete

---

## Problem Statement

Accounts Payable teams process thousands of invoices monthly, and manual review can't catch everything:
- Duplicate payments cost companies 0.1-0.5% of revenue
- Fraudulent invoices often slip through
- Unusual patterns go unnoticed until audit
- Manual spot-checking is time-consuming and inconsistent

**Goal:** Build a Python tool that automatically scans AP transaction data and flags suspicious invoices for review.

---

## Questions We're Answering

1. **Are there duplicate invoices?** (same vendor + amount within 7 days)
2. **Are there unusual amounts?** (outliers > 3 std dev from vendor average)
3. **Are there suspicious timing patterns?** (invoices on weekends, holidays)
4. **Are there round number red flags?** ($1,000+ amounts ending in 000)
5. **Are there vendor anomalies?** (new vendors with large first invoices, inactive vendors suddenly billing)
6. **What's the overall health of the AP process?** (summary metrics and risk scores)

---

## Dataset

**Source:** Synthetic AP transaction dataset (50,000 records)

| Column | Description |
|--------|-------------|
| INVOICE_ID | Unique invoice identifier |
| VENDOR_ID | Vendor identifier |
| VENDOR_NAME | Vendor name |
| INVOICE_DATE | Date of invoice |
| DUE_DATE | Payment due date |
| INVOICE_AMOUNT | Invoice amount |

---

## Tools & Skills Demonstrated

### Technical
- Python (pandas, numpy)
- Statistical outlier detection
- Automated report generation (HTML/CSV)
- Command-line tool development
- Data validation and cleaning

### Financial/Business Concepts
- AP workflow and controls
- Duplicate payment detection
- Fraud indicators (round numbers, timing anomalies)
- Vendor management
- Internal controls
- Risk scoring methodology

---

## Methodology

### 1. Data Import & Cleaning
- Load CSV/Excel transaction data
- Parse dates correctly
- Handle missing values
- Standardize data types

### 2. Anomaly Detection Rules

| Rule | Description | Risk Weight |
|------|-------------|-------------|
| **Duplicates** | Same vendor + amount within 7 days | HIGH (3) |
| **Outliers** | Amount > 3 std dev from vendor mean | MEDIUM (2) |
| **Round Numbers** | Amounts ≥$1,000 ending in 000 | LOW (1) |
| **Weekend Invoices** | Invoice dated Saturday/Sunday | MEDIUM (2) |
| **Holiday Invoices** | Invoice dated on US federal holiday | MEDIUM (2) |
| **New Vendor Spike** | First invoice from vendor > $5,000 | MEDIUM (2) |
| **Inactive Vendor** | No activity in 180+ days, then invoice | HIGH (3) |

### 3. Risk Scoring
- Each flag adds weighted points to anomaly score
- Risk categories: HIGH (≥5), MEDIUM (3-4), LOW (1-2), CLEAN (0)
- Multiple flags on same invoice compound the risk

### 4. Report Generation
- Flagged invoices exported to CSV
- Summary statistics and metrics
- HTML report with visual breakdown

---

## Results

Analysis of 50,000 AP transactions:

| Metric | Value |
|--------|-------|
| Total Records | 50,000 |
| Flagged Records | 11,111 (22.2%) |
| High Risk | 11 |
| Medium Risk | 494 |
| Low Risk | 10,606 |

---

## Deliverables

- [x] `src/ap_anomaly_detector.py` — Main Python detection script
- [x] `data/ap_transactions_clean.csv` — Sample dataset
- [x] `reports/anomaly_report.html` — Visual summary report
- [x] `reports/flagged_invoices.csv` — Flagged records for review
- [x] `reports/invoices_with_flags.csv` — Full dataset with flags

---

## Usage

```bash
python ap_anomaly_detector.py input_file.csv -o output_directory/
```

**Arguments:**
- `input_file` — Path to CSV or Excel file with AP transactions
- `-o, --output` — Output directory (default: same as input)

**Output Files:**
- `flagged_invoices.csv` — Records with anomalies only
- `invoices_with_flags.csv` — All records with flag columns
- `anomaly_report.csv` — Summary statistics
- `anomaly_report.html` — Formatted HTML report

---

## Business Interpretation

- **22.2% flag rate** — Reasonable for initial screening (expect 5-10% to be true positives)
- **11 high-risk items** — Require immediate review (potential duplicates or reactivated vendors)
- **Time savings** — Analysis of 50,000 records completes in seconds vs. hours of manual review
- **Consistent application** — Same rules applied to every invoice, no sampling bias

---

## Future Enhancements

- Benford's Law analysis for first-digit distribution
- Machine learning anomaly detection (Isolation Forest, LOF)
- Email alerts for high-severity flags
- Integration with accounting software APIs
- Historical trend tracking and dashboards
- Streamlit web interface

---

## References

- [ACFE Fraud Prevention](https://www.acfe.com/)
- [Benford's Law for Fraud Detection](https://en.wikipedia.org/wiki/Benford%27s_law)
- [pandas Documentation](https://pandas.pydata.org/docs/)
