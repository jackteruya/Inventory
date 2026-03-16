from celery import Celery
from kombu import Queue

from app.infrastructure.config.settings import get_settings

settings = get_settings()
celery_app = Celery(
    "inventory_app",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)
celery_app.conf.task_default_queue = "inventory"
celery_app.conf.task_queues = (Queue("inventory"),)
celery_app.conf.worker_send_task_events = True
celery_app.conf.task_send_sent_event = True
celery_app.autodiscover_tasks(["app.infrastructure.messaging"])
