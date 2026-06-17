from fastapi import APIRouter

from app.schemas import QueryRequest, SearchRequest
from app.services.dataset_service import DatasetService
from app.services.recommendation_service import RecommendationService
from app.utils.response_formatter import success_response, error_response

router = APIRouter()

recommendation_service = RecommendationService()
dataset_service = DatasetService()


@router.get("/")
def health():
    return {
        "status": "running"
    }


@router.post("/recommend")
def recommend(request: QueryRequest):
    try:
        result = recommendation_service.get_recommendations(request.query)

        return success_response(
            message="Recommendations generated successfully",
            data=result
        )

    except Exception as e:
        return error_response(
            message=str(e),
            data=None
        )


@router.post("/similar")
def similar(request: QueryRequest):
    try:
        result = recommendation_service.get_similar_recommendations(request.query)

        return success_response(
            message="Similar restaurants generated successfully",
            data=result
        )

    except Exception as e:
        return error_response(
            message=str(e),
            data=None
        )


@router.post("/search")
def search(request: SearchRequest):
    try:
        result = dataset_service.search_restaurant(request.restaurant_name)

        return success_response(
            message="Restaurant search completed successfully",
            data={
                "restaurant_name": request.restaurant_name,
                "total_results": len(result),
                "results": result
            }
        )

    except Exception as e:
        return error_response(
            message=str(e),
            data=None
        )