import pandas as pd

DATA_FILE = "datasets/processed/indore_restaurants_features.csv"

df = pd.read_csv(DATA_FILE)

df["tags"] = df["tags"].fillna("").astype(str)
df["category"] = df["category"].fillna("").astype(str)
df["area"] = df["area"].fillna("").astype(str)
df["budget_bucket"] = df["budget_bucket"].fillna("").astype(str)


def show_results(result_df, title):
    print("\n" + title)
    print("-" * len(title))

    if result_df.empty:
        print("No matching restaurants found.")
        return

    print(
        result_df[
            [
                "restaurant_name",
                "rating",
                "total_reviews",
                "category",
                "tags",
                "budget_bucket",
                "estimated_cost_for_two",
                "area",
                "trending_score"
            ]
        ].head(10)
    )


def top_trending(limit=10):
    result = df.sort_values(by="trending_score", ascending=False).head(limit)
    show_results(result, "Top Trending Restaurants/Cafes")


def recommend_by_budget(max_budget=1200, limit=10):
    result = df[df["estimated_cost_for_two"] <= max_budget]
    result = result.sort_values(by="trending_score", ascending=False).head(limit)
    show_results(result, f"Best Recommendations Under ₹{max_budget} For Two")


def recommend_cafes(limit=10):
    result = df[df["tags"].str.contains("cafe|coffee_dessert", case=False, na=False)]
    result = result.sort_values(by="trending_score", ascending=False).head(limit)
    show_results(result, "Best Cafe Recommendations")


def recommend_date_night(limit=10):
    result = df[df["tags"].str.contains("date_night|rooftop|fine_dining", case=False, na=False)]
    result = result.sort_values(by="trending_score", ascending=False).head(limit)
    show_results(result, "Best Date Night / Rooftop Recommendations")


def recommend_by_area(area_name, limit=10):
    result = df[df["area"].str.contains(area_name, case=False, na=False)]
    result = result.sort_values(by="trending_score", ascending=False).head(limit)
    show_results(result, f"Best Recommendations in {area_name}")


def recommend_similar_place(place_name, limit=10):
    matched = df[df["restaurant_name"].str.contains(place_name, case=False, na=False)]

    if matched.empty:
        print(f"\nNo restaurant found matching: {place_name}")
        return

    base_place = matched.iloc[0]
    base_tags = str(base_place["tags"])
    base_budget = str(base_place["budget_bucket"])

    result = df[
        (df["tags"].apply(lambda x: any(tag.strip() in str(x) for tag in base_tags.split(",")))) |
        (df["budget_bucket"] == base_budget)
    ]

    result = result[result["restaurant_name"] != base_place["restaurant_name"]]
    result = result.sort_values(by="trending_score", ascending=False).head(limit)

    show_results(result, f"Places Similar To {base_place['restaurant_name']}")


if __name__ == "__main__":
    top_trending()
    recommend_by_budget(1200)
    recommend_cafes()
    recommend_date_night()
    recommend_by_area("Vijay Nagar")
    recommend_similar_place("Berlin")