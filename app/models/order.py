from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class OrderStatus(str, Enum):
    PENDENTE = "PENDENTE"
    PREPARANDO = "PREPARANDO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    command_id: int = Field(foreign_key="commands.id", index=True)
    status: OrderStatus = Field(default=OrderStatus.PENDENTE, index=True)
    notes: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    total_amount: float = Field(default=0.0)

    command: "Command" = Relationship(back_populates="orders")
    items: list["OrderItem"] = Relationship(back_populates="order")