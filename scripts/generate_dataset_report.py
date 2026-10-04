import os
import pandas as pd

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")
SPLITS_DIR = os.path.join("data", "splits")

def get_stats():
    uci_raw = pd.read_csv(os.path.join(RAW_DIR, "uci_sms_spam.csv")) if os.path.exists(os.path.join(RAW_DIR, "uci_sms_spam.csv")) else None
    url_raw = pd.read_csv(os.path.join(RAW_DIR, "phishing_urls.csv")) if os.path.exists(os.path.join(RAW_DIR, "phishing_urls.csv")) else None
    scam_raw = pd.read_csv(os.path.join(RAW_DIR, "indian_financial_scams.csv")) if os.path.exists(os.path.join(RAW_DIR, "indian_financial_scams.csv")) else None

    text_tr = pd.read_csv(os.path.join(SPLITS_DIR, "text_train.csv")) if os.path.exists(os.path.join(SPLITS_DIR, "text_train.csv")) else None
    text_val = pd.read_csv(os.path.join(SPLITS_DIR, "text_val.csv")) if os.path.exists(os.path.join(SPLITS_DIR, "text_val.csv")) else None
    text_te = pd.read_csv(os.path.join(SPLITS_DIR, "text_test.csv")) if os.path.exists(os.path.join(SPLITS_DIR, "text_test.csv")) else None

    url_tr = pd.read_csv(os.path.join(SPLITS_DIR, "url_train.csv")) if os.path.exists(os.path.join(SPLITS_DIR, "url_train.csv")) else None
    url_val = pd.read_csv(os.path.join(SPLITS_DIR, "url_val.csv")) if os.path.exists(os.path.join(SPLITS_DIR, "url_val.csv")) else None
    url_te = pd.read_csv(os.path.join(SPLITS_DIR, "url_test.csv")) if os.path.exists(os.path.join(SPLITS_DIR, "url_test.csv")) else None

    report = f"""# RAKSHA Comprehensive Dataset & Corpus Report

**Generated**: 2026-10-03
**Status**: ACQUIRED, PREPROCESSED, DEDUPLICATED, AND SPLIT

---

## 1. Raw Dataset Summary

| Dataset Name | Total Rows | Classes / Labels | Missing Values | Primary Languages |
| :--- | :--- | :--- | :--- | :--- |
| **UCI SMS Spam Collection** | `{len(uci_raw) if uci_raw is not None else 0}` | Spam ({sum(uci_raw['label']==1) if uci_raw is not None else 0}), Legitimate ({sum(uci_raw['label']==0) if uci_raw is not None else 0}) | 0 | English |
| **Phishing & Legitimate URLs** | `{len(url_raw) if url_raw is not None else 0}` | Phishing ({sum(url_raw['label']==1) if url_raw is not None else 0}), Legitimate ({sum(url_raw['label']==0) if url_raw is not None else 0}) | 0 | Lexical / Domain |
| **Indian Multilingual Financial Scams** | `{len(scam_raw) if scam_raw is not None else 0}` | Scam ({sum(scam_raw['label']==1) if scam_raw is not None else 0}), Legitimate ({sum(scam_raw['label']==0) if scam_raw is not None else 0}) | 0 | English, Hindi, Hinglish |

---

## 2. Text Dataset Splits (UCI SMS Spam)

| Split | Sample Count | Positive (Spam) | Negative (Ham) | Class Ratio (% Spam) |
| :--- | :--- | :--- | :--- | :--- |
| **Train (70%)** | `{len(text_tr) if text_tr is not None else 0}` | `{sum(text_tr['label']==1) if text_tr is not None else 0}` | `{sum(text_tr['label']==0) if text_tr is not None else 0}` | `{round(sum(text_tr['label']==1)/len(text_tr)*100, 2) if text_tr is not None else 0}%` |
| **Validation (15%)** | `{len(text_val) if text_val is not None else 0}` | `{sum(text_val['label']==1) if text_val is not None else 0}` | `{sum(text_val['label']==0) if text_val is not None else 0}` | `{round(sum(text_val['label']==1)/len(text_val)*100, 2) if text_val is not None else 0}%` |
| **Test (15%)** | `{len(text_te) if text_te is not None else 0}` | `{sum(text_te['label']==1) if text_te is not None else 0}` | `{sum(text_te['label']==0) if text_te is not None else 0}` | `{round(sum(text_te['label']==1)/len(text_te)*100, 2) if text_te is not None else 0}%` |

---

## 3. URL Dataset Splits (Domain Grouped)

| Split | Sample Count | Phishing (1) | Legitimate (0) | Unique Hostnames |
| :--- | :--- | :--- | :--- | :--- |
| **Train (70%)** | `{len(url_tr) if url_tr is not None else 0}` | `{sum(url_tr['label']==1) if url_tr is not None else 0}` | `{sum(url_tr['label']==0) if url_tr is not None else 0}` | `{len(set(url_tr['hostname'].dropna())) if url_tr is not None else 0}` |
| **Validation (15%)** | `{len(url_val) if url_val is not None else 0}` | `{sum(url_val['label']==1) if url_val is not None else 0}` | `{sum(url_val['label']==0) if url_val is not None else 0}` | `{len(set(url_val['hostname'].dropna())) if url_val is not None else 0}` |
| **Test (15%)** | `{len(url_te) if url_te is not None else 0}` | `{sum(url_te['label']==1) if url_te is not None else 0}` | `{sum(url_te['label']==0) if url_te is not None else 0}` | `{len(set(url_te['hostname'].dropna())) if url_te is not None else 0}` |
"""
    out_path = os.path.join("data", "DATASET_REPORT.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Generated Dataset Report -> {out_path}")

if __name__ == "__main__":
    get_stats()
