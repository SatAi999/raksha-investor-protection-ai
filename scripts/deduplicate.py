import os
import pandas as pd

INTERIM_DIR = os.path.join("data", "interim")
PROCESSED_DIR = os.path.join("data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

def deduplicate_text_df(df: pd.DataFrame, text_col: str = "clean_text") -> tuple[pd.DataFrame, int]:
    initial_count = len(df)
    df_dedup = df.drop_duplicates(subset=[text_col]).copy()
    removed = initial_count - len(df_dedup)
    return df_dedup, removed

def deduplicate_url_df(df: pd.DataFrame, url_col: str = "url") -> tuple[pd.DataFrame, int]:
    initial_count = len(df)
    df_dedup = df.drop_duplicates(subset=[url_col]).copy()
    removed = initial_count - len(df_dedup)
    return df_dedup, removed

def main():
    print("=== DEDUPLICATING DATASETS ===")
    
    # 1. UCI SMS
    uci_in = os.path.join(INTERIM_DIR, "uci_sms_clean.csv")
    if os.path.exists(uci_in):
        df_uci = pd.read_csv(uci_in)
        df_uci_dedup, uci_dup_count = deduplicate_text_df(df_uci, "clean_text")
        uci_out = os.path.join(PROCESSED_DIR, "uci_sms_dedup.csv")
        df_uci_dedup.to_csv(uci_out, index=False)
        print(f"  UCI SMS Deduplicated: {len(df_uci)} -> {len(df_uci_dedup)} (Removed {uci_dup_count} exact duplicates)")

    # 2. Indian Scams
    scam_in = os.path.join(INTERIM_DIR, "indian_scams_clean.csv")
    if os.path.exists(scam_in):
        df_scam = pd.read_csv(scam_in)
        df_scam_dedup, scam_dup_count = deduplicate_text_df(df_scam, "clean_text")
        scam_out = os.path.join(PROCESSED_DIR, "indian_scams_dedup.csv")
        df_scam_dedup.to_csv(scam_out, index=False)
        print(f"  Indian Scams Deduplicated: {len(df_scam)} -> {len(df_scam_dedup)} (Removed {scam_dup_count} exact duplicates)")

    # 3. Phishing URLs
    url_in = os.path.join(INTERIM_DIR, "phishing_urls_features.csv")
    if os.path.exists(url_in):
        df_url = pd.read_csv(url_in)
        df_url_dedup, url_dup_count = deduplicate_url_df(df_url, "url")
        url_out = os.path.join(PROCESSED_DIR, "phishing_urls_dedup.csv")
        df_url_dedup.to_csv(url_out, index=False)
        print(f"  Phishing URLs Deduplicated: {len(df_url)} -> {len(df_url_dedup)} (Removed {url_dup_count} exact duplicates)")

if __name__ == "__main__":
    main()
