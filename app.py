from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from src.recommendation_api_logic import (
    get_top_trending,
    get_budget_recommendations,
    get_cafe_recommendations,
    get_date_night_recommendations,
    get_area_recommendations,
    get_similar_restaurants,
    search_restaurants
)

app = FastAPI(
    title="Menulytics AI Recommendation API",
    description="AI-powered restaurant recommendation and analytics API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def success_response(message, data=None):
    return {
        "success": True,
        "message": message,
        "data": data
    }


@app.get("/")
def home():
    return success_response(
        "Menulytics AI API is running",
        {
            "status": "success"
        }
    )


@app.get("/health")
def health():
    return success_response(
        "FastAPI AI backend is healthy",
        {
            "status": "up"
        }
    )


@app.get("/recommend")
def recommend(
    query: str = Query("trending"),
    limit: int = Query(10, ge=1, le=50)
):
    if "cafe" in query.lower():
        data = get_cafe_recommendations(limit)
    elif "date" in query.lower() or "night" in query.lower():
        data = get_date_night_recommendations(limit)
    elif "budget" in query.lower() or "cheap" in query.lower():
        data = get_budget_recommendations(1200, limit)
    else:
        data = search_restaurants(query, limit)

        if not data:
            data = get_top_trending(limit)

    return success_response(
        "Recommendations generated",
        data
    )


@app.get("/similar")
def similar(
    name: str = Query(...),
    limit: int = Query(10, ge=1, le=50)
):
    data = get_similar_restaurants(name, limit)

    return success_response(
        "Similar restaurants generated",
        data
    )


@app.get("/search")
def search(
    query: str = Query(...),
    limit: int = Query(10, ge=1, le=50)
):
    data = search_restaurants(query, limit)

    return success_response(
        "Search results generated",
        data
    )


@app.get("/trending")
def trending(limit: int = Query(10, ge=1, le=50)):
    return success_response(
        "Top trending restaurants fetched",
        get_top_trending(limit)
    )


@app.get("/recommend/budget")
def budget_recommendations(
    max_budget: int = Query(1200, ge=100),
    limit: int = Query(10, ge=1, le=50)
):
    return success_response(
        "Budget recommendations generated",
        get_budget_recommendations(max_budget, limit)
    )


@app.get("/recommend/cafes")
def cafe_recommendations(limit: int = Query(10, ge=1, le=50)):
    return success_response(
        "Cafe recommendations generated",
        get_cafe_recommendations(limit)
    )


@app.get("/recommend/date-night")
def date_night_recommendations(limit: int = Query(10, ge=1, le=50)):
    return success_response(
        "Date night recommendations generated",
        get_date_night_recommendations(limit)
    )


@app.get("/recommend/area")
def area_recommendations(
    area: str = Query(...),
    limit: int = Query(10, ge=1, le=50)
):
    return success_response(
        "Area recommendations generated",
        get_area_recommendations(area, limit)
    )


@app.get("/recommend/similar")
def similar_recommendations(
    place: str = Query(...),
    limit: int = Query(10, ge=1, le=50)
):
    return success_response(
        "Similar restaurants generated",
        get_similar_restaurants(place, limit)
    )