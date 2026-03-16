from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.inventory_event_dispatcher import InventoryEventDispatcher
from app.application.use_cases.add_stock import AddStockUseCase
from app.application.use_cases.get_item import GetInventoryItemUseCase
from app.application.use_cases.list_items import ListInventoryItemsUseCase
from app.application.use_cases.remove_stock import RemoveStockUseCase
from app.domain.repositories.inventory_repository import InventoryRepository
from app.domain.services.name_normalizer import InventoryNameNormalizer
from app.infrastructure.db.repositories.sqlalchemy_inventory_repository import SqlAlchemyInventoryRepository
from app.infrastructure.db.session import get_db_session
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.messaging.celery_inventory_dispatcher import CeleryInventoryEventDispatcher
from app.infrastructure.normalizers.unicode_name_normalizer import UnicodeInventoryNameNormalizer


def get_inventory_repository(session: AsyncSession = Depends(get_db_session)) -> InventoryRepository:
    return SqlAlchemyInventoryRepository(session)


def get_unit_of_work(session: AsyncSession = Depends(get_db_session)) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session)


def get_name_normalizer() -> InventoryNameNormalizer:
    return UnicodeInventoryNameNormalizer()


def get_event_dispatcher() -> InventoryEventDispatcher:
    return CeleryInventoryEventDispatcher()


def get_add_stock_use_case(
    repository: InventoryRepository = Depends(get_inventory_repository),
    uow: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
    normalizer: InventoryNameNormalizer = Depends(get_name_normalizer),
    dispatcher: InventoryEventDispatcher = Depends(get_event_dispatcher),
) -> AddStockUseCase:
    return AddStockUseCase(repository, uow, normalizer, dispatcher)


def get_remove_stock_use_case(
    repository: InventoryRepository = Depends(get_inventory_repository),
    uow: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
    dispatcher: InventoryEventDispatcher = Depends(get_event_dispatcher),
) -> RemoveStockUseCase:
    return RemoveStockUseCase(repository, uow, dispatcher)


def get_get_item_use_case(
    repository: InventoryRepository = Depends(get_inventory_repository),
) -> GetInventoryItemUseCase:
    return GetInventoryItemUseCase(repository)


def get_list_items_use_case(
    repository: InventoryRepository = Depends(get_inventory_repository),
) -> ListInventoryItemsUseCase:
    return ListInventoryItemsUseCase(repository)
