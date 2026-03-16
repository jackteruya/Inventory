import asyncio
from uuid import UUID

from app.application.services.inventory_event_dispatcher import InventoryEventDispatcher
from app.domain.entities.inventory_item import InventoryItem
from app.domain.exceptions.inventory_not_found import InventoryNotFoundError
from app.domain.repositories.inventory_repository import InventoryRepository
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork


class RemoveStockUseCase:
    def __init__(
        self,
        repository: InventoryRepository,
        uow: SqlAlchemyUnitOfWork,
        dispatcher: InventoryEventDispatcher,
    ) -> None:
        self.repository = repository
        self.uow = uow
        self.dispatcher = dispatcher

    async def execute(self, item_id: UUID, quantity: int) -> InventoryItem:
        async with self.uow:
            item = await self.repository.get_by_id_for_update(item_id)
            if not item:
                raise InventoryNotFoundError()
            item.remove_stock(quantity)
            item = await self.repository.save(item)
            await self.uow.commit()

        asyncio.create_task(
            self.dispatcher.dispatch_inventory_changed(item.id, event_type="stock_removed", quantity=quantity)
        )
        return item
