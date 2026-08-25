from redis import Redis

from fridge_ai.config import get_settings
from fridge_ai.database import check_database_connection
from fridge_ai.vector_store import get_qdrant_client


def check_qdrant_connection() -> bool:
    get_qdrant_client().get_collections()
    return True


def check_redis_connection() -> bool:
    settings = get_settings()
    client = Redis.from_url(settings.celery_broker_url)
    try:
        return bool(client.ping())
    finally:
        client.close()


def check_dependencies() -> dict[str, str]:
    checks = {
        "database": check_database_connection,
        "qdrant": check_qdrant_connection,
        "redis": check_redis_connection,
    }
    results: dict[str, str] = {}

    for name, check in checks.items():
        try:
            results[name] = "healthy" if check() else "unhealthy"
        except Exception:
            results[name] = "unhealthy"

    return results
