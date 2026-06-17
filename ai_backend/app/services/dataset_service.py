import pandas as pd

from app.config import DATASET_PATH


class DatasetService:
    def __init__(self):
        self.df = self.load_dataset()

    def load_dataset(self):
        df = pd.read_csv(DATASET_PATH)
        df = df.fillna("")

        df["cuisines"] = df.apply(self.derive_cuisines, axis=1)

        return df

    def derive_cuisines(self, row):
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

    def search_restaurant(self, restaurant_name: str):
        query = restaurant_name.lower().strip()

        results = self.df[
            self.df["restaurant_name"].str.lower().str.contains(query, na=False)
        ]

        return results.to_dict(orient="records")