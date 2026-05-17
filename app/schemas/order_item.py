from sqlmodel import SQLModel

from app.schemas.product import ProductRead


class OrderItemCreate(SQLModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: float


class OrderItemUpdate(SQLModel):
    product_id: int | None = None
    quantity: int | None = None
    unit_price: float | None = None


class OrderItemRead(SQLModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float
    product: ProductRead | None = None