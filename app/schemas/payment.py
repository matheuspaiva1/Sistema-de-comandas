from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.payment import PaymentMethod, PaymentStatus
from app.schemas import PyObjectId


class PaymentCreate(BaseModel):
    command_id: str
    amount: float
    method: Optional[PaymentMethod] = PaymentMethod.DINHEIRO


class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    paid_at: Optional[datetime] = None


class PaymentRead(BaseModel):
    id: PyObjectId
    amount: float
    method: Optional[PaymentMethod] = None
    status: Optional[PaymentStatus] = None
    paid_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
