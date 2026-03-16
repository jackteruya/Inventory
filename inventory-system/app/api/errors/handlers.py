from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.insufficient_stock import InsufficientStockError
from app.domain.exceptions.invalid_operation import InvalidInventoryOperationError
from app.domain.exceptions.inventory_not_found import InventoryNotFoundError
from app.infrastructure.observability.logging import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(InventoryNotFoundError)
    async def handle_not_found(request: Request, exc: InventoryNotFoundError):
        logger.info("item not found", extra={"path": request.url.path, "detail": str(exc)})
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(InsufficientStockError)
    async def handle_insufficient_stock(request: Request, exc: InsufficientStockError):
        logger.warning("insufficient stock", extra={"path": request.url.path, "detail": str(exc)})
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(InvalidInventoryOperationError)
    async def handle_invalid_operation(request: Request, exc: InvalidInventoryOperationError):
        logger.warning("invalid inventory operation", extra={"path": request.url.path, "detail": str(exc)})
        return JSONResponse(status_code=400, content={"detail": str(exc)})
