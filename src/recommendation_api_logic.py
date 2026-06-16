import pandas as pd

DATA_FILE = "datasets/processed/indore_restaurants_features.csv"

df = pd.read_csv(DATA_FILE)

df["tags"] = df["tags"].fillna("").astype(str)
df["category"] = df["category"].fillna("").astype(str)
df["area"] = df["area"].fillna("").astype(str)
df["budget_bucket"] = df["budget_bucket"].fillna("").astype(str)


def derive_cuisines(row):
    text = f"{row.get('tags', '')} {row.get('category', '')}".lower()

    cuisine_keywords = {
        "North Indian": ["north indian", "indian", "punjabi", "dhaba"],
        "South Indian": ["south indian", "dosa", "idli"],
        "Chinese": ["chinese", "noodles", "manchurian"],
        "Italian": ["italian", "pizza", "pasta"],
        "Fast Food": ["fast food", "burger", "fries", "snacks"],
        "Cafe": ["cafe", "coffee"],
        "Bakery": ["bakery", "cake", "dessert"],
        "Mughlai": ["mughlai", "biryani", "kebab"],
        "Continental": ["continental"],
        "Street Food": ["street food", "chaat"],
        "Desserts": ["dessert", "ice cream", "sweet"],
    }

    cuisines = []

    for cuisine, keywords in cuisine_keywords.items():
        if any(keyword in text for keyword in keywords):
            cuisines.append(cuisine)

    if not cuisines:
        cuisines.append("Multi Cuisine")

    return cuisines


df["cuisines"] = df.apply(derive_cuisines, axis=1)


OUTPUT_COLUMNS = [
    "restaurant_name",
    "rating",
    "total_reviews",
    "category",
    "cuisines",
    "tags",
    "budget_bucket",
    "estimated_cost_for_two",
    "area",
    "trending_score",
    "google_maps_url"
]


def format_results(result_df, limit=10):
    result_df = result_df.head(limit)
    return result_df[OUTPUT_COLUMNS].to_dict(orient="records")


def get_top_trending(limit=10):
    result = df.sort_values(by="trending_score", ascending=False)
    return format_results(result, limit)


def get_budget_recommendations(max_budget=1200, limit=10):
    result = df[df["estimated_cost_for_two"] <= max_budget]
    result = result.sort_values(by="trending_score", ascending=False)
    return format_results(result, limit)


def get_cafe_recommendations(limit=10):
    result = df[df["tags"].str.contains("cafe|coffee_dessert", case=False, na=False)]
    result = result.sort_values(by="trending_score", ascending=False)
    return format_results(result, limit)


def get_date_night_recommendations(limit=10):
    result = df[df["tags"].str.contains("date_night|rooftop|fine_dining", case=False, na=False)]
    result = result.sort_values(by="trending_score", ascending=False)
    return format_results(result, limit)


def get_area_recommendations(area_name, limit=10):
    result = df[df["area"].str.contains(area_name, case=False, na=False)]
    result = result.sort_values(by="trending_score", ascending=False)
    return format_results(result, limit)


def get_similar_restaurants(place_name, limit=10):
    matched = df[df["restaurant_name"].str.contains(place_name, case=False, na=False)]

    if matched.empty:
        return []

    base_place = matched.iloc[0]
    base_tags = str(base_place["tags"])
    base_budget = str(base_place["budget_bucket"])

    tag_list = [tag.strip() for tag in base_tags.split(",") if tag.strip()]

    if tag_list:
        result = df[
            (df["tags"].apply(lambda x: any(tag in str(x) for tag in tag_list))) |
            (df["budget_bucket"] == base_budget)
        ]
    else:
        result = df[df["budget_bucket"] == base_budget]

    result = result[result["restaurant_name"] != base_place["restaurant_name"]]
    result = result.sort_values(by="trending_score", ascending=False)

    return format_results(result, limit)


def search_restaurants(query, limit=10):
    query = str(query).lower()

    result = df[
        df["restaurant_name"].str.lower().str.contains(query, na=False) |
        df["category"].str.lower().str.contains(query, na=False) |
        df["tags"].str.lower().str.contains(query, na=False) |
        df["area"].str.lower().str.contains(query, na=False)
    ]

    result = result.sort_values(by="trending_score", ascending=False)

    return format_results(result, limit)