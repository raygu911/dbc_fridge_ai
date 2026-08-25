import pytest

from fridge_ai.embeddings import create_embedding
from fridge_ai.rag import build_recommendation_prompt
from fridge_ai.schemas import RecipeResponse


def test_empty_text_cannot_be_embedded() -> None:
    with pytest.raises(ValueError, match="Text cannot be empty"):
        create_embedding("   ")


def test_recommendation_prompt_is_grounded() -> None:
    recipe = RecipeResponse.model_validate(
        {
            "id": 1,
            "name": "Chickpea Bowl",
            "description": "A quick grain bowl.",
            "ingredients": ["chickpeas", "rice"],
            "instructions": ["Combine and serve"],
            "cooking_time_minutes": 15,
            "dietary_tags": ["vegan"],
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T00:00:00Z",
        }
    )

    prompt = build_recommendation_prompt(
        "a quick vegan dinner",
        [recipe],
    )

    assert "User request: a quick vegan dinner" in prompt
    assert "Recipe 1: Chickpea Bowl" in prompt
    assert "ingredients from other retrieved recipes" in prompt
