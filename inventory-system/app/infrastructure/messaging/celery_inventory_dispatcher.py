import asyncio
from uuid import UUID

from app.application.services.inventory_event_dispatcher import InventoryEventDispatcher
from app.infrastructure.messaging.tasks import inventory_changed_task


class CeleryInventoryEventDispatcher(InventoryEventDispatcher):
    async def dispatch_inventory_changed(self, item_id: UUID, event_type: str, quantity: int) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: inventory_changed_task.delay(str(item_id), event_type, quantity))
