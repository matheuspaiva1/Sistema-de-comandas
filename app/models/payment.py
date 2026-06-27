from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING

from beanie import Document, Link

if TYPE_CHECKING:
    from app.models.command import Command


class PaymentMethod(str, Enum):
    DINHEIRO = "DINHEIRO"
    CARTAO = "CARTAO"
    PIX = "PIX"


class PaymentStatus(str, Enum):
    PENDENTE = "PENDENTE"
    PAGO = "PAGO"
    ESTORNADO = "ESTORNADO"


class Payment(Document):
    """Representa um pagamento parcial ou total aplicado a uma comanda."""

    command: Link["Command"]
    amount: float = 0.0
    method: PaymentMethod = PaymentMethod.DINHEIRO
    status: PaymentStatus = PaymentStatus.PENDENTE
    paid_at: Optional[datetime] = None

    class Settings:
        name = "payments"
        indexes = ["status"]
