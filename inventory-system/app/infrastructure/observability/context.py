from contextvars import ContextVar
from uuid import uuid4

_request_id: ContextVar[str | None] = ContextVar("request_id", default=None)


def set_request_id(value: str | None = None) -> str:
    rid = value or str(uuid4())
    _request_id.set(rid)
    return rid


def get_request_id() -> str | None:
    return _request_id.get()
