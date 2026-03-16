from celery import Celery

celery = Celery(
    "task_manager",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery.autodiscover_tasks(["app.workers"])