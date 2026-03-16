from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.domain.exceptions.insufficient_stock import InsufficientStockError
from app.domain.exceptions.invalid_operation import InvalidInventoryOperationError
from app.domain.exceptions.inventory_not_found import InventoryNotFoundError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(InventoryNotFoundError)
    async def handle_not_found(_, exc: InventoryNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(InsufficientStockError)
    async def handle_insufficient_stock(_, exc: InsufficientStockError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(InvalidInventoryOperationError)
    async def handle_invalid_operation(_, exc: InvalidInventoryOperationError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})
