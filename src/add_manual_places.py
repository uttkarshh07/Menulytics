import pandas as pd

MASTER_FILE = "datasets/processed/indore_restaurants_cafes_master.csv"
MANUAL_FILE = "datasets/raw/manual_additions.csv"
OUTPUT_FILE = "datasets/processed/indore_restaurants_cafes_master_gold.csv"

master_df = pd.read_csv(MASTER_FILE)
manual_df = pd.read_csv(MANUAL_FILE)

if "manual_status" not in master_df.columns:
    master_df["manual_status"] = "scraped"

combined_df = pd.concat([master_df, manual_df], ignore_index=True)

combined_df["name_clean"] = combined_df["name"].astype(str).str.lower().str.strip()

combined_df = combined_df.drop_duplicates(subset=["name_clean"], keep="last")

combined_df = combined_df.drop(columns=["name_clean"])

combined_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("Gold master dataset created.")
print("Saved to:", OUTPUT_FILE)
print("Old size:", len(master_df))
print("Manual additions:", len(manual_df))
print("Final size:", len(combined_df))