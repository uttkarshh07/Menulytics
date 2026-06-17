import pandas as pd
from sklearn.preprocessing import MinMaxScaler

INPUT_FILE = "datasets/processed/indore_restaurants_clean_gold.csv"
OUTPUT_FILE = "datasets/processed/indore_restaurants_trending_gold.csv"

df = pd.read_csv(INPUT_FILE)

df["rating"] = df["rating"].fillna(0)
df["total_reviews"] = df["total_reviews"].fillna(0)

scaler = MinMaxScaler()

df[["rating_scaled", "reviews_scaled"]] = scaler.fit_transform(
    df[["rating", "total_reviews"]]
)

df["trending_score"] = (
    0.4 * df["rating_scaled"] +
    0.6 * df["reviews_scaled"]
)

df = df.sort_values(by="trending_score", ascending=False)

df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("Trending dataset created.")
print("Saved to:", OUTPUT_FILE)

print("\nTop 20 Trending Restaurants/Cafes in Indore:")
print(
    df[
        [
            "restaurant_name",
            "rating",
            "total_reviews",
            "category",
            "trending_score"
        ]
    ].head(20)
)