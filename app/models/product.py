import enum
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship


class CategoryEnum(str, enum.Enum):
    BEBIDA = "BEBIDA"
    PRATO_PRINCIPAL = "PRATO_PRINCIPAL"
    ENTRADA = "ENTRADA"
    SOBREMESA = "SOBREMESA"
    LANCHE = "LANCHE"
    OUTRO = "OUTRO"


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: str = Field(max_length=500)
    category: CategoryEnum
    price: float
    active: bool = Field(default=True)

    documents: list["Document"] = Relationship(back_populates="product")
    item_commands: list["ItemCommand"] = Relationship(back_populates="product")
