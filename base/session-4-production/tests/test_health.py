import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from apps.api.main import app
from fridge_ai import health

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to FridgeAI"


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "fridge-ai-api",
        "environment": "development",
    }


def test_response_includes_generated_request_id() -> None:
    response = client.get("/health")

    request_id = response.headers["X-Request-ID"]
    assert request_id
    assert len(request_id) <= 128


def test_response_preserves_client_request_id() -> None:
    response = client.get(
        "/health",
        headers={"X-Request-ID": "training-request-123"},
    )

    assert response.headers["X-Request-ID"] == "training-request-123"


def test_readiness_reports_healthy_dependencies(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "apps.api.main.check_dependencies",
        lambda: {
            "database": "healthy",
            "qdrant": "healthy",
            "redis": "healthy",
        },
    )

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {
            "database": "healthy",
            "qdrant": "healthy",
            "redis": "healthy",
        },
    }


def test_readiness_returns_503_for_unhealthy_dependency(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "apps.api.main.check_dependencies",
        lambda: {
            "database": "healthy",
            "qdrant": "unhealthy",
            "redis": "healthy",
        },
    )

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json()["status"] == "unready"
    assert response.json()["checks"]["qdrant"] == "unhealthy"


def test_dependency_check_handles_expected_client_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        health,
        "check_database_connection",
        lambda: (_ for _ in ()).throw(
            OperationalError("SELECT 1", {}, Exception("offline"))
        ),
    )
    monkeypatch.setattr(health, "check_qdrant_connection", lambda: True)
    monkeypatch.setattr(health, "check_redis_connection", lambda: True)

    assert health.check_dependencies() == {
        "database": "unhealthy",
        "qdrant": "healthy",
        "redis": "healthy",
    }


def test_dependency_check_does_not_hide_programming_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        health,
        "check_database_connection",
        lambda: (_ for _ in ()).throw(ValueError("invalid check")),
    )

    with pytest.raises(ValueError, match="invalid check"):
        health.check_dependencies()
