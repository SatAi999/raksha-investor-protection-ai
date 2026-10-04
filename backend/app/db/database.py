import os
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime

DB_PATH = os.path.join("data", "raksha.db")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class InvestigationDB(Base):
    __tablename__ = "investigations"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="completed")
    input_type = Column(String, default="text")
    raw_input = Column(Text)
    extracted_text = Column(Text)
    
    # Risk Summary
    risk_level = Column(String)
    risk_probability = Column(Float)
    confidence = Column(Float)
    uncertainty = Column(Float)

    # Detailed JSON Records
    claims_json = Column(JSON)
    url_analysis_json = Column(JSON)
    sebi_verification_json = Column(JSON)
    cybercrime_verification_json = Column(JSON)
    phishtank_verification_json = Column(JSON)
    red_flags_json = Column(JSON)
    explainable_reasons_json = Column(JSON)
    evidence_graph_json = Column(JSON)
    timeline_json = Column(JSON)

def init_db():
    os.makedirs("data", exist_ok=True)
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at {DATABASE_URL}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
