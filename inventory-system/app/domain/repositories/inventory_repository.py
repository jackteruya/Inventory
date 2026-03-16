from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.inventory_item import InventoryItem


class InventoryRepository(ABC):
    @abstractmethod
    async def get_by_id(self, item_id: UUID) -> InventoryItem | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_identifier(self, identifier: str) -> InventoryItem | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id_for_update(self, item_id: UUID) -> InventoryItem | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_identifier_for_update(self, identifier: str) -> InventoryItem | None:
        raise NotImplementedError

    @abstractmethod
    async def find_or_initialize(self, name: str, identifier: str) -> InventoryItem:
        raise NotImplementedError

    @abstractmethod
    async def create(self, name: str, identifier: str, quantity: int) -> InventoryItem:
        raise NotImplementedError

    @abstractmethod
    async def save(self, item: InventoryItem) -> InventoryItem:
        raise NotImplementedError

    @abstractmethod
    async def list_items(self, order_by: str | None = None, direction: str | None = None) -> list[InventoryItem]:
        raise NotImplementedError
