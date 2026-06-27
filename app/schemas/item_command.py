from typing import Optional

from pydantic import BaseModel

from app.schemas import PyObjectId
from app.schemas.product import ProductRead


class ItemCommandCreate(BaseModel):
    product_id: PyObjectId
    quantity: int
    unit_price: float
    observation: Optional[str] = None


class ItemCommandUpdate(BaseModel):
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    observation: Optional[str] = None


class ItemCommandRead(BaseModel):
    quantity: int
    unit_price: float
    observation: Optional[str] = None
    product: Optional[ProductRead] = None

    model_config = {"from_attributes": True}
