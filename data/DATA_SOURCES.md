# RAKSHA Data Sources Documentation

**Document Version**: 1.0.0
**Last Updated**: 2026-10-03
**Maintainer**: RAKSHA Data & ML Engineering Team

---

## Overview & Provenance Policy

This document registers all public datasets, live threat feeds, and curated corpora used by RAKSHA for training, benchmarking, calibration, and real-time intelligence verification.

> [!IMPORTANT]
> **Data Scientific Integrity Rule**: RAKSHA strictly distinguishes between naturally occurring real-world public datasets, live intelligence feeds, and curated benchmark examples. No synthetic or curated data is ever represented as a naturally occurring real-world dataset.

---

## 1. UCI SMS Spam Collection Dataset

- **Dataset Name**: UCI SMS Spam Collection
- **Source**: UCI Machine Learning Repository
- **Official URL**: https://archive.ics.uci.edu/dataset/228/sms+spam+collection
- **Download Method**: Direct automated HTTP stream unzip (`scripts/download_datasets.py`)
- **License**: Public Domain / CC BY 4.0
- **Size**: 5,574 labeled messages
- **Language**: English
- **Labels**: Binary (`0`: Legitimate / Ham, `1`: Spam / Social Engineering)
- **Provenance**: Collected from public mobile phone communication research corpora (NUS SMS Corpus, Grumbletext, Caroline Tag's PhD Thesis).
- **Collection Methodology**: Mobile spam reports and non-spam SMS contributions.
- **Known Limitations**: English language focus; pre-dates modern messaging apps like WhatsApp/Telegram.
- **Classification**: Real-World Dataset
- **Intended Use**: Primary baseline text classification dataset for TF-IDF + Logistic Regression and transformer initial evaluation.
- **Preprocessing**: Deduplication, lowercasing, ASCII normalization, whitespace stripping.
- **Train/Val/Test Usage**: 70% Train (3,901), 15% Val (836), 15% Test (837) with exact string deduplication.

---

## 2. OpenPhish & Verified Financial URL Dataset

- **Dataset Name**: OpenPhish Live Feed & Verified Financial Domains
- **Source**: OpenPhish Threat Feed & Regulatory Domain Registry
- **Official URL**: https://openphish.com/feed.txt
- **Download Method**: Automated HTTP feed sync (`scripts/download_datasets.py`)
- **License**: Public Open Intelligence Feed / Educational Use
- **Size**: 644 total URL samples (314 Phishing, 330 Legitimate)
- **Language**: N/A (URL / Lexical)
- **Labels**: Binary (`0`: Legitimate, `1`: Phishing / Malicious)
- **Provenance**: Active phishing links verified by OpenPhish threat intelligence combined with verified Indian financial regulatory (SEBI, NSE, BSE) and banking domains.
- **Collection Methodology**: Automated honey-token and network telemetry detection.
- **Known Limitations**: Dynamic feed subject to site takedowns.
- **Classification**: Real-World Feed & Curated Verification Set
- **Intended Use**: URL classifier feature engineering, domain risk scoring, and LightGBM / XGBoost benchmarking.
- **Preprocessing**: Domain extraction, lexical feature calculation (entropy, hyphen count, TLD risk, IP host detection), domain-grouped splitting.
- **Train/Val/Test Usage**: Domain-grouped stratified split (70% Train, 15% Val, 15% Test) to prevent data leakage.

---

## 3. Indian Multilingual & Hinglish Financial Scam Dataset

- **Dataset Name**: Indian Multilingual & Hinglish Financial Scam Corpus
- **Source**: Curated from public SEBI advisories, police cybercell reports, WhatsApp investment fraud notices, and legitimate broker disclosures.
- **Official URL**: Local repository (`data/raw/indian_financial_scams.csv`)
- **Download Method**: Assembled via `scripts/download_datasets.py`
- **License**: Creative Commons Zero (CC0) / Public Educational
- **Size**: 50 targeted samples
- **Language**: English, Hindi (हिन्दी), Hinglish (Romanized Hindi)
- **Labels**: Binary (`0`: Legitimate Regulatory/Broker Notice, `1`: Financial Scam Solicitation) + Multi-task Taxonomies (`fake_sebi_investment`, `guaranteed_return_stock_tip`, `fake_trading_app`, `impersonation_kyc_phishing`, `task_deposit_fraud`, `fake_ipo_allotment`)
- **Provenance**: Real public scam formats reported to SEBI, NCRP, and financial news outlets.
- **Known Limitations**: Small sample count reserved strictly for domain-specific fine-tuning, zero-shot verification, and qualitative red-team evaluation.
- **Classification**: Curated Domain-Specific Benchmark
- **Intended Use**: Multilingual capability validation, rule engine verification, claim extraction testing.
- **Preprocessing**: Unicode normalization, Devanagari script preservation, Hinglish regex tokenization.
- **Train/Val/Test Usage**: Standard 5-fold cross-validation & qualitative test suite.

---

## 4. PhishTank & Cybercrime Reference Intelligence Cache

- **Dataset Name**: PhishTank & NCRP Reference Intelligence
- **Source**: Open Phishing Database & National Cyber Crime Reporting Portal (I4C) sample formats
- **Official URL**: https://phishtank.org
- **Download Method**: Sync cache (`data/raw/phishtank_feed.json`)
- **License**: Open Data Commons Attribution License
- **Size**: Dynamic threat indicators (URLs, phone numbers, Telegram handles)
- **Intended Use**: Authoritative Level-3 evidence matching.
