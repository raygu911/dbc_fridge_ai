from sqlalchemy import select
from sqlalchemy.orm import Session

from fridge_ai.models import Recipe
from fridge_ai.schemas import RecipeCreate


def create_recipe(database: Session, recipe_data: RecipeCreate) -> Recipe:
    recipe = Recipe(**recipe_data.model_dump())

    database.add(recipe)
    database.commit()
    database.refresh(recipe)

    return recipe


def list_recipes(database: Session) -> list[Recipe]:
    statement = select(Recipe).order_by(Recipe.id)
    return list(database.scalars(statement).all())


def get_recipe(database: Session, recipe_id: int) -> Recipe | None:
    return database.get(Recipe, recipe_id)