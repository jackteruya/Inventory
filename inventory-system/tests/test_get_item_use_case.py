from unittest.mock import AsyncMock

import pytest

from app.application.use_cases.get_item import GetInventoryItemUseCase
from app.domain.exceptions.inventory_not_found import InventoryNotFoundError

pytestmark = pytest.mark.asyncio


@pytest.fixture
def repository():
    return AsyncMock()


@pytest.fixture
def use_case(repository):
    return GetInventoryItemUseCase(repository)


async def test_get_item_returns_item(use_case, repository, make_item):
    item = make_item()
    repository.get_by_id.return_value = item

    result = await use_case.execute(item.id)

    assert result == item
    repository.get_by_id.assert_called_once_with(item.id)


async def test_get_item_raises_when_not_found(use_case, repository, make_item):
    item = make_item()
    repository.get_by_id.return_value = None

    with pytest.raises(InventoryNotFoundError):
        await use_case.execute(item.id)
