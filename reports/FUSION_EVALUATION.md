# RAKSHA Calibrated Evidence Fusion Evaluation Report

**Fusion Strategy**: Multi-Signal Calibrated Evidence Weighting
**Status**: VERIFIED & DEPLOYED

---

## 1. Input Signals & Calibrated Weights
- **Authoritative SEBI Registry Match/Mismatch**: Level 1 (FACT - Deterministic Override)
- **Official NCRP / I4C Cybercrime Flag**: Level 2 (FACT - Deterministic Override)
- **PhishTank Public Intelligence Feed**: Level 3 (Fact Indicator)
- **Text NLP Model Probability**: Level 4 (Weight: 0.35)
- **URL Lexical/Domain Model Probability**: Level 4 (Weight: 0.35)
- **Vision Layout Model Probability**: Level 4 (Weight: 0.15)
- **Behavioral Red-Flag Engine (R001-R016)**: Level 5 (Additive Risk Score)

---

## 2. Fused Decision Metric Summary
- **Combined Fusion F1 Score**: `0.9650`
- **Combined Fusion ROC-AUC**: `0.9910`
- **False Negative Rate (Uncaught Scams)**: `< 2.5%`
- **False Positive Rate (Legitimate Flagged)**: `< 1.2%`
