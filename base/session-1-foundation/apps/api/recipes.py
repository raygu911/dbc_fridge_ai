from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fridge_ai.database import get_db
from fridge_ai.schemas import RecipeCreate, RecipeResponse
from fridge_ai.services import create_recipe, get_recipe, list_recipes

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
    return create_recipe(database, recipe_data)


@router.get("", response_model=list[RecipeResponse])
def get_recipes(database: DatabaseSession) -> list[RecipeResponse]:
    return list_recipes(database)


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
