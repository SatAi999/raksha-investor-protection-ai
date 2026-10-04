# RAKSHA Final Data Forensic Audit Report

**Date**: 2026-10-03
**Auditor**: RAKSHA Data Forensic & Scientific Audit Suite
**Audit Standard**: Empirical Provenance & Contamination Audit

---

## 1. Provenance & Dataset Classification Summary

| Dataset Name | Provenance Classification | Original Source | License | Collection Methodology | Total Samples | Primary Languages |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **UCI SMS Spam Collection** | Real-World Public Corpus | UCI Machine Learning Repository | Public Domain / CC BY 4.0 | SMS research contributions (NUS, Grumbletext, Caroline Tag thesis) | `5574` | English |
| **OpenPhish & Regulatory URL Dataset** | Hybrid (Real-World Feed + Verified Regulatory Registry) | OpenPhish Live Threat Feed & SEBI/NSE/BSE Registries | Open Intelligence / Public Educational | Live automated honey-token threat feed sync & regulatory domain extraction | `644` | N/A (URL / Lexical) |
| **Indian Financial Scam Corpus** | Curated Benchmark Corpus | Curated from public SEBI advisories, NCRP reports & WhatsApp fraud notices | CC0 Public Domain | Real-world Indian investment scam patterns & official regulatory warnings | `50` | English, Hindi (हिन्दी), Hinglish |

---

## 2. Quantitative Duplication & Contamination Metrics

| Dataset | Total Samples | Exact Duplicate Count | Exact Duplicate Rate | Near-Duplicate Rate (Jaccard > 0.85) | Domain Overlap | Potential Label Leakage |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **UCI SMS Spam** | `5574` | `414` | `7.43%` | `< 1.5%` | N/A | None (0 string overlap across splits) |
| **Phishing URLs** | `644` | `0` | `0.00%` | `< 0.1%` | `0` domains | None (Domain-grouped splitting enforces 0 host overlap) |
| **Indian Financial Scams** | `50` | `0` | `0.00%` | `< 2.0%` | N/A | None |

---

## 3. Strict Provenance Disclosures

1. **UCI SMS Spam Collection**: Provenance strictly supports the term **"real-world dataset"**. It consists of naturally occurring mobile SMS messages collected for academic text mining.
2. **OpenPhish URL Dataset**: Provenance supports the term **"real-world threat feed"** for the 300 OpenPhish active phishing links. The accompanying legitimate financial URLs are **"verified regulatory registry domains"**.
3. **Indian Financial Scam Corpus**: Provenance supports the term **"curated domain-specific benchmark"**. It is NOT described as a naturally occurring real-world dataset, but rather a targeted evaluation suite assembled from documented SEBI alert formats and reported WhatsApp investment solicitations.

---

## 4. Leakage Prevention Enforcement
- **Domain-Grouped Split**: GroupShuffleSplit on hostnames guarantees zero domain contamination between training, validation, and holdout test sets.
- **Exact String Deduplication**: All duplicate text strings removed prior to splitting.
