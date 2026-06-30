from typing import Optional

from beanie.odm.fields import Link
from pydantic import BaseModel, field_validator

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

    @field_validator("product", mode="before")
    @classmethod
    def ignore_unresolved_link(cls, value):
        if isinstance(value, Link):
            return None
        return value

    model_config = {"from_attributes": True}
