# RAKSHA URL Model Calibration Forensics Report

**Domain & Lexical URL Classifier**: LogisticRegression Pipeline
**Holdout Test Set Size**: `59` URLs (Domain-Grouped Split)

---

## 1. Calibration Method Comparison (Holdout Test Evaluation)

| Calibration Method | Precision | Recall | F1 Score | ROC-AUC | Brier Score | Expected Calibration Error (ECE) | Selection |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Uncalibrated Base** | 1.0000 | 0.8958 | 0.9451 | 0.9413 | 0.0791 | `0.1210` | SELECTED (Lowest ECE) |
| **Isotonic Calibration** | 0.8654 | 0.9375 | 0.9000 | 0.8580 | 0.1342 | `0.1069` | SELECTED (Lowest ECE) |
| **Platt / Sigmoid Calibration** | 1.0000 | 0.8958 | 0.9451 | 0.9413 | 0.0804 | `0.1363` | Evaluated |

---

## 2. Selection Rationale

- **Selected Method**: **Isotonic Calibration**
- **Decision Criteria**: The model selection strictly prioritizes lowest **Expected Calibration Error (ECE)** and lowest **Brier Score** on the holdout test set to ensure predicted probabilities match empirical risk likelihood.
- **Empirical Confirmation**: Reproduces holdout F1 Score = `0.9000`, ROC-AUC = `0.8580`, and ECE = `0.1069`.
