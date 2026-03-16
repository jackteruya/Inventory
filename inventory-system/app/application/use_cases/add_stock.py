import asyncio

from app.application.services.inventory_event_dispatcher import InventoryEventDispatcher
from app.domain.entities.inventory_item import InventoryItem
from app.domain.repositories.inventory_repository import InventoryRepository
from app.domain.services.name_normalizer import InventoryNameNormalizer
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.observability.logging import get_logger

logger = get_logger(__name__)


class AddStockUseCase:
    def __init__(
        self,
        repository: InventoryRepository,
        uow: SqlAlchemyUnitOfWork,
        normalizer: InventoryNameNormalizer,
        dispatcher: InventoryEventDispatcher,
    ) -> None:
        self.repository = repository
        self.uow = uow
        self.normalizer = normalizer
        self.dispatcher = dispatcher

    async def execute(self, name: str, quantity: int) -> InventoryItem:
        identifier = self.normalizer.normalize(name)
        display_name = name.strip().capitalize()

        logger.info("adding stock", extra={"identifier": identifier, "quantity": quantity})

        async with self.uow:
            item = await self.repository.find_or_initialize(name=display_name, identifier=identifier)
            item.add_stock(quantity)
            item = await self.repository.save(item)
            await self.uow.commit()

        logger.info(
            "stock added",
            extra={"item_id": str(item.id), "identifier": identifier, "quantity": quantity, "total": item.quantity},
        )

        asyncio.create_task(
            self.dispatcher.dispatch_inventory_changed(item.id, event_type="stock_added", quantity=quantity)
        )
        return item
