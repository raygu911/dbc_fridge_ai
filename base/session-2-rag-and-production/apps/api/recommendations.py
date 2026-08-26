from typing import Annotated

import requests
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fridge_ai.config import get_settings
from fridge_ai.database import get_db
from fridge_ai.rag import generate_recommendation
from fridge_ai.schemas import (
    RecipeResponse,
    RecipeSearchResult,
    RecommendationRequest,
    RecommendationResponse,
)
from fridge_ai.services import get_recipe
from fridge_ai.vector_store import search_recipes

router = APIRouter(prefix="/api/v1/recommendations", tags=["Recommendations"])

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=RecommendationResponse)
def recommend_recipes(
    request: RecommendationRequest,
    database: DatabaseSession,
) -> RecommendationResponse:
    matches = search_recipes(query=request.query, limit=request.limit)
    sources: list[RecipeSearchResult] = []

    for match in matches:
        recipe = get_recipe(database, int(match.id))
        if recipe is not None:
            sources.append(
                RecipeSearchResult(
                    recipe=RecipeResponse.model_validate(recipe),
                    score=match.score,
                )
            )

    if not sources:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No matching recipes found",
        )

    try:
        recommendation = generate_recommendation(
            query=request.query,
            recipes=[source.recipe for source in sources],
        )
    except (requests.RequestException, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Recommendation model is unavailable",
        ) from error

    settings = get_settings()
    return RecommendationResponse(
        query=request.query,
        recommendation=recommendation,
        model=settings.ollama_model,
        sources=sources,
    )
