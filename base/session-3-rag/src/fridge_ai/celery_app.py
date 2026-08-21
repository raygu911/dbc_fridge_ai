from celery import Celery

from fridge_ai.config import get_settings

settings = get_settings()

celery_app = Celery(
    "fridge_ai",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["fridge_ai.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    result_expires=3_600,
)

