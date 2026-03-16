from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AddStockRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    quantity: int = Field(gt=0)


class RemoveStockRequest(BaseModel):
    quantity: int = Field(gt=0)


class AddStockResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    identifier: str


class InventoryItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    quantity: int
    last_updated: datetime
