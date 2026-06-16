from src.recommendation_engine_v2 import recommend_from_query

test_queries = [
    "Show cafes similar to Berlin - Haus de Gourmet",
    "Show restaurants similar to One8 Commune",
    "Premium lounges in Vijay Nagar",
    "Best date night places in Vijay Nagar",
    "Suggest rooftop cafes under ₹1500 for two",
    "Budget-friendly cafes under ₹1000",
    "Show places similar to Romeo Lane",
    "Recommend premium restaurants for dinner",
    "Suggest cafes in Vijay Nagar",
    "Show luxury restaurants under ₹2500 for two",
]

for query in test_queries:
    print("=" * 80)
    print("QUERY:", query)

    output = recommend_from_query(query, top_n=5)
    print("PARSED:", output["parsed_filters"])
    print("TOTAL:", output["total_results"])

    for item in output["recommendations"]:
        print("-", item["restaurant_name"])
        print("  Area:", item["area"])
        print("  Cost:", item["estimated_cost_for_two"])
        print("  Score:", item.get("similarity_score", item["trending_score"]))
        print("  Explanation:", item["explanation"])