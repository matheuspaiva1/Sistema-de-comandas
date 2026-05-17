from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.product import CategoryEnum


class ProductCreate(SQLModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=500)
    category: CategoryEnum
    price: float
    active: Optional[bool] = True


class ProductUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    category: Optional[CategoryEnum] = None
    price: Optional[float] = None
    active: Optional[bool] = None


class ProductRead(SQLModel):
    id: int
    name: str
    description: str
    category: CategoryEnum
    price: float
    active: bool
