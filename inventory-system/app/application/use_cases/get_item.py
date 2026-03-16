from uuid import UUID

from app.domain.entities.inventory_item import InventoryItem
from app.domain.exceptions.inventory_not_found import InventoryNotFoundError
from app.domain.repositories.inventory_repository import InventoryRepository


class GetInventoryItemUseCase:
    def __init__(self, repository: InventoryRepository) -> None:
        self.repository = repository

    async def execute(self, item_id: UUID) -> InventoryItem:
        item = await self.repository.get_by_id(item_id)
        if item is None:
            raise InventoryNotFoundError()
        return item
