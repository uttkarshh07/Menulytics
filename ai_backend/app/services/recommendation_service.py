import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.recommendation_engine_v2 import recommend_from_query


class RecommendationService:
    def get_recommendations(self, query: str):
        return recommend_from_query(query)

    def get_similar_recommendations(self, query: str):
        return recommend_from_query(query)