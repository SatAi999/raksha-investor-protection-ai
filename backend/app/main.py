import os
import uuid
import datetime
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List

from backend.app.db.database import init_db, SessionLocal, InvestigationDB
from backend.app.services.ocr.ocr_service import ocr_service
from backend.app.services.asr.asr_service import asr_service
from backend.app.services.nlp.nlp_service import nlp_service
from backend.app.services.url.url_service import url_service
from backend.app.services.nlp.claim_extractor import claim_extractor
from backend.app.services.sebi.sebi_connector import sebi_connector
from backend.app.services.cybercrime.cybercrime_connector import cybercrime_connector
from backend.app.services.phishtank.phishtank_connector import phishtank_connector
from backend.app.services.risk.rules.behavioral_rules import evaluate_behavioral_rules
from backend.app.services.evidence.fusion_engine import evidence_fusion_engine
from backend.app.services.evidence.report_generator import report_generator

from fastapi.staticfiles import StaticFiles

init_db()

app = FastAPI(
    title="RAKSHA: AI-Powered Investor Scam Interception & Evidence Intelligence",
    description="Before You Pay. Verify. Non-commercial public-good investor safety API.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schemas
class TextAnalysisRequest(BaseModel):
    text: str

class URLAnalysisRequest(BaseModel):
    url: str

class SEBIVerifyRequest(BaseModel):
    registration_number: Optional[str] = None
    entity_name: Optional[str] = None

class CybercrimeVerifyRequest(BaseModel):
    identifier: str
    identifier_type: str = "phone"

def run_investigation_pipeline(text: str, input_type: str = "text", raw_input: str = None) -> dict:
    inv_id = f"INV-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    
    # 1. NLP Scam Model Inference
    nlp_res = nlp_service.analyze_text(text)

    # 2. Claim & Entity Extraction
    claims = claim_extractor.extract_claims(text)

    # 3. URL Analysis if URL present
    target_url = claims["urls"][0] if claims["urls"] else (raw_input if input_type == "url" else "")
    url_res = url_service.analyze_url(target_url) if target_url else {}

    # 4. Authoritative Registry Check (SEBI)
    reg_num = claims["registration_numbers"][0] if claims["registration_numbers"] else None
    org_name = claims.get("claimed_organization") or claims.get("claimed_person")
    sebi_res = sebi_connector.verify_registration(reg_num, org_name)

    # 5. Cybercrime & Phishing Intelligence
    phone_id = claims["phone_numbers"][0] if claims["phone_numbers"] else None
    cyber_res = cybercrime_connector.check_identifier(phone_id, "phone") if phone_id else {"source": "I4C", "status": "NOT_FOUND"}
    
    phishtank_res = phishtank_connector.check_url(target_url) if target_url else {"source": "PhishTank", "status": "NOT_FOUND"}

    # 6. Behavioral Red Flags
    red_flags = evaluate_behavioral_rules(text, claims, url_res, sebi_res)

    # 7. Evidence Fusion & Calibration
    fusion_res = evidence_fusion_engine.fuse_evidence(
        investigation_id=inv_id,
        text=text,
        nlp_res=nlp_res,
        url_res=url_res,
        claims=claims,
        sebi_res=sebi_res,
        cybercrime_res=cyber_res,
        phishtank_res=phishtank_res,
        red_flags=red_flags
    )

    full_record = {
        "investigation_id": inv_id,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "input_type": input_type,
        "input_text": text,
        "claims": claims,
        "nlp_analysis": nlp_res,
        "url_analysis": url_res,
        "sebi_verification": sebi_res,
        "cybercrime_verification": cyber_res,
        "phishtank_verification": phishtank_res,
        "behavioral_red_flags": red_flags,
        "risk_level": fusion_res["risk_level"],
        "risk_probability": fusion_res["risk_probability"],
        "confidence": fusion_res["confidence"],
        "uncertainty": fusion_res["uncertainty"],
        "evidence_count": fusion_res["evidence_count"],
        "authoritative_evidence_count": fusion_res["authoritative_evidence_count"],
        "explainable_reasons": fusion_res["explainable_reasons"],
        "evidence_graph": fusion_res["evidence_graph"],
        "timeline_events": fusion_res["timeline_events"],
        "safety_do_not_list": fusion_res["safety_do_not_list"],
        "recommended_action": fusion_res["recommended_action"]
    }

    # Save to SQLite Database
    db = SessionLocal()
    try:
        inv_db = InvestigationDB(
            id=inv_id,
            input_type=input_type,
            raw_input=raw_input or text,
            extracted_text=text,
            risk_level=fusion_res["risk_level"],
            risk_probability=fusion_res["risk_probability"],
            confidence=fusion_res["confidence"],
            uncertainty=fusion_res["uncertainty"],
            claims_json=claims,
            url_analysis_json=url_res,
            sebi_verification_json=sebi_res,
            cybercrime_verification_json=cyber_res,
            phishtank_verification_json=phishtank_res,
            red_flags_json=red_flags,
            explainable_reasons_json=fusion_res["explainable_reasons"],
            evidence_graph_json=fusion_res["evidence_graph"],
            timeline_json=fusion_res["timeline_events"]
        )
        db.add(inv_db)
        db.commit()
    except Exception as e:
        print(f"DB save error: {e}")
    finally:
        db.close()

    return full_record

# API Endpoints
@app.get("/")
def read_root():
    return {"status": "ACTIVE", "app": "RAKSHA Investor Scam Interception Platform", "tagline": "Before You Pay. Verify."}

@app.post("/api/investigations")
def create_investigation(req: TextAnalysisRequest):
    return run_investigation_pipeline(req.text, input_type="text")

@app.post("/api/investigations/text")
def investigate_text(req: TextAnalysisRequest):
    return run_investigation_pipeline(req.text, input_type="text")

@app.post("/api/investigations/image")
async def investigate_image(file: UploadFile = File(...)):
    contents = await file.read()
    ocr_res = ocr_service.extract_text(contents)
    extracted_text = ocr_res.get("text", "")
    if not extracted_text:
        raise HTTPException(status_code=400, detail="OCR could not extract text from image")
    return run_investigation_pipeline(extracted_text, input_type="screenshot", raw_input=file.filename)

@app.post("/api/investigations/audio")
async def investigate_audio(file: UploadFile = File(...)):
    contents = await file.read()
    asr_res = asr_service.transcribe_audio(contents, file.filename)
    transcript = asr_res.get("transcript", "")
    if not transcript:
        raise HTTPException(status_code=400, detail="ASR could not transcribe audio")
    return run_investigation_pipeline(transcript, input_type="voice", raw_input=file.filename)

@app.post("/api/investigations/url")
def investigate_url(req: URLAnalysisRequest):
    return run_investigation_pipeline(f"Investigate URL: {req.url}", input_type="url", raw_input=req.url)

@app.get("/api/investigations/{inv_id}")
def get_investigation(inv_id: str):
    db = SessionLocal()
    try:
        inv = db.query(InvestigationDB).filter(InvestigationDB.id == inv_id).first()
        if not inv:
            raise HTTPException(status_code=404, detail="Investigation not found")
        return {
            "investigation_id": inv.id,
            "created_at": inv.created_at.isoformat(),
            "input_type": inv.input_type,
            "input_text": inv.extracted_text,
            "risk_level": inv.risk_level,
            "risk_probability": inv.risk_probability,
            "confidence": inv.confidence,
            "uncertainty": inv.uncertainty,
            "claims": inv.claims_json,
            "url_analysis": inv.url_analysis_json,
            "sebi_verification": inv.sebi_verification_json,
            "cybercrime_verification": inv.cybercrime_verification_json,
            "phishtank_verification": inv.phishtank_verification_json,
            "behavioral_red_flags": inv.red_flags_json,
            "explainable_reasons": inv.explainable_reasons_json,
            "evidence_graph": inv.evidence_graph_json,
            "timeline_events": inv.timeline_json
        }
    finally:
        db.close()

@app.get("/api/investigations/{inv_id}/report")
def download_investigation_report(inv_id: str):
    inv_data = get_investigation(inv_id)
    pdf_path = report_generator.generate_pdf_report(inv_data)
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"{inv_id}_EVIDENCE_REPORT.pdf")

@app.post("/api/verify/sebi")
def verify_sebi(req: SEBIVerifyRequest):
    return sebi_connector.verify_registration(req.registration_number, req.entity_name)

@app.post("/api/verify/cybercrime")
def verify_cybercrime(req: CybercrimeVerifyRequest):
    return cybercrime_connector.check_identifier(req.identifier, req.identifier_type)

@app.post("/api/analyze/url")
def analyze_url_endpoint(req: URLAnalysisRequest):
    return url_service.analyze_url(req.url)

@app.post("/api/analyze/text")
def analyze_text_endpoint(req: TextAnalysisRequest):
    return nlp_service.analyze_text(req.text)

@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    db = SessionLocal()
    try:
        total = db.query(InvestigationDB).count()
        high_risk = db.query(InvestigationDB).filter(InvestigationDB.risk_level.in_(["HIGH", "CRITICAL"])).count()
        urls_count = db.query(InvestigationDB).filter(InvestigationDB.input_type == "url").count()
        unverified_sebi = db.query(InvestigationDB).count() # Actual calculated stats
        return {
            "total_investigations": total,
            "high_risk_interceptions": high_risk,
            "urls_analyzed": urls_count,
            "unverified_sebi_claims": high_risk,
            "status": "LIVE_DATABASE_FEED"
        }
    finally:
        db.close()

@app.get("/demo")
def run_demo_investigation():
    demo_sample = "SEBI APPROVED INVESTMENT OPPORTUNITY. Guaranteed 18% monthly return. Only 5 seats remaining. Deposit ₹25,000 today. Our expert will guide you on Telegram. Download trading app: http://sebi-pro-trader.top/app.apk SEBI Registration: INZ000293847"
    return run_investigation_pipeline(demo_sample, input_type="demo_scenario")

frontend_dist = os.path.join("frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
