# Project 2: AP/Invoice Automation

> Automated invoice processing pipeline with OCR extraction, validation, and anomaly detection.

**Status:** Not Started

---

## Problem Statement

Accounts Payable teams manually process hundreds of invoices monthly, leading to:
- Data entry errors (2-5% error rate typical)
- Duplicate payments
- Missed early payment discounts
- Slow processing times (days vs. hours)
- Fraud vulnerability

**Goal:** Build an automated pipeline that extracts invoice data, validates against vendor master, and flags anomalies.

---

## Dataset

**Source:** Synthetic invoice dataset (TBD)

| Component | Description |
|-----------|-------------|
| Invoice images/PDFs | Sample invoices for OCR |
| Vendor master | Approved vendors with payment terms |
| Historical payments | Past invoice payments for anomaly baseline |

---

## Tools & Skills Demonstrated

### Technical
- Python (pandas, numpy)
- OCR (pytesseract, OpenCV)
- Regular expressions for data extraction
- Anomaly detection (Isolation Forest, statistical methods)
- Streamlit (demo app)

### Financial Concepts
- AP workflow automation
- Three-way matching (PO, receipt, invoice)
- Duplicate detection
- Vendor validation
- Payment term optimization

---

## Methodology

### 1. Invoice Data Extraction
- [ ] Set up OCR pipeline (pytesseract)
- [ ] Extract key fields:
  - Vendor name
  - Invoice number
  - Invoice date
  - Due date
  - Line items
  - Total amount
- [ ] Handle multiple invoice formats

### 2. Data Validation
- [ ] Match vendor to master file
- [ ] Validate invoice number format
- [ ] Check for duplicates
- [ ] Verify GL code mapping
- [ ] Flag missing required fields

### 3. Anomaly Detection
- [ ] Unusual amounts (vs. vendor history)
- [ ] Suspicious timing patterns
- [ ] Duplicate invoice detection
- [ ] New vendor alerts

### 4. Demo Application
- [ ] Streamlit upload interface
- [ ] Real-time extraction display
- [ ] Validation status dashboard
- [ ] Export to CSV/Excel

---

## Deliverables

- [ ] `notebooks/01_ocr_extraction.ipynb` — OCR pipeline development
- [ ] `notebooks/02_validation_rules.ipynb` — Validation logic
- [ ] `notebooks/03_anomaly_detection.ipynb` — Anomaly model
- [ ] `src/invoice_processor.py` — Main processing module
- [ ] `src/validators.py` — Validation functions
- [ ] `app/streamlit_app.py` — Demo application
- [ ] `reports/ap_automation_report.pdf` — Process documentation

---

## Business Interpretation

*To be completed after development*

- Processing time savings
- Error reduction rate
- Anomaly detection accuracy
- ROI calculation

---

## Future Enhancements

- Integration with ERP systems (SAP, Oracle)
- Machine learning for GL code prediction
- Email ingestion for invoice receipt
- Approval workflow automation
- Advanced document AI (Azure Form Recognizer, AWS Textract)

---

## References

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [OpenCV Python](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
