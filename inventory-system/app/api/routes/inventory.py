from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import (
    get_add_stock_use_case,
    get_get_item_use_case,
    get_list_items_use_case,
    get_remove_stock_use_case,
)
from app.application.use_cases.add_stock import AddStockUseCase
from app.application.use_cases.get_item import GetInventoryItemUseCase
from app.application.use_cases.list_items import ListInventoryItemsUseCase
from app.application.use_cases.remove_stock import RemoveStockUseCase
from app.schemas.inventory_schema import AddStockRequest, AddStockResponse, InventoryItemResponse, RemoveStockRequest

router = APIRouter()


@router.post("/", response_model=AddStockResponse, status_code=status.HTTP_202_ACCEPTED)
async def add_stock(
    request: AddStockRequest,
    use_case: AddStockUseCase = Depends(get_add_stock_use_case),
) -> AddStockResponse:
    item = await use_case.execute(name=request.name, quantity=request.quantity)
    return AddStockResponse.model_validate(item)


@router.get("/", response_model=list[InventoryItemResponse])
async def list_items(
    order_by: str | None = Query(default=None),
    direction: str | None = Query(default=None),
    use_case: ListInventoryItemsUseCase = Depends(get_list_items_use_case),
) -> list[InventoryItemResponse]:
    items = await use_case.execute(order_by=order_by, direction=direction)
    return [InventoryItemResponse.model_validate(item) for item in items]


@router.get("/{item_id}/", response_model=InventoryItemResponse)
async def get_item(
    item_id: UUID,
    use_case: GetInventoryItemUseCase = Depends(get_get_item_use_case),
) -> InventoryItemResponse:
    item = await use_case.execute(item_id)
    return InventoryItemResponse.model_validate(item)


@router.delete("/{item_id}/", response_model=InventoryItemResponse, status_code=status.HTTP_202_ACCEPTED)
async def remove_stock(
    item_id: UUID,
    request: RemoveStockRequest,
    use_case: RemoveStockUseCase = Depends(get_remove_stock_use_case),
) -> InventoryItemResponse:
    item = await use_case.execute(item_id=item_id, quantity=request.quantity)
    return InventoryItemResponse.model_validate(item)
