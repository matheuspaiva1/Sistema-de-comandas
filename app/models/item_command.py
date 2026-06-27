from typing import Optional

from beanie import Link
from pydantic import BaseModel

from app.models.product import Product


class ItemCommand(BaseModel):
    """Item embutido dentro de uma comanda. Não tem coleção própria no banco."""

    product: Link[Product]
    quantity: int
    unit_price: float
    observation: Optional[str] = None
