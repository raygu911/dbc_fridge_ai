import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from apps.api.recipes import router as recipes_router
from apps.api.recommendations import router as recommendations_router
from fridge_ai.config import get_settings
from fridge_ai.database import create_database_tables
from fridge_ai.health import check_dependencies
from fridge_ai.logging import configure_logging
from fridge_ai.schemas import HealthResponse, ReadinessResponse

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)


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


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", "").strip()[:128]
    request_id = request_id or str(uuid4())
    request.state.request_id = request_id
    started_at = perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        logger.exception(
            "Unhandled request error",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
            },
        )
        response = JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "request_id": request_id,
            },
        )

    duration_ms = round((perf_counter() - started_at) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "Request completed",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    return response


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


@app.get(
    "/ready",
    response_model=ReadinessResponse,
    responses={503: {"model": ReadinessResponse}},
    tags=["General"],
)
def readiness_check() -> ReadinessResponse | JSONResponse:
    checks = check_dependencies()
    is_ready = all(result == "healthy" for result in checks.values())
    result = ReadinessResponse(
        status="ready" if is_ready else "unready",
        checks=checks,
    )

    if not is_ready:
        return JSONResponse(
            status_code=503,
            content=result.model_dump(),
        )

    return result
