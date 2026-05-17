from datetime import datetime

from pydantic import Field
from sqlmodel import SQLModel

from app.models.order import OrderStatus
from app.schemas.order_item import OrderItemRead


class OrderCreate(SQLModel):
    command_id: int
    notes: str | None = None


class OrderUpdate(SQLModel):
    status: OrderStatus | None = None
    notes: str | None = None
    total_amount: float | None = None


class OrderRead(SQLModel):
    id: int
    command_id: int
    status: OrderStatus
    notes: str | None = None
    created_at: datetime
    total_amount: float
    items: list[OrderItemRead] = Field(default_factory=list)