from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class PaymentMethod(str, Enum):
    DINHEIRO = "DINHEIRO"
    CARTAO = "CARTAO"
    PIX = "PIX"


class PaymentStatus(str, Enum):
    PENDENTE = "PENDENTE"
    PAGO = "PAGO"
    ESTORNADO = "ESTORNADO"


class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    command_id: int | None = Field(default=None, foreign_key="commands.id", index=True)
    # order_id removed; payments associate to Command (account) by default
    amount: float = Field(default=0.0)
    method: PaymentMethod = Field(default=PaymentMethod.DINHEIRO)
    status: PaymentStatus = Field(default=PaymentStatus.PENDENTE, index=True)
    paid_at: datetime | None = None

    command: Optional["Command"] = Relationship(back_populates="payments")
    # order relationship removed to decouple payments from orders
