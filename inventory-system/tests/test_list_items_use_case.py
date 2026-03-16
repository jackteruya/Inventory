from unittest.mock import AsyncMock

import pytest

from app.application.use_cases.list_items import ListInventoryItemsUseCase

pytestmark = pytest.mark.asyncio


@pytest.fixture
def repository():
    return AsyncMock()


@pytest.fixture
def use_case(repository):
    return ListInventoryItemsUseCase(repository)


async def test_list_items_returns_all(use_case, repository, make_item):
    items = [make_item("Açaí", "acai", 10), make_item("Banana", "banana", 3)]
    repository.list_items.return_value = items

    result = await use_case.execute()

    assert result == items
    repository.list_items.assert_called_once_with(order_by=None, direction=None)


async def test_list_items_passes_ordering_params(use_case, repository):
    repository.list_items.return_value = []

    await use_case.execute(order_by="name", direction="asc")

    repository.list_items.assert_called_once_with(order_by="name", direction="asc")


async def test_list_items_returns_empty_list(use_case, repository):
    repository.list_items.return_value = []

    result = await use_case.execute()

    assert result == []
