from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.errors.handlers import register_exception_handlers
from app.api.routes.health import router as health_router
from app.api.routes.inventory import router as inventory_router
from app.infrastructure.config.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(health_router)
app.include_router(inventory_router, prefix=f"{settings.api_v1_prefix}/inventory", tags=["inventory"])
