import os
import re
import pandas as pd
import unicodedata

RAW_DIR = os.path.join("data", "raw")
INTERIM_DIR = os.path.join("data", "interim")
os.makedirs(INTERIM_DIR, exist_ok=True)

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    # NFKC Unicode normalization (handles Devanagari & Latin unicode composite characters)
    text = unicodedata.normalize("NFKC", text)
    # Standardize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def preprocess_text_datasets():
    print("=== PREPROCESSING TEXT DATASETS ===")
    
    # 1. UCI SMS Spam
    uci_path = os.path.join(RAW_DIR, "uci_sms_spam.csv")
    if os.path.exists(uci_path):
        df_uci = pd.read_csv(uci_path)
        df_uci["clean_text"] = df_uci["text"].apply(clean_text)
        df_uci["text_length"] = df_uci["clean_text"].apply(len)
        df_uci["word_count"] = df_uci["clean_text"].apply(lambda s: len(s.split()))
        uci_out = os.path.join(INTERIM_DIR, "uci_sms_clean.csv")
        df_uci.to_csv(uci_out, index=False)
        print(f"  UCI SMS Spam preprocessed: {len(df_uci)} rows -> {uci_out}")

    # 2. Indian Financial Scams
    scam_path = os.path.join(RAW_DIR, "indian_financial_scams.csv")
    if os.path.exists(scam_path):
        df_scam = pd.read_csv(scam_path)
        df_scam["clean_text"] = df_scam["text"].apply(clean_text)
        df_scam["text_length"] = df_scam["clean_text"].apply(len)
        df_scam["word_count"] = df_scam["clean_text"].apply(lambda s: len(s.split()))
        scam_out = os.path.join(INTERIM_DIR, "indian_scams_clean.csv")
        df_scam.to_csv(scam_out, index=False)
        print(f"  Indian Financial Scams preprocessed: {len(df_scam)} rows -> {scam_out}")

if __name__ == "__main__":
    preprocess_text_datasets()
