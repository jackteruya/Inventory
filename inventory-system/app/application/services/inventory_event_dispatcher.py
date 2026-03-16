from abc import ABC, abstractmethod
from uuid import UUID


class InventoryEventDispatcher(ABC):
    @abstractmethod
    async def dispatch_inventory_changed(self, item_id: UUID, event_type: str, quantity: int) -> None:
        raise NotImplementedError
