from typing import Optional

from pydantic import BaseModel

from app.models.product import CategoryEnum
from app.schemas import PyObjectId


class ProductCreate(BaseModel):
    name: str
    description: str
    category: CategoryEnum
    price: float
    active: Optional[bool] = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[CategoryEnum] = None
    price: Optional[float] = None
    active: Optional[bool] = None


class ProductRead(BaseModel):
    id: PyObjectId
    name: str
    description: str
    category: CategoryEnum
    price: float
    active: bool

    model_config = {"from_attributes": True}
