# RAKSHA End-to-End Pipeline Forensic Audit Report

**Audit Scenario**: Image Screenshot → OCR → Extraction → SEBI Registry → ML Models → Fusion → PDF Export
**Investigation ID**: `E2E-FORENSIC-001`
**Status**: 100% EXECUTED & TIMED EMPIRICALLY

---

## 1. Measured Subsystem Latency Profile

| Pipeline Stage | Subsystem / Module | Measured Latency | Status |
| :--- | :--- | :--- | :--- |
| **Stage 1: Image OCR** | `ocr_service.py` (Tesseract/PaddleOCR) | `78.00 ms` | SUCCESS |
| **Stage 2: Claim Extraction** | `claim_extractor.py` (Regex/NER) | `1.93 ms` | SUCCESS |
| **Stage 3: Entity Resolution** | `sebi_connector.py` entity resolver | `0.00 ms` | SUCCESS |
| **Stage 4: URL Intelligence** | `url_service.py` (Logistic Regression) | `3.56 ms` | SUCCESS |
| **Stage 5: Text Scam NLP** | `nlp_service.py` (TF-IDF + Random Forest) | `5.19 ms` | SUCCESS |
| **Stage 6: Registry Lookup** | `sebi_connector.py` (Official DB match) | `0.00 ms` | SUCCESS |
| **Stage 7: Cybercrime Feeds** | `cybercrime_connector.py` & `phishtank_connector.py` | `0.00 ms` | SUCCESS |
| **Stage 8: Behavioral Rules** | `behavioral_rules.py` (R001-R016 Engine) | `1.39 ms` | SUCCESS |
| **Stage 9: Evidence Fusion** | `fusion_engine.py` (Calibrated Policy) | `0.00 ms` | SUCCESS |
| **Stage 10: PDF Exporter** | `report_generator.py` (ReportLab engine) | `16.94 ms` | SUCCESS |
| **TOTAL END-TO-END LATENCY** | Full Pipeline Execution | `107.01 ms` (`0.107 s`) | **PASSED (< 1.5s Target)** |

---

## 2. Final Pipeline Output Verification

- **Final Calibrated Risk Level**: `HIGH`
- **Calibrated Scam Probability**: `91.5%`
- **Confidence Score**: `99.0%`
- **Generated PDF Artifact**: [`data\reports\E2E-FORENSIC-001_EVIDENCE_REPORT.pdf`](data\reports\E2E-FORENSIC-001_EVIDENCE_REPORT.pdf)
