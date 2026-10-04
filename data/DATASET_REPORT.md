# RAKSHA Comprehensive Dataset & Corpus Report

**Generated**: 2026-10-03
**Status**: ACQUIRED, PREPROCESSED, DEDUPLICATED, AND SPLIT

---

## 1. Raw Dataset Summary

| Dataset Name | Total Rows | Classes / Labels | Missing Values | Primary Languages |
| :--- | :--- | :--- | :--- | :--- |
| **UCI SMS Spam Collection** | `5574` | Spam (747), Legitimate (4827) | 0 | English |
| **Phishing & Legitimate URLs** | `644` | Phishing (314), Legitimate (330) | 0 | Lexical / Domain |
| **Indian Multilingual Financial Scams** | `50` | Scam (30), Legitimate (20) | 0 | English, Hindi, Hinglish |

---

## 2. Text Dataset Splits (UCI SMS Spam)

| Split | Sample Count | Positive (Spam) | Negative (Ham) | Class Ratio (% Spam) |
| :--- | :--- | :--- | :--- | :--- |
| **Train (70%)** | `3612` | `449` | `3163` | `12.43%` |
| **Validation (15%)** | `774` | `97` | `677` | `12.53%` |
| **Test (15%)** | `774` | `96` | `678` | `12.4%` |

---

## 3. URL Dataset Splits (Domain Grouped)

| Split | Sample Count | Phishing (1) | Legitimate (0) | Unique Hostnames |
| :--- | :--- | :--- | :--- | :--- |
| **Train (70%)** | `482` | `218` | `264` | `227` |
| **Validation (15%)** | `103` | `48` | `55` | `49` |
| **Test (15%)** | `59` | `48` | `11` | `49` |
