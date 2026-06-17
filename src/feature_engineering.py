import pandas as pd
import re

INPUT_FILE = "datasets/processed/indore_restaurants_trending_gold.csv"
OUTPUT_FILE = "datasets/processed/indore_restaurants_features_gold.csv"

df = pd.read_csv(INPUT_FILE)


def clean_text(value):
    if pd.isna(value):
        return ""
    return str(value).lower().strip()


def has_keyword(text, keywords):
    return any(keyword in text for keyword in keywords)


def create_tags(row):
    name = clean_text(row["restaurant_name"])
    category = clean_text(row["category"])
    address = clean_text(row["address"])

    combined = f"{name} {category} {address}"

    tags = []

    if has_keyword(combined, ["cafe", "coffee", "brew", "beans"]):
        tags.append("cafe")

    if has_keyword(combined, ["restaurant", "dining", "kitchen", "bistro", "restro"]):
        tags.append("restaurant")

    if has_keyword(combined, ["rooftop", "terrace", "sky", "roof"]):
        tags.append("rooftop")

    if has_keyword(combined, ["fine dining", "luxury", "gourmet", "lounge", "bar"]):
        tags.append("fine_dining")

    if has_keyword(combined, ["family", "pure veg", "thali", "bhojnalay"]):
        tags.append("family_friendly")

    if has_keyword(combined, ["date", "lounge", "bistro", "gourmet", "terrace", "rooftop"]):
        tags.append("date_night")

    if has_keyword(combined, ["pizza", "burger", "mcdonald", "kfc", "sandwich"]):
        tags.append("fast_food")

    if has_keyword(combined, ["coffee", "cafe", "bakery", "dessert", "choco"]):
        tags.append("coffee_dessert")

    return ", ".join(sorted(set(tags)))


def estimate_budget_bucket(row):
    name = clean_text(row["restaurant_name"])
    category = clean_text(row["category"])
    tags = clean_text(row["tags"])

    combined = f"{name} {category} {tags}"

    if has_keyword(combined, ["fine_dining", "gourmet", "bar", "lounge", "luxury"]):
        return "premium"

    if has_keyword(combined, ["cafe", "bistro", "rooftop", "restaurant"]):
        return "mid_range"

    if has_keyword(combined, ["thali", "bhojnalay", "kachori", "dhaba", "snacks", "chat"]):
        return "budget"

    return "mid_range"


def estimate_cost_for_two(bucket):
    if bucket == "budget":
        return 500
    if bucket == "mid_range":
        return 1200
    if bucket == "premium":
        return 2200
    return 1200

def calculate_vfm_score(df):
    max_cost = df["estimated_cost_for_two"].max()

    # Higher affordability = lower cost
    df["affordability_score"] = (
        1 - (df["estimated_cost_for_two"] / max_cost)
    )

    df["vfm_score"] = (
        (
            0.4 * df["rating_scaled"] +
            0.3 * df["reviews_scaled"] +
            0.2 * df["trending_score"] +
            0.1 * df["affordability_score"]
        ) * 10
    ).round(2)

    return df

def extract_area(address):
    address = clean_text(address)

    known_areas = [
        "vijay nagar",
        "palasia",
        "sakhet nagar",
        "saket nagar",
        "bhawarkuan",
        "geeta bhawan",
        "rajwada",
        "khajrana",
        "anand bazar",
        "new palasia",
        "old palasia",
        "scheme no 54",
        "scheme no 78",
        "scheme 140",
        "nipania",
        "rau",
        "ab road",
        "ring road"
    ]

    for area in known_areas:
        if area in address:
            return area.title()

    return "Indore"


df["tags"] = df.apply(create_tags, axis=1)
df["budget_bucket"] = df.apply(estimate_budget_bucket, axis=1)
df["estimated_cost_for_two"] = df["budget_bucket"].apply(estimate_cost_for_two)
df["area"] = df["address"].apply(extract_area)
# NEW
df = calculate_vfm_score(df)

df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("Feature engineered dataset created.")
print("Saved to:", OUTPUT_FILE)
print("Shape:", df.shape)

print("\nSample columns:")
print(
    df[
        [
            "restaurant_name",
            "rating",
            "total_reviews",
            "category",
            "tags",
            "budget_bucket",
            "estimated_cost_for_two",
            "area",
            "trending_score",
            "affordability_score",
            "vfm_score"
        ]
    ].head(20)
)