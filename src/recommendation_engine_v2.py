import pandas as pd
from pathlib import Path

from src.query_parser import parse_query


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = PROJECT_ROOT / "datasets" / "processed" / "indore_restaurants_features.csv"

PREMIUM_BRANDS = {
    "Berlin - Haus de Gourmet",
    "One8 Commune Indore",
    "Romeo Lane Indore",
    "Studio XO Indore",
    "Coco Loco Kitchen Bar Indore",
    "Pincode by Kunal Kapur Indore",
    "Mama Loca Vijay Nagar",
    "Mama Loca New Palasia",
    "Chemistry The Cafe Lounge",
    "Firangi Cafe and Bar",
    "Kebabsville Sayaji Indore",
    "Constellation WOW Crest Indore",
    "Twilight WOW Crest Indore"
}

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

def load_dataset():
    df = pd.read_csv(DATASET_PATH)

    df["tags"] = df["tags"].fillna("").astype(str)
    df["area"] = df["area"].fillna("").astype(str)
    df["category"] = df["category"].fillna("").astype(str)
    df["restaurant_name"] = df["restaurant_name"].fillna("").astype(str)
    df["address"] = df["address"].fillna("").astype(str)
    df["budget_bucket"] = df["budget_bucket"].fillna("").astype(str)

    df["estimated_cost_for_two"] = pd.to_numeric(
        df["estimated_cost_for_two"], errors="coerce"
    ).fillna(9999)

    df["trending_score"] = pd.to_numeric(
        df["trending_score"], errors="coerce"
    ).fillna(0)

    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)
    df["total_reviews"] = pd.to_numeric(df["total_reviews"], errors="coerce").fillna(0)
    df["cuisines"] = df.apply(derive_cuisines, axis=1)

    return df


def get_tag_set(value):
    if pd.isna(value):
        return set()

    return {
        tag.strip().lower()
        for tag in str(value).replace("|", ",").split(",")
        if tag.strip()
    }


def jaccard_similarity(tags1, tags2):
    if not tags1 or not tags2:
        return 0

    return len(tags1.intersection(tags2)) / len(tags1.union(tags2))


def cost_similarity(cost1, cost2):
    try:
        cost1 = float(cost1)
        cost2 = float(cost2)

        if cost1 <= 0 or cost2 <= 0 or cost1 == 9999 or cost2 == 9999:
            return 0

        return max(0, 1 - abs(cost1 - cost2) / max(cost1, cost2))

    except:
        return 0


def build_similarity_explanation(row, ref_row):
    reasons = []

    if str(row["area"]).lower() == str(ref_row["area"]).lower():
        reasons.append(f"is also located in {row['area']}")

    if row["budget_bucket"] == ref_row["budget_bucket"]:
        reasons.append(f"has a similar {row['budget_bucket']} budget range")

    if cost_similarity(row["estimated_cost_for_two"], ref_row["estimated_cost_for_two"]) >= 0.75:
        reasons.append("has similar pricing")

    row_tags = get_tag_set(row["tags"])
    ref_tags = get_tag_set(ref_row["tags"])
    common_tags = row_tags.intersection(ref_tags)

    useful_tags = [
        tag.replace("_", " ")
        for tag in common_tags
        if tag in {"date_night", "fine_dining", "premium", "lounge", "rooftop", "cafe", "restaurant"}
    ]

    if useful_tags:
        reasons.append("shares ambience like " + ", ".join(useful_tags[:3]))

    if not reasons:
        reasons.append("has a similar dining profile")

    return "Recommended because it " + ", ".join(reasons) + "."


def build_explanation(row, parsed):
    reasons = []

    if parsed["budget"]:
        if parsed.get("budget_relaxed"):
            reasons.append(
                f"is slightly above your ₹{parsed['budget']} budget but within the closest available range under ₹{parsed['relaxed_budget_limit']}"
            )
        else:
            reasons.append(f"fits your budget under ₹{parsed['budget']}")

    if parsed["area"]:
        reasons.append(f"is located in/near {parsed['area']}")

    if parsed["category"]:
        reasons.append(f"matches your requested {parsed['category']} type")

    if parsed["occasion"]:
        reasons.append(f"is suitable for {parsed['occasion'].replace('_', ' ')}")

    if parsed["ambience"]:
        reasons.append(f"matches ambience like {', '.join(parsed['ambience'])}")

    reasons.append("has a strong trending score")

    return "Recommended because it " + ", ".join(reasons) + "."


def calculate_similarity_scores(results, ref_row):
    ref_area = str(ref_row["area"]).lower().strip()
    ref_budget = str(ref_row["budget_bucket"]).lower().strip()
    ref_cost = ref_row["estimated_cost_for_two"]
    ref_tags = get_tag_set(ref_row["tags"])
    ref_trending = float(ref_row["trending_score"])

    scores = []

    for _, row in results.iterrows():
        row_area = str(row["area"]).lower().strip()
        row_budget = str(row["budget_bucket"]).lower().strip()
        row_cost = row["estimated_cost_for_two"]
        row_tags = get_tag_set(row["tags"])
        row_trending = float(row["trending_score"])

        area_match = 1 if row_area == ref_area and row_area != "" else 0
        budget_match = 1 if row_budget == ref_budget and row_budget != "" else 0
        premium_match = 1 if "premium" in row_tags and "premium" in ref_tags else 0

        brand_boost = 0

        if (
            ref_row["restaurant_name"] in PREMIUM_BRANDS and
            row["restaurant_name"] in PREMIUM_BRANDS
        ):
            brand_boost = 1

        tag_similarity = jaccard_similarity(row_tags, ref_tags)
        price_similarity = cost_similarity(row_cost, ref_cost)
        trending_similarity = max(0, 1 - abs(row_trending - ref_trending))

        similarity_score = (
            0.25 * area_match +
            0.20 * price_similarity +
            0.20 * tag_similarity +
            0.10 * budget_match +
            0.05 * premium_match +
            0.05 * trending_similarity +
            0.15 * brand_boost
        )

        scores.append(similarity_score)

    return scores


def recommend_from_query(query, top_n=10):
    df = load_dataset()
    restaurant_names = df["restaurant_name"].tolist()
    parsed = parse_query(query, restaurant_names)

    parsed["budget_relaxed"] = False
    parsed["relaxed_budget_limit"] = None

    results = df.copy()
    results["match_score"] = 0

    if parsed["restaurant_reference"]:
        ref_row_df = df[df["restaurant_name"] == parsed["restaurant_reference"]]

        if not ref_row_df.empty:
            ref_row = ref_row_df.iloc[0]

            results = results[
                results["restaurant_name"] != parsed["restaurant_reference"]
            ].copy()

            results["similarity_score"] = calculate_similarity_scores(results, ref_row)
            results["final_score"] = results["similarity_score"]

            results = results.sort_values(
                by=["final_score", "trending_score", "rating", "total_reviews"],
                ascending=False
            ).head(top_n)

            recommendations = []

            for _, row in results.iterrows():
                recommendations.append({
                    "restaurant_name": row["restaurant_name"],
                    "category": row["category"],
                    "area": row["area"],
                    "cuisines": row["cuisines"],
                    "rating": row["rating"],
                    "total_reviews": row["total_reviews"],
                    "estimated_cost_for_two": row["estimated_cost_for_two"],
                    "budget_bucket": row["budget_bucket"],
                    "trending_score": row["trending_score"],
                    "tags": row["tags"],
                    "google_maps_url": row["google_maps_url"],
                    "similarity_score": row["similarity_score"],
                    "explanation": build_similarity_explanation(row, ref_row),
                })

            return {
                "query": query,
                "parsed_filters": parsed,
                "total_results": len(recommendations),
                "recommendations": recommendations
            }

    if parsed["budget"]:
        strict_budget_results = results[
            results["estimated_cost_for_two"] <= parsed["budget"]
        ]

        if strict_budget_results.empty:
            relaxed_budget = parsed["budget"] + 300
            parsed["budget_relaxed"] = True
            parsed["relaxed_budget_limit"] = relaxed_budget

            results = results[
                results["estimated_cost_for_two"] <= relaxed_budget
            ].copy()
            results["match_score"] += 1
        else:
            results = strict_budget_results.copy()
            results["match_score"] += 3

    if parsed["area"]:
        area = parsed["area"].lower()
        results = results[
            results["area"].str.lower().str.contains(area, na=False) |
            results["address"].fillna("").str.lower().str.contains(area, na=False)
        ].copy()
        results["match_score"] += 3

    if parsed["category"]:
        category = parsed["category"].lower()
        results["match_score"] += (
            results["category"].str.lower().str.contains(category, na=False).astype(int) * 2
        )
        results["match_score"] += (
            results["tags"].str.lower().str.contains(category, na=False).astype(int) * 2
        )

    if parsed["occasion"]:
        occasion = parsed["occasion"].replace("_", " ").lower()
        results["match_score"] += (
            results["tags"].str.lower().str.contains(occasion, na=False).astype(int) * 2
        )
    if parsed["occasion"] == "premium":
        results = results[
            (results["budget_bucket"].str.lower() == "premium") &
            (results["tags"].str.lower().str.contains("premium|luxury|fine_dining|fine dining|lounge", na=False))
        ].copy()

    for ambience in parsed["ambience"]:
        results["match_score"] += (
            results["tags"].str.lower().str.contains(ambience.lower(), na=False).astype(int) * 2
        )
        results["match_score"] += (
            results["category"].str.lower().str.contains(ambience.lower(), na=False).astype(int)
        )

    if results.empty:
        return {
            "query": query,
            "parsed_filters": parsed,
            "total_results": 0,
            "recommendations": []
        }

    results["final_score"] = results["match_score"] + results["trending_score"]

    results = results.sort_values(
        by=["final_score", "trending_score", "rating", "total_reviews"],
        ascending=False
    ).head(top_n)

    recommendations = []

    for _, row in results.iterrows():
        recommendations.append({
            "restaurant_name": row["restaurant_name"],
            "category": row["category"],
            "area": row["area"],
            "cuisines": row["cuisines"],
            "rating": row["rating"],
            "total_reviews": row["total_reviews"],
            "estimated_cost_for_two": row["estimated_cost_for_two"],
            "budget_bucket": row["budget_bucket"],
            "trending_score": row["trending_score"],
            "tags": row["tags"],
            "google_maps_url": row["google_maps_url"],
            "explanation": build_explanation(row, parsed)
        })

    return {
        "query": query,
        "parsed_filters": parsed,
        "total_results": len(recommendations),
        "recommendations": recommendations
    }


if __name__ == "__main__":
    test_query = "Show cafes similar to Berlin - Haus de Gourmet"
    output = recommend_from_query(test_query)

    print("QUERY:", output["query"])
    print("PARSED:", output["parsed_filters"])

    for item in output["recommendations"]:
        print("\n", item["restaurant_name"])
        print("Cost:", item["estimated_cost_for_two"])
        print("Area:", item["area"])
        print("Similarity Score:", item.get("similarity_score"))
        print(item["explanation"])