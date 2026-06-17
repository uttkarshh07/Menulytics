import pandas as pd

FILE = "datasets/processed/indore_restaurants_features_gold.csv"

df = pd.read_csv(FILE)

updates = {
    "One8 Commune Indore": (
        "Vijay Nagar",
        2200,
        "premium",
        "date_night, fine_dining, premium, lounge, restaurant"
    ),

    "Romeo Lane Indore": (
        "Vijay Nagar",
        2200,
        "premium",
        "date_night, fine_dining, premium, lounge, restaurant"
    ),

    "Pincode by Kunal Kapur Indore": (
        "Vijay Nagar",
        2200,
        "premium",
        "date_night, fine_dining, premium, restaurant"
    ),

    "Studio XO Indore": (
        "Vijay Nagar",
        2200,
        "premium",
        "date_night, fine_dining, premium, lounge, restaurant"
    ),

    "Mama Loca Vijay Nagar": (
        "Vijay Nagar",
        1800,
        "premium",
        "date_night, cafe, premium, coffee_dessert"
    ),

    "Mama Loca New Palasia": (
        "New Palasia",
        1800,
        "premium",
        "date_night, cafe, premium, coffee_dessert"
    ),

    "Coco Loco Kitchen Bar Indore": (
        "Vijay Nagar",
        2200,
        "premium",
        "date_night, fine_dining, premium, lounge, restaurant"
    )
}

for name, (area, cost, bucket, tags) in updates.items():

    mask = (
        df["restaurant_name"]
        .str.lower()
        .str.strip()
        == name.lower()
    )

    df.loc[mask, "area"] = area
    df.loc[mask, "estimated_cost_for_two"] = cost
    df.loc[mask, "budget_bucket"] = bucket
    df.loc[mask, "tags"] = tags

df.to_csv(FILE, index=False, encoding="utf-8-sig")

print("Premium metadata updated successfully!\n")

print(
    df[
        df["restaurant_name"].str.contains(
            "One8|Romeo|Coco|Mama|Studio|Pincode",
            case=False,
            na=False
        )
    ][
        [
            "restaurant_name",
            "area",
            "estimated_cost_for_two",
            "budget_bucket",
            "tags"
        ]
    ].to_string(index=False)
)