from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.domain.entities.inventory_item import InventoryItem
from app.domain.exceptions.insufficient_stock import InsufficientStockError
from app.infrastructure.normalizers.unicode_name_normalizer import UnicodeInventoryNameNormalizer


def test_remove_stock_raises_when_insufficient() -> None:
    item = InventoryItem(
        id=uuid4(),
        name="Açaí",
        identifier="acai",
        quantity=2,
        last_updated=datetime.now(UTC),
    )

    with pytest.raises(InsufficientStockError):
        item.remove_stock(3)


def test_normalizer_collapses_accent_and_case() -> None:
    normalizer = UnicodeInventoryNameNormalizer()
    assert normalizer.normalize("  AÇAÍ  ") == "acai"
