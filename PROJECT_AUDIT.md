# RAKSHA: System & Repository Audit Report

**Timestamp**: 2026-10-03
**Environment**: Windows 11 | RTX 4070 Laptop GPU (8GB VRAM, CUDA 12.7) | 32 GB RAM | Python 3.10.9 (`D:\Computer_Vision\venv`) | Node.js v20.20.2

---

## 1. Environment & Hardware Audit

| Attribute | Specification | Status |
| :--- | :--- | :--- |
| **Operating System** | Windows 11 Home 64-bit | Verified |
| **CPU / RAM** | Multi-core CPU, 32 GB Physical RAM (~6.2 GB free) | Verified |
| **GPU Acceleration** | NVIDIA GeForce RTX 4070 Laptop GPU (8 GB VRAM) | Verified (CUDA 12.7) |
| **Python VirtualEnv** | `D:\Computer_Vision\venv\Scripts\python.exe` (PyTorch 2.5.1+cu121) | Verified & Active |
| **Node.js / npm** | Node v20.20.2, npm v10.8.2 | Verified |
| **Key Installed ML Tools** | PyTorch, Transformers, Scikit-Learn, LightGBM, XGBoost, PaddleOCR | Verified |

---

## 2. Workspace & Codebase Audit

- **Directory**: `d:\Raksha`
- **Existing Files**: Initial clean workspace.
- **Action Required**: Full production architecture build spanning data pipeline, NLP models, URL classifier, backend services, frontend dashboard, risk fusion engine, authoritative connectors, explainable visualization, PDF evidence generator, and testing suites.

---

## 3. Execution Strategy

1. **Data Infrastructure**: Acquire real public SMS/scam/financial smishing datasets, real phishing URL datasets, and Indian Hinglish fraud samples. Build data leakage prevention and deduplication pipeline.
2. **Model Training**:
   - **Text Model**: Benchmark TF-IDF + Logistic Regression baseline against Multilingual Transformers (MuRIL / XLM-RoBERTa / IndicBERT).
   - **URL Model**: Engineer lexical, host, entropy, and domain features; train LightGBM / XGBoost classifier.
   - **Visual & OCR Engine**: Integrate PaddleOCR/Tesseract with vision layout verification.
3. **Claim & Entity Intelligence**: Regex + NER claim extractor, regulatory registration normalizer, and SEBI / NCRP / PhishTank connectors.
4. **Evidence Fusion & Calibration**: Isotonic regression & temperature scaling calibrated multi-signal fusion policy.
5. **Backend Service**: FastAPI with async execution pipeline, database persistence, evidence graph generator, and PDF exporter.
6. **Frontend**: Next.js / React interactive dashboard built with high-trust, Bharat-first design (English, Hindi, Hinglish).
