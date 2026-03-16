from sqlalchemy import case, desc, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.inventory_item import InventoryItem
from app.domain.exceptions.invalid_operation import InvalidInventoryOperationError
from app.domain.repositories.inventory_repository import InventoryRepository
from app.infrastructure.db.models.inventory_model import InventoryItemModel


class SqlAlchemyInventoryRepository(InventoryRepository):
    VALID_ORDER_FIELDS = {
        "name": InventoryItemModel.name,
        "quantity": InventoryItemModel.quantity,
        "last_updated": InventoryItemModel.last_updated,
    }

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, item_id) -> InventoryItem | None:
        model = await self.session.get(InventoryItemModel, item_id)
        return self._to_entity(model) if model else None

    async def get_by_identifier(self, identifier: str) -> InventoryItem | None:
        stmt = select(InventoryItemModel).where(InventoryItemModel.identifier == identifier)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_id_for_update(self, item_id) -> InventoryItem | None:
        stmt = select(InventoryItemModel).where(InventoryItemModel.id == item_id).with_for_update()
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_identifier_for_update(self, identifier: str) -> InventoryItem | None:
        stmt = select(InventoryItemModel).where(InventoryItemModel.identifier == identifier).with_for_update()
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_or_initialize(self, name: str, identifier: str) -> InventoryItem:
        # UPSERT: garante que a linha existe antes do SELECT FOR UPDATE,
        # eliminando race condition em inserts simultâneos para o mesmo identifier.
        upsert_stmt = (
            insert(InventoryItemModel)
            .values(name=name, identifier=identifier, quantity=0)
            .on_conflict_do_nothing(index_elements=["identifier"])
        )
        await self.session.execute(upsert_stmt)
        await self.session.flush()

        select_stmt = select(InventoryItemModel).where(InventoryItemModel.identifier == identifier).with_for_update()
        result = await self.session.execute(select_stmt)
        model = result.scalar_one()
        return self._to_entity(model)

    async def create(self, name: str, identifier: str, quantity: int) -> InventoryItem:
        if quantity <= 0:
            raise InvalidInventoryOperationError("Quantity must be greater than zero.")
        model = InventoryItemModel(name=name, identifier=identifier, quantity=quantity)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def save(self, item: InventoryItem) -> InventoryItem:
        model = await self.session.get(InventoryItemModel, item.id)
        if model is None:
            model = InventoryItemModel(
                id=item.id,
                name=item.name,
                identifier=item.identifier,
                quantity=item.quantity,
                last_updated=item.last_updated,
            )
            self.session.add(model)
        else:
            model.name = item.name
            model.identifier = item.identifier
            model.quantity = item.quantity
            model.last_updated = item.last_updated
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def list_items(self, order_by: str | None = None, direction: str | None = None) -> list[InventoryItem]:
        stmt = select(InventoryItemModel)

        if order_by:
            if order_by not in self.VALID_ORDER_FIELDS:
                raise InvalidInventoryOperationError("Invalid order_by field.")
            direction = (direction or "asc").lower()
            if direction not in {"asc", "desc"}:
                raise InvalidInventoryOperationError("Invalid direction field.")
            column = self.VALID_ORDER_FIELDS[order_by]
            stmt = stmt.order_by(desc(column) if direction == "desc" else column.asc())
        else:
            stmt = stmt.order_by(
                case((InventoryItemModel.quantity < 5, 0), else_=1),
                InventoryItemModel.last_updated.desc(),
                InventoryItemModel.name.asc(),
            )

        result = await self.session.execute(stmt)
        return [self._to_entity(model) for model in result.scalars().all()]

    @staticmethod
    def _to_entity(model: InventoryItemModel) -> InventoryItem:
        return InventoryItem(
            id=model.id,
            name=model.name,
            identifier=model.identifier,
            quantity=model.quantity,
            last_updated=model.last_updated,
        )
