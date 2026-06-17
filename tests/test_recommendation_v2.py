import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from src.recommendation_engine_v2 import recommend_from_query

queries = [
    "Best date night places in Vijay Nagar",
    "Budget-friendly cafes under ₹1000",
    "Fine dining restaurants near Palasia",
    "Premium lounges in Vijay Nagar",
    "Show cafes similar to Berlin - Haus de Gourmet"
]

for q in queries:
    print("\n" + "="*80)
    print("QUERY:", q)

    result = recommend_from_query(q, top_n=5)

    print("PARSED:", result["parsed_filters"])
    print("TOTAL RESULTS:", result["total_results"])

    for r in result["recommendations"]:
        print("\nRestaurant:", r["restaurant_name"])
        print("Area:", r["area"])
        print("Cost for Two:", r["estimated_cost_for_two"])
        print("Trending Score:", r["trending_score"])
        print("Explanation:", r["explanation"])