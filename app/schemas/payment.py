from datetime import datetime
from sqlmodel import SQLModel

from app.models.payment import PaymentMethod, PaymentStatus


class PaymentCreate(SQLModel):
    command_id: int | None = None
    amount: float
    method: PaymentMethod | None = None


class PaymentUpdate(SQLModel):
    status: PaymentStatus | None = None
    paid_at: datetime | None = None


class PaymentRead(SQLModel):
    id: int
    command_id: int | None = None
    amount: float
    method: PaymentMethod | None = None
    status: PaymentStatus | None = None
    paid_at: datetime | None = None