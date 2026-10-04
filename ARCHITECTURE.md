# RAKSHA System Architecture Specification

```
                    RAKSHA
                       |
        +--------------+--------------+
        |                             |
      INPUTS                     LIVE SOURCES
        |                             |
   +----+----+                 +------+------+
   |    |    |                 |      |      |
 Text Image Audio             SEBI   NCRP  PhishTank
   |    |    |
   |   OCR  ASR
   |    |    |
   +----+----+
        |
   NLP MODEL
        |
   CLAIM EXTRACTION
        |
   ENTITY RESOLUTION
        |
 +------+-------+----------------+
 |              |                |
 URL MODEL   VISION MODEL    RULE ENGINE
 |              |                |
 +--------------+----------------+
                |
          EVIDENCE FUSION
                |
           CALIBRATION
                |
       EXPLAINABLE RESULT
          /      |      \
      PROTECT  EVIDENCE  RECOVERY
```

---

## Architecture Components

1. **Input Preprocessing Layer**:
   - `backend/app/services/ocr/ocr_service.py`: Tesseract & PaddleOCR multi-engine screenshot text extractor.
   - `backend/app/services/asr/asr_service.py`: Speech-to-Text transcription via OpenAI Whisper.

2. **Analysis & Modeling Layer**:
   - `backend/app/services/nlp/nlp_service.py`: Calibrated text scam classifier (`models/text/text_pipeline.pkl`).
   - `backend/app/services/url/url_service.py`: Lexical & entropy domain classifier (`models/url/url_pipeline.pkl`).
   - `backend/app/services/nlp/claim_extractor.py`: Structured claim, regulator, return rate, and payment handle extractor.

3. **Authoritative Verification Layer**:
   - `backend/app/services/sebi/sebi_connector.py`: SEBI Official Intermediary Registry matcher.
   - `backend/app/services/cybercrime/cybercrime_connector.py`: NCRP / I4C Cybercrime suspect connector.
   - `backend/app/services/phishtank/phishtank_connector.py`: PhishTank live feed sync cache.

4. **Risk & Fusion Engine**:
   - `backend/app/services/risk/rules/behavioral_rules.py`: Rules R001-R016.
   - `backend/app/services/evidence/fusion_engine.py`: Multi-level calibrated evidence fusion engine.

5. **Presentation & Export Layer**:
   - `backend/app/services/evidence/report_generator.py`: PDF Evidence Summary exporter.
   - `frontend/src/App.tsx`: High-trust React UI dashboard.
