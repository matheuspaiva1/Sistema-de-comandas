from sqlmodel import SQLModel

from app.schemas.product import ProductRead


class ItemCommandCreate(SQLModel):
    command_id: int
    product_id: int
    quantity: int
    unit_price: float


class ItemCommandUpdate(SQLModel):
    product_id: int | None = None
    quantity: int | None = None
    unit_price: float | None = None


class ItemCommandRead(SQLModel):
    id: int
    command_id: int
    product_id: int
    quantity: int
    unit_price: float
    product: ProductRead | None = None
