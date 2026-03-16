import socket

from fastapi import APIRouter
from sqlalchemy import text

from app.infrastructure.config.settings import get_settings
from app.infrastructure.db.session import AsyncSessionLocal

router = APIRouter(prefix="/health")


@router.get("/")
async def health() -> dict:
    settings = get_settings()
    db_ok = False
    rabbit_ok = False

    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    try:
        with socket.create_connection((settings.rabbitmq_host, settings.rabbitmq_port), timeout=2):
            rabbit_ok = True
    except Exception:
        rabbit_ok = False

    status = "ok" if db_ok and rabbit_ok else "degraded"
    return {"status": status, "database": db_ok, "rabbitmq": rabbit_ok}
