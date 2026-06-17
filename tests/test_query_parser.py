from src.query_parser import parse_query

sample_names = [
    "Berlin - Haus de Gourmet",
    "One8 Commune",
    "Mama Loca Vijay Nagar"
]

queries = [
    "Suggest rooftop cafes under ₹1500 for two",
    "Best date night places in Vijay Nagar",
    "Show cafes similar to Berlin - Haus de Gourmet",
    "Trending cafes for college students",
    "Fine dining restaurants near Palasia",
    "Budget-friendly cafes under ₹1000",
    "Romantic places for anniversaries",
    "Premium lounges in Vijay Nagar"
]

for q in queries:
    print("\nQUERY:", q)
    print(parse_query(q, sample_names))