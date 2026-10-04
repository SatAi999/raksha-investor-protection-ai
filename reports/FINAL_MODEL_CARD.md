# RAKSHA Master Model Card & Provenance Documentation

**System**: RAKSHA (AI-Powered Investor Scam Interception & Evidence Intelligence)
**Release Version**: 1.0.0-production
**Evaluation Date**: 2026-10-03
**License**: Non-Commercial Public-Good Safety Infrastructure

---

## Model Summary

| Model Component | Architecture | Training Dataset | Primary Metric (F1) | ECE | Saved Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Text Scam Classifier** | Calibrated TF-IDF + RandomForest | UCI SMS + Indian Financial Scams | `0.9519` | `0.0084` | `models/text/text_pipeline.pkl` |
| **URL Intelligence Model** | Calibrated LogisticRegression | OpenPhish Live + Regulatory Domains | `0.9000` | `0.1069` | `models/url/url_pipeline.pkl` |
| **Evidence Fusion Model** | Multi-Source Calibrated Weighted Policy | Combined Holdout Datasets | `0.9650` | `< 0.03` | `models/fusion/fusion_policy.json` |

---

## Intended Use & Safety Controls
- **Primary Purpose**: Pre-transaction interception of unverified financial solicitations for retail Indian investors.
- **Safety Guarantee**: Authoritative SEBI registry and NCRP cybercrime facts ALWAYS take precedence over model probabilities. Machine learning outputs are clearly labeled as estimates.
