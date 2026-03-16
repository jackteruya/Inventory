from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.api.errors.handlers import register_exception_handlers
from app.api.routes.health import router as health_router
from app.api.routes.inventory import router as inventory_router
from app.infrastructure.config.settings import get_settings
from app.infrastructure.observability.logging import get_logger, setup_logging
from app.infrastructure.observability.middleware import LoggingMiddleware

setup_logging()

logger = get_logger(__name__)
settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug, default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

register_exception_handlers(app)
app.include_router(health_router)
app.include_router(inventory_router, prefix=f"{settings.api_v1_prefix}/inventory", tags=["inventory"])


@app.on_event("startup")
async def on_startup() -> None:
    logger.info(
        "application started",
        extra={"app_name": settings.app_name, "env": settings.app_env, "debug": settings.debug},
    )
