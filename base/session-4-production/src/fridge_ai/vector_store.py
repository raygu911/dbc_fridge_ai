from functools import lru_cache

from qdrant_client import QdrantClient, models

from fridge_ai.config import get_settings
from fridge_ai.embeddings import create_embedding
from fridge_ai.models import Recipe

VECTOR_SIZE = 384


@lru_cache
def get_qdrant_client() -> QdrantClient:
    settings = get_settings()
    return QdrantClient(url=settings.qdrant_url)


def ensure_recipe_collection() -> None:
    settings = get_settings()
    client = get_qdrant_client()

    if client.collection_exists(settings.qdrant_collection):
        return

    client.create_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=models.VectorParams(
            size=VECTOR_SIZE,
            distance=models.Distance.COSINE,
        ),
    )


def recipe_to_text(recipe: Recipe) -> str:
    ingredients = ", ".join(recipe.ingredients)
    tags = ", ".join(recipe.dietary_tags)

    return (
        f"Recipe: {recipe.name}. "
        f"Description: {recipe.description}. "
        f"Ingredients: {ingredients}. "
        f"Dietary tags: {tags}."
    )


def index_recipe(recipe: Recipe) -> None:
    settings = get_settings()
    client = get_qdrant_client()

    ensure_recipe_collection()

    client.upsert(
        collection_name=settings.qdrant_collection,
        wait=True,
        points=[
            models.PointStruct(
                id=recipe.id,
                vector=create_embedding(recipe_to_text(recipe)),
                payload={
                    "recipe_id": recipe.id,
                    "name": recipe.name,
                    "description": recipe.description,
                    "ingredients": recipe.ingredients,
                    "dietary_tags": recipe.dietary_tags,
                },
            )
        ],
    )


def index_recipes(recipes: list[Recipe]) -> int:
    for recipe in recipes:
        index_recipe(recipe)

    return len(recipes)


def search_recipes(
    query: str,
    limit: int = 5,
) -> list[models.ScoredPoint]:
    cleaned_query = " ".join(query.split())

    if not cleaned_query:
        raise ValueError("Search query cannot be empty")

    settings = get_settings()
    client = get_qdrant_client()

    ensure_recipe_collection()

    result = client.query_points(
        collection_name=settings.qdrant_collection,
        query=create_embedding(cleaned_query),
        limit=limit,
        with_payload=True,
        with_vectors=False,
    )

    return result.points
