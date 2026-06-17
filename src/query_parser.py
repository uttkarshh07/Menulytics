import re
from difflib import SequenceMatcher

AREAS = [
    "vijay nagar", "palasia", "new palasia", "old palasia",
    "bhawarkua", "sapna sangeeta", "rajwada", "mg road",
    "ab road", "scheme 54", "scheme 78", "scheme 140", "rau"
]

CATEGORIES = {
    "cafe": ["cafe", "cafes", "coffee", "coffee shop"],
    "restaurant": ["restaurant", "restaurants", "dining", "places"],
    "lounge": ["lounge", "lounges", "bar", "pub"],
    "rooftop": ["rooftop", "terrace"],
}

OCCASIONS = {
    "date_night": ["date night", "date", "romantic", "couple"],
    "anniversary": ["anniversary"],
    "college": ["college", "students", "friends"],
    "family": ["family"],
    "premium": ["premium", "luxury", "fine dining", "classy"],
    "budget": ["budget-friendly", "budget", "cheap", "affordable", "pocket friendly"],
}

AMBIENCE = [
    "rooftop", "romantic", "premium", "luxury", "cozy",
    "aesthetic", "viral", "trending", "fine dining", "lounge"
]


def normalize(text):
    return re.sub(r"[^a-z0-9 ]", " ", str(text).lower()).strip()


def extract_budget(query: str):
    query = query.lower()

    patterns = [
        r"under\s*₹?\s*(\d+)",
        r"below\s*₹?\s*(\d+)",
        r"within\s*₹?\s*(\d+)",
        r"less than\s*₹?\s*(\d+)",
        r"₹\s*(\d+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            return int(match.group(1))

    return None


def extract_area(query: str):
    query = query.lower()

    for area in AREAS:
        if area in query:
            return area.title()

    return None


def extract_category(query: str):
    query = query.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in query:
                return category

    return None


def extract_occasion(query: str):
    query = query.lower()

    for occasion, keywords in OCCASIONS.items():
        for keyword in keywords:
            if keyword in query:
                return occasion

    return None


def extract_ambience(query: str):
    query = query.lower()
    found = []

    for word in AMBIENCE:
        if word in query:
            found.append(word)

    return found


def extract_restaurant_reference(query: str, restaurant_names):
    query_clean = normalize(query)

    best_name = None
    best_score = 0

    for name in restaurant_names:
        name_clean = normalize(name)

        if not name_clean:
            continue

        if name_clean in query_clean:
            return name

        name_words = name_clean.split()

        for length in range(2, min(5, len(name_words)) + 1):
            short_name = " ".join(name_words[:length])

            if short_name in query_clean:
                return name

        score = SequenceMatcher(None, query_clean, name_clean).ratio()

        if score > best_score:
            best_score = score
            best_name = name

    if best_score >= 0.55:
        return best_name

    return None


def parse_query(query: str, restaurant_names=None):
    if restaurant_names is None:
        restaurant_names = []

    return {
        "original_query": query,
        "budget": extract_budget(query),
        "area": extract_area(query),
        "category": extract_category(query),
        "occasion": extract_occasion(query),
        "ambience": extract_ambience(query),
        "restaurant_reference": extract_restaurant_reference(query, restaurant_names)
        if ("similar to" in query.lower() or "like" in query.lower()) else None
    }