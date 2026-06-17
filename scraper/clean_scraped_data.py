import pandas as pd
import re

INPUT_FILE = "datasets/processed/indore_restaurants_cafes_details_gold.csv"
OUTPUT_FILE = "datasets/processed/indore_restaurants_clean_gold.csv"

df = pd.read_csv(INPUT_FILE)


def clean_text(value):
    if pd.isna(value):
        return ""

    value = str(value)
    value = value.replace("", "")
    value = value.replace("", "")
    value = value.replace("", "")
    value = value.replace("", "")
    value = value.replace("\n", " ")
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def clean_rating(value):
    try:
        return float(value)
    except:
        return None


def clean_reviews(value):
    if pd.isna(value):
        return 0

    value = str(value).replace(",", "")
    value = re.sub(r"[^\d]", "", value)

    if value == "":
        return 0

    return int(value)


df["restaurant_name"] = df["restaurant_name"].apply(clean_text)
df["category"] = df["category"].apply(clean_text)
df["address"] = df["address"].apply(clean_text)
df["phone"] = df["phone"].apply(clean_text)
df["website"] = df["website"].apply(clean_text)
df["google_maps_url"] = df["google_maps_url"].apply(clean_text)

df["rating"] = df["rating"].apply(clean_rating)
df["total_reviews"] = df["total_reviews"].apply(clean_reviews)

df = df.drop_duplicates(subset=["restaurant_name"], keep="first")

df["data_source"] = "Google Maps"
df["city"] = "Indore"

df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("Clean dataset created.")
print("Saved to:", OUTPUT_FILE)
print("Shape:", df.shape)
print(df.head())