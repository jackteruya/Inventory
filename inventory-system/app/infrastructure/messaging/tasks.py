import logging
import random
import time

from app.infrastructure.messaging.celery_app import celery_app
from app.infrastructure.observability.logging import setup_logging

logger = logging.getLogger(__name__)


class InventoryTask(celery_app.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(
            "Task %s definitively failed after all retries. args=%s kwargs=%s error=%s",
            task_id,
            args,
            kwargs,
            exc,
        )


@celery_app.task(
    bind=True,
    base=InventoryTask,
    autoretry_for=(Exception,),
    retry_backoff=3,
    retry_kwargs={"max_retries": 3},
)
def inventory_changed_task(self, item_id: str, event_type: str, quantity: int) -> dict:
    setup_logging()

    if random.randint(0, 9) < 5:
        raise Exception("Simulated processing failure.")

    time.sleep(random.randint(1, 5))

    return {"item_id": item_id, "event_type": event_type, "quantity": quantity, "status": "processed"}
