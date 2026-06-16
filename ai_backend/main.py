from fastapi import FastAPI

from app.config import APP_NAME, APP_VERSION
from app.routes.recommendation_routes import router as recommendation_router

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

app.include_router(recommendation_router)