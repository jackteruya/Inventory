from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from app.domain.exceptions.insufficient_stock import InsufficientStockError
from app.domain.exceptions.invalid_operation import InvalidInventoryOperationError


@dataclass
class InventoryItem:
    id: UUID
    name: str
    identifier: str
    quantity: int
    last_updated: datetime

    def add_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise InvalidInventoryOperationError("Quantity must be greater than zero.")
        self.quantity += quantity
        self.last_updated = datetime.now(UTC)

    def remove_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise InvalidInventoryOperationError("Quantity must be greater than zero.")
        if quantity > self.quantity:
            raise InsufficientStockError("Insufficient stock.")
        self.quantity -= quantity
        self.last_updated = datetime.now(UTC)
