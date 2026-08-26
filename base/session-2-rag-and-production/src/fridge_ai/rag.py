import requests

from fridge_ai.config import get_settings
from fridge_ai.schemas import RecipeResponse


def build_recommendation_prompt(
    query: str,
    recipes: list[RecipeResponse],
) -> str:
    recipe_context = "\n\n".join(
        (
            f"Recipe {number}: {recipe.name}\n"
            f"Description: {recipe.description}\n"
            f"Ingredients: {', '.join(recipe.ingredients)}\n"
            f"Cooking time: {recipe.cooking_time_minutes} minutes\n"
            f"Dietary tags: {', '.join(recipe.dietary_tags) or 'none'}"
        )
        for number, recipe in enumerate(recipes, start=1)
    )

    return (
        "You are FridgeAI, a meal recommendation assistant. "
        "Answer using only the retrieved recipes below. "
        "Recommend one best match and explain briefly why it fits. "
        "Compare the selected recipe only with the user's request. "
        "Mention a mismatch only when the selected recipe does not satisfy an "
        "explicit part of the request. Do not treat ingredients from other "
        "retrieved recipes as missing. Do not invent recipes, ingredients, "
        "dietary claims, or allergy guarantees.\n\n"
        f"User request: {query}\n\n"
        f"Retrieved recipes:\n{recipe_context}"
    )


def generate_recommendation(
    query: str,
    recipes: list[RecipeResponse],
) -> str:
    if not recipes:
        raise ValueError("At least one recipe is required")

    settings = get_settings()
    response = requests.post(
        f"{settings.ollama_url}/api/chat",
        json={
            "model": settings.ollama_model,
            "messages": [
                {
                    "role": "user",
                    "content": build_recommendation_prompt(query, recipes),
                }
            ],
            "stream": False,
            "options": {"temperature": 0.2},
        },
        timeout=120,
    )
    response.raise_for_status()

    content = response.json().get("message", {}).get("content", "").strip()
    if not content:
        raise ValueError("Ollama returned an empty recommendation")

    return content
