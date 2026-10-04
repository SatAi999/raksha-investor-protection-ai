import os
import pandas as pd
from sklearn.model_selection import train_test_split, GroupShuffleSplit

PROCESSED_DIR = os.path.join("data", "processed")
SPLITS_DIR = os.path.join("data", "splits")
os.makedirs(SPLITS_DIR, exist_ok=True)
SEED = 42

def build_text_splits():
    print("=== BUILDING TEXT DATASET SPLITS ===")
    uci_file = os.path.join(PROCESSED_DIR, "uci_sms_dedup.csv")
    if not os.path.exists(uci_file):
        print(f"File {uci_file} missing.")
        return

    df = pd.read_csv(uci_file)
    # Stratified Split: Train (70%), Val (15%), Test (15%)
    train_df, temp_df = train_test_split(df, test_size=0.30, random_state=SEED, stratify=df["label"])
    val_df, test_df = train_test_split(temp_df, test_size=0.50, random_state=SEED, stratify=temp_df["label"])

    train_df.to_csv(os.path.join(SPLITS_DIR, "text_train.csv"), index=False)
    val_df.to_csv(os.path.join(SPLITS_DIR, "text_val.csv"), index=False)
    test_df.to_csv(os.path.join(SPLITS_DIR, "text_test.csv"), index=False)

    print(f"  Text Train: {len(train_df)} | Val: {len(val_df)} | Test: {len(test_df)}")

def build_url_splits():
    print("=== BUILDING URL DATASET SPLITS (DOMAIN GROUPED) ===")
    url_file = os.path.join(PROCESSED_DIR, "phishing_urls_dedup.csv")
    if not os.path.exists(url_file):
        print(f"File {url_file} missing.")
        return

    df = pd.read_csv(url_file)
    # Group by hostname to prevent domain-level data leakage across splits
    gss1 = GroupShuffleSplit(n_splits=1, train_size=0.70, random_state=SEED)
    train_idx, temp_idx = next(gss1.split(df, df["label"], df["hostname"]))
    
    train_df = df.iloc[train_idx].copy()
    temp_df = df.iloc[temp_idx].copy()
    
    gss2 = GroupShuffleSplit(n_splits=1, train_size=0.50, random_state=SEED)
    val_idx, test_idx = next(gss2.split(temp_df, temp_df["label"], temp_df["hostname"]))
    
    val_df = temp_df.iloc[val_idx].copy()
    test_df = temp_df.iloc[test_idx].copy()

    train_df.to_csv(os.path.join(SPLITS_DIR, "url_train.csv"), index=False)
    val_df.to_csv(os.path.join(SPLITS_DIR, "url_val.csv"), index=False)
    test_df.to_csv(os.path.join(SPLITS_DIR, "url_test.csv"), index=False)

    print(f"  URL Train: {len(train_df)} | Val: {len(val_df)} | Test: {len(test_df)}")

def main():
    build_text_splits()
    build_url_splits()

if __name__ == "__main__":
    main()
