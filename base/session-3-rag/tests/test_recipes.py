from collections.abc import Generator
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from apps.api.main import app
from fridge_ai.database import engine, get_db


@pytest.fixture(autouse=True)
def disable_recipe_indexing_task(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "apps.api.recipes.index_recipe_task.delay",
        lambda recipe_id: None,
    )

@pytest.fixture
def database_session() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()

    database = Session(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield database
    finally:
        database.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(
    database_session: Session,
) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield database_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def valid_recipe() -> dict[str, object]:
    return {
        "name": "Test Vegetable Soup",
        "description": "A recipe created during automated testing.",
        "ingredients": ["carrot", "potato", "water"],
        "instructions": ["Chop vegetables", "Boil until tender"],
        "cooking_time_minutes": 30,
        "dietary_tags": ["vegan"],
    }


def test_create_and_retrieve_recipe(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/recipes",
        json=valid_recipe(),
    )

    assert create_response.status_code == 201

    created_recipe = create_response.json()
    recipe_id = created_recipe["id"]

    assert created_recipe["name"] == "Test Vegetable Soup"
    assert created_recipe["dietary_tags"] == ["vegan"]

    retrieve_response = client.get(f"/api/v1/recipes/{recipe_id}")

    assert retrieve_response.status_code == 200
    assert retrieve_response.json()["id"] == recipe_id


def test_list_recipes_includes_created_recipe(
    client: TestClient,
) -> None:
    create_response = client.post(
        "/api/v1/recipes",
        json=valid_recipe(),
    )
    recipe_id = create_response.json()["id"]

    list_response = client.get("/api/v1/recipes")

    assert list_response.status_code == 200
    assert any(
        recipe["id"] == recipe_id
        for recipe in list_response.json()
    )


def test_missing_recipe_returns_404(client: TestClient) -> None:
    response = client.get("/api/v1/recipes/999_999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Recipe not found"}


def test_invalid_recipe_returns_422(client: TestClient) -> None:
    response = client.post(
        "/api/v1/recipes",
        json={
            "name": "",
            "description": "",
            "ingredients": [],
            "instructions": [],
            "cooking_time_minutes": 0,
            "dietary_tags": [],
        },
    )

    assert response.status_code == 422


def test_semantic_recipe_search(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_response = client.post(
        "/api/v1/recipes",
        json=valid_recipe(),
    )
    recipe_id = create_response.json()["id"]

    def fake_search_recipes(
        query: str,
        limit: int,
    ) -> list[SimpleNamespace]:
        assert query == "warming vegetable meal"
        assert limit == 3

        return [
            SimpleNamespace(
                id=recipe_id,
                score=0.91,
            )
        ]

    monkeypatch.setattr(
        "apps.api.recipes.search_recipes",
        fake_search_recipes,
    )

    response = client.get(
        "/api/v1/recipes/search",
        params={
            "query": "warming vegetable meal",
            "limit": 3,
        },
    )

    assert response.status_code == 200

    results = response.json()
    assert len(results) == 1
    assert results[0]["recipe"]["id"] == recipe_id
    assert results[0]["recipe"]["name"] == "Test Vegetable Soup"
    assert results[0]["score"] == pytest.approx(0.91)


def test_generate_grounded_recommendation(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_response = client.post(
        "/api/v1/recipes",
        json=valid_recipe(),
    )
    recipe_id = create_response.json()["id"]

    monkeypatch.setattr(
        "apps.api.recommendations.search_recipes",
        lambda query, limit: [SimpleNamespace(id=recipe_id, score=0.93)],
    )

    def fake_generate_recommendation(
        query: str,
        recipes: list[object],
    ) -> str:
        assert query == "a warming vegan dinner"
        assert len(recipes) == 1
        assert recipes[0].name == "Test Vegetable Soup"
        return "Try Test Vegetable Soup because it is warm and vegan."

    monkeypatch.setattr(
        "apps.api.recommendations.generate_recommendation",
        fake_generate_recommendation,
    )

    response = client.post(
        "/api/v1/recommendations",
        json={
            "query": "a warming vegan dinner",
            "limit": 3,
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert result["model"] == "gemma3:4b"
    assert result["sources"][0]["recipe"]["id"] == recipe_id
    assert result["sources"][0]["score"] == pytest.approx(0.93)
    assert "Test Vegetable Soup" in result["recommendation"]

