import random
import time

from app.infrastructure.messaging.celery_app import celery_app
from app.infrastructure.observability.logging import get_logger, setup_logging

setup_logging()

logger = get_logger(__name__)


class InventoryTask(celery_app.Task):
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.warning(
            "task retrying",
            extra={"task_id": task_id, "attempt": self.request.retries, "error": str(exc)},
        )

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(
            "task permanently failed",
            extra={"task_id": task_id, "args": args, "kwargs": kwargs, "error": str(exc)},
        )


@celery_app.task(
    bind=True,
    base=InventoryTask,
    autoretry_for=(Exception,),
    retry_backoff=3,
    retry_kwargs={"max_retries": 3},
)
def inventory_changed_task(self, item_id: str, event_type: str, quantity: int) -> dict:
    logger.info(
        "task started",
        extra={"task_id": self.request.id, "item_id": item_id, "event_type": event_type, "quantity": quantity},
    )

    if random.randint(0, 9) < 5:
        raise Exception("Simulated processing failure.")

    time.sleep(random.randint(1, 5))

    result = {"item_id": item_id, "event_type": event_type, "quantity": quantity, "status": "processed"}

    logger.info("task completed", extra={"task_id": self.request.id, "item_id": item_id, "event_type": event_type})

    return result
