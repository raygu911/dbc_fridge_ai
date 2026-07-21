from fastapi import FastAPI

from fridge_ai.config import get_settings
from fridge_ai.schemas import HealthResponse

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Backend API for the FridgeAI meal recommendation system.",
    version="0.1.0",
)


@app.get("/", tags=["General"])
def root() -> dict[str, str]:
    return {
        "message": "Welcome to FridgeAI",
        "documentation": "/docs",
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service="fridge-ai-api",
        environment=settings.app_env,
    )