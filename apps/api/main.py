from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.api.recommendations import router as recommendations_router
from apps.api.recipes import router as recipes_router
from fridge_ai.config import get_settings
from fridge_ai.database import create_database_tables
from fridge_ai.schemas import HealthResponse

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    create_database_tables()
    yield


app = FastAPI(
    title=settings.app_name,
    description="Backend API for the FridgeAI meal recommendation system.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(recipes_router)
app.include_router(recommendations_router)


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
