import os
import re
import math
import pandas as pd
from urllib.parse import urlparse

RAW_DIR = os.path.join("data", "raw")
INTERIM_DIR = os.path.join("data", "interim")
os.makedirs(INTERIM_DIR, exist_ok=True)

SUSPICIOUS_TLDS = {".top", ".xyz", ".club", ".site", ".info", ".online", ".tech", ".biz", ".app", ".work", ".click"}
SUSPICIOUS_TOKENS = ["sebi", "sec", "trade", "bonus", "guaranteed", "profit", "kyc", "verify", "update", "free", "login", "pay", "gift", "escrow", "claim"]

def calculate_entropy(text: str) -> float:
    if not text:
        return 0.0
    prob = [float(text.count(c)) / len(text) for c in set(text)]
    return -sum([p * math.log2(p) for p in prob])

def extract_url_features(url: str) -> dict:
    if not isinstance(url, str) or not url.strip():
        url = "http://unknown.com"
    
    url = url.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "http://" + url
        
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""
    
    # 1. Lexical Length Features
    url_len = len(url)
    host_len = len(hostname)
    path_len = len(path)
    
    # 2. Counts & Delimiters
    num_dots = hostname.count(".")
    num_hyphens = hostname.count("-")
    num_digits = sum(c.isdigit() for c in url)
    num_specials = sum(not c.isalnum() and c not in [":", "/", ".", "-"] for c in url)
    
    # 3. Structural & Protocol Signals
    is_https = 1 if parsed.scheme == "https" else 0
    is_ip = 1 if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname) else 0
    has_punycode = 1 if "xn--" in hostname.lower() else 0
    
    # 4. TLD and Domain Features
    tld = "." + hostname.split(".")[-1].lower() if "." in hostname else ""
    is_suspicious_tld = 1 if tld in SUSPICIOUS_TLDS else 0
    
    # 5. Token Suspiciousness & Entropy
    host_lower = hostname.lower()
    suspicious_token_count = sum(1 for token in SUSPICIOUS_TOKENS if token in host_lower or token in path.lower())
    entropy = calculate_entropy(hostname)
    
    return {
        "url_len": url_len,
        "host_len": host_len,
        "path_len": path_len,
        "num_dots": num_dots,
        "num_hyphens": num_hyphens,
        "num_digits": num_digits,
        "num_specials": num_specials,
        "is_https": is_https,
        "is_ip": is_ip,
        "has_punycode": has_punycode,
        "is_suspicious_tld": is_suspicious_tld,
        "suspicious_token_count": suspicious_token_count,
        "entropy": entropy,
        "hostname": hostname,
        "tld": tld
    }

def preprocess_url_dataset():
    print("=== PREPROCESSING URL DATASETS ===")
    url_path = os.path.join(RAW_DIR, "phishing_urls.csv")
    if not os.path.exists(url_path):
        print(f"Error: {url_path} not found.")
        return

    df = pd.read_csv(url_path)
    features_list = []
    for idx, row in df.iterrows():
        feats = extract_url_features(row["url"])
        feats["url"] = row["url"]
        feats["label"] = row["label"]
        feats["source"] = row.get("source", "unknown")
        features_list.append(feats)

    feats_df = pd.DataFrame(features_list)
    out_path = os.path.join(INTERIM_DIR, "phishing_urls_features.csv")
    feats_df.to_csv(out_path, index=False)
    print(f"  Extracted lexical features for {len(feats_df)} URLs -> {out_path}")

if __name__ == "__main__":
    preprocess_url_dataset()
