from types import SimpleNamespace

import pytest

from fridge_ai.tasks import index_recipe_task


class FakeDatabase:
    def __enter__(self) -> "FakeDatabase":
        return self

    def __exit__(self, *args: object) -> None:
        return None


def test_index_recipe_task(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    recipe = SimpleNamespace(id=42)
    indexed_recipes: list[object] = []

    monkeypatch.setattr(
        "fridge_ai.tasks.SessionLocal",
        FakeDatabase,
    )
    monkeypatch.setattr(
        "fridge_ai.tasks.get_recipe",
        lambda database, recipe_id: recipe,
    )
    monkeypatch.setattr(
        "fridge_ai.tasks.index_recipe",
        indexed_recipes.append,
    )

    result = index_recipe_task.run(42)

    assert result == 42
    assert indexed_recipes == [recipe]
