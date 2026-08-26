from fridge_ai.celery_app import celery_app
from fridge_ai.database import SessionLocal
from fridge_ai.services import get_recipe
from fridge_ai.vector_store import index_recipe


@celery_app.task(
    name="fridge_ai.index_recipe",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def index_recipe_task(recipe_id: int) -> int:
    with SessionLocal() as database:
        recipe = get_recipe(database, recipe_id)
        if recipe is None:
            raise ValueError(f"Recipe {recipe_id} does not exist")

        index_recipe(recipe)

    return recipe_id
