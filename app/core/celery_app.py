from celery import Celery

celery = Celery(
    "task_manager",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.autodiscover_tasks(["app.workers"])

import app.workers.tasks

celery.conf.task_routes = {
    "app.workers.tasks.*": {"queue": "tasks"}
}