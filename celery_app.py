from celery import Celery
import os
celery_app = Celery(
    "fastapi_project",
    broker = "redis://localhost:6379/0",
    backend = "redis://localhost:6379/0",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content = ["json"],
    result_serializer = "json",
    timezone = "Asia/Bishkek",
    enable_utc = True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit = 25 * 60,
)

# celery_app.autodiscover_tasks(['celery_tasks'])