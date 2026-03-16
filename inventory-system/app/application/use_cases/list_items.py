from app.domain.entities.inventory_item import InventoryItem
from app.domain.repositories.inventory_repository import InventoryRepository


class ListInventoryItemsUseCase:
    def __init__(self, repository: InventoryRepository) -> None:
        self.repository = repository

    async def execute(self, order_by: str | None = None, direction: str | None = None) -> list[InventoryItem]:
        return await self.repository.list_items(order_by=order_by, direction=direction)
