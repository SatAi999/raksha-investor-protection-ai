# RAKSHA Data Leakage Audit Report

**Date**: 2026-10-03
**Status**: PASSED (ZERO LEAKAGE DETECTED)

---

## 1. Text Dataset Leakage Audit

| Metric | Measured Value | Threshold | Status |
| :--- | :--- | :--- | :--- |
| **Train Sample Count** | `3612` | - | Informational |
| **Validation Sample Count** | `774` | - | Informational |
| **Test Sample Count** | `774` | - | Informational |
| **Train vs Val Exact Overlap** | `0` | 0 | PASSED |
| **Train vs Test Exact Overlap** | `0` | 0 | PASSED |
| **Val vs Test Exact Overlap** | `0` | 0 | PASSED |

---

## 2. URL Dataset & Domain Leakage Audit

| Metric | Measured Value | Threshold | Status |
| :--- | :--- | :--- | :--- |
| **Train Sample Count** | `482` | - | Informational |
| **Validation Sample Count** | `103` | - | Informational |
| **Test Sample Count** | `59` | - | Informational |
| **Train vs Val Exact URL Overlap** | `0` | 0 | PASSED |
| **Train vs Test Exact URL Overlap** | `0` | 0 | PASSED |
| **Train vs Val Domain Overlap** | `0` | 0 | PASSED |
| **Train vs Test Domain Overlap** | `0` | 0 | PASSED |

---

## Conclusion
- Domain grouping strictly isolates hostnames across train, validation, and test splits.
- Zero contamination verified across exact text strings and URL domain identifiers.
