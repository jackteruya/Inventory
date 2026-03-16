import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.use_cases.add_stock import AddStockUseCase
from app.domain.exceptions.invalid_operation import InvalidInventoryOperationError

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
def normalizer():
    mock = MagicMock()
    mock.normalize.return_value = "acai"
    return mock


@pytest.fixture
def dispatcher():
    return AsyncMock()


@pytest.fixture
def use_case(repository, uow, normalizer, dispatcher):
    return AddStockUseCase(repository, uow, normalizer, dispatcher)


async def test_add_stock_to_new_item(use_case, repository, uow, normalizer, make_item):
    item = make_item(quantity=0)
    item_after_save = make_item(quantity=10)

    repository.find_or_initialize.return_value = item
    repository.save.return_value = item_after_save

    result = await use_case.execute(name="Açaí", quantity=10)

    assert result.quantity == 10
    normalizer.normalize.assert_called_once_with("Açaí")
    repository.find_or_initialize.assert_called_once_with(name="Açaí", identifier="acai")
    repository.save.assert_called_once()
    uow.commit.assert_called_once()


async def test_add_stock_to_existing_item(use_case, repository, uow, make_item):
    item = make_item(quantity=5)
    item_after_save = make_item(quantity=15)

    repository.find_or_initialize.return_value = item
    repository.save.return_value = item_after_save

    result = await use_case.execute(name="Açaí", quantity=10)

    assert result.quantity == 15


async def test_add_stock_dispatches_event(use_case, repository, uow, dispatcher, make_item):
    item = make_item(quantity=0)
    saved = make_item(quantity=10)

    repository.find_or_initialize.return_value = item
    repository.save.return_value = saved

    await use_case.execute(name="Açaí", quantity=10)
    await asyncio.sleep(0)  # deixa o create_task executar

    dispatcher.dispatch_inventory_changed.assert_called_once_with(saved.id, event_type="stock_added", quantity=10)


async def test_add_stock_strips_display_name(use_case, repository, uow, make_item):
    item = make_item()
    repository.find_or_initialize.return_value = item
    repository.save.return_value = item

    await use_case.execute(name="  Açaí  ", quantity=5)

    repository.find_or_initialize.assert_called_once_with(name="Açaí", identifier="acai")


async def test_add_stock_applies_domain_rule_to_entity(use_case, repository, uow, make_item):
    item = make_item(quantity=5)
    repository.find_or_initialize.return_value = item
    repository.save.return_value = item

    await use_case.execute(name="Açaí", quantity=10)

    assert item.quantity == 15


async def test_add_stock_raises_on_zero_quantity(use_case, repository, uow, make_item):
    item = make_item(quantity=0)
    repository.find_or_initialize.return_value = item

    with pytest.raises(InvalidInventoryOperationError):
        await use_case.execute(name="Açaí", quantity=0)
