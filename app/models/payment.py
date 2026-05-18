from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel, AutoString


class PaymentMethod(str, Enum):
    DINHEIRO = "DINHEIRO"
    CARTAO = "CARTAO"
    PIX = "PIX"


class PaymentStatus(str, Enum):
    PENDENTE = "PENDENTE"
    PAGO = "PAGO"
    ESTORNADO = "ESTORNADO"


class Payment(SQLModel, table=True):
    """Representa um pagamento parcial ou total aplicado a uma comanda."""

    __tablename__ = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    command_id: int | None = Field(default=None, foreign_key="commands.id", index=True)
    amount: float = Field(default=0.0)
    method: PaymentMethod = Field(default=PaymentMethod.DINHEIRO, sa_type=AutoString)
    status: PaymentStatus = Field(default=PaymentStatus.PENDENTE, index=True, sa_type=AutoString)
    paid_at: datetime | None = None

    command: Optional["Command"] = Relationship(back_populates="payments")
