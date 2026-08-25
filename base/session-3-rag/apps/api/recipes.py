from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from fridge_ai.database import get_db
from fridge_ai.schemas import RecipeCreate, RecipeResponse, RecipeSearchResult
from fridge_ai.services import create_recipe, get_recipe, list_recipes
from fridge_ai.tasks import index_recipe_task
from fridge_ai.vector_store import search_recipes

router = APIRouter(prefix="/api/v1/recipes", tags=["Recipes"])

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=RecipeResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_recipe(
    recipe_data: RecipeCreate,
    database: DatabaseSession,
) -> RecipeResponse:
    recipe = create_recipe(database, recipe_data)
    index_recipe_task.delay(recipe.id)
    return recipe


@router.get("", response_model=list[RecipeResponse])
def get_recipes(database: DatabaseSession) -> list[RecipeResponse]:
    return list_recipes(database)


@router.get("/search", response_model=list[RecipeSearchResult])
def semantic_recipe_search(
    database: DatabaseSession,
    query: Annotated[str, Query(min_length=1, max_length=200)],
    limit: Annotated[int, Query(ge=1, le=20)] = 5,
) -> list[RecipeSearchResult]:
    matches = search_recipes(query=query, limit=limit)
    results: list[RecipeSearchResult] = []

    for match in matches:
        recipe = get_recipe(database, int(match.id))

        if recipe is not None:
            results.append(
                RecipeSearchResult(
                    recipe=RecipeResponse.model_validate(recipe),
                    score=match.score,
                )
            )

    return results


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe_by_id(
    recipe_id: int,
    database: DatabaseSession,
) -> RecipeResponse:
    recipe = get_recipe(database, recipe_id)

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )

    return recipe

