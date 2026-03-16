import asyncio
from unittest.mock import AsyncMock

import pytest

from app.application.use_cases.remove_stock import RemoveStockUseCase
from app.domain.exceptions.insufficient_stock import InsufficientStockError
from app.domain.exceptions.inventory_not_found import InventoryNotFoundError

pytestmark = pytest.mark.asyncio


@pytest.fixture
def repository():
    return AsyncMock()


@pytest.fixture
def uow():
    mock = AsyncMock()
    mock.__aenter__.return_value = mock
    mock.__aexit__.return_value = None
    return mock


@pytest.fixture
def dispatcher():
    return AsyncMock()


@pytest.fixture
def use_case(repository, uow, dispatcher):
    return RemoveStockUseCase(repository, uow, dispatcher)


async def test_remove_stock_success(use_case, repository, uow, make_item):
    item = make_item(quantity=10)
    item_after_save = make_item(quantity=8)

    repository.get_by_id_for_update.return_value = item
    repository.save.return_value = item_after_save

    result = await use_case.execute(item_id=item.id, quantity=2)

    assert result.quantity == 8
    repository.get_by_id_for_update.assert_called_once_with(item.id)
    repository.save.assert_called_once()
    uow.commit.assert_called_once()


async def test_remove_stock_raises_when_item_not_found(use_case, repository, make_item):
    item = make_item()
    repository.get_by_id_for_update.return_value = None

    with pytest.raises(InventoryNotFoundError):
        await use_case.execute(item_id=item.id, quantity=1)


async def test_remove_stock_raises_when_insufficient(use_case, repository, make_item):
    item = make_item(quantity=2)
    repository.get_by_id_for_update.return_value = item

    with pytest.raises(InsufficientStockError):
        await use_case.execute(item_id=item.id, quantity=5)


async def test_remove_stock_dispatches_event(use_case, repository, uow, dispatcher, make_item):
    item = make_item(quantity=10)
    saved = make_item(quantity=8)

    repository.get_by_id_for_update.return_value = item
    repository.save.return_value = saved

    await use_case.execute(item_id=item.id, quantity=2)
    await asyncio.sleep(0)  # deixa o create_task executar

    dispatcher.dispatch_inventory_changed.assert_called_once_with(saved.id, event_type="stock_removed", quantity=2)


async def test_remove_stock_applies_domain_rule_to_entity(use_case, repository, uow, make_item):
    item = make_item(quantity=10)
    repository.get_by_id_for_update.return_value = item
    repository.save.return_value = item

    await use_case.execute(item_id=item.id, quantity=3)

    assert item.quantity == 7


async def test_remove_stock_does_not_dispatch_when_item_not_found(use_case, repository, dispatcher, make_item):
    item = make_item()
    repository.get_by_id_for_update.return_value = None

    with pytest.raises(InventoryNotFoundError):
        await use_case.execute(item_id=item.id, quantity=1)

    dispatcher.dispatch_inventory_changed.assert_not_called()
