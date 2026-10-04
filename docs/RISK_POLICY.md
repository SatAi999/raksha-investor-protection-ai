# RAKSHA Risk Policy & Evidence Hierarchy

## Evidence Hierarchy

| Level | Evidence Category | Authority Type | Override Power |
| :--- | :--- | :--- | :--- |
| **Level 1** | SEBI Official Intermediary Registry | Government / Regulatory Fact | Automatic Mismatch Flag |
| **Level 2** | National Cybercrime Reporting Portal (I4C) | Official Public Cybersecurity Fact | Automatic Critical Flag |
| **Level 3** | PhishTank Active Intelligence | Verified Phishing Feed Fact | Automatic Critical Flag |
| **Level 4** | Machine Learning Models (Text & URL) | Statistical Probability Estimate | Weighted Calibration Signal |
| **Level 5** | Behavioral Red-Flag Engine (R001-R016) | Deterministic Heuristic Rule | Additive Risk Score |

---

## Decision Thresholds

- **CRITICAL**: Level 2 or 3 match, OR Level 1 SEBI registration mismatch combined with guaranteed return claims. Risk Probability >= 0.95.
- **HIGH**: Level 1 unverified SEBI claim, OR multiple high-severity behavioral red flags (R001 + R007 + R009). Risk Probability >= 0.80.
- **REVIEW**: Mixed evidence or insufficient registration context. Risk Probability between 0.45 and 0.79.
- **LOW**: Verified legitimate regulatory notice, clean broker advisory, or zero scam indicators. Risk Probability < 0.45.
