from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.domain.entities.inventory_item import InventoryItem


@pytest.fixture
def make_item():
    def _factory(name: str = "Açaí", identifier: str = "acai", quantity: int = 10) -> InventoryItem:
        return InventoryItem(
            id=uuid4(),
            name=name,
            identifier=identifier,
            quantity=quantity,
            last_updated=datetime.now(UTC),
        )

    return _factory
