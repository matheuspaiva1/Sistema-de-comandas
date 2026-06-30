import enum
from pymongo import IndexModel, TEXT

from beanie import Document, Link
from pydantic import Field

from app.models.document import FileDocument


class CategoryEnum(str, enum.Enum):
    BEBIDA = "BEBIDA"
    PRATO_PRINCIPAL = "PRATO_PRINCIPAL"
    ENTRADA = "ENTRADA"
    SOBREMESA = "SOBREMESA"
    LANCHE = "LANCHE"
    OUTRO = "OUTRO"


class Product(Document):
    """Representa um produto do cardápio do estabelecimento."""

    name: str
    description: str
    category: CategoryEnum
    price: float
    active: bool = True
    documents: list[Link[FileDocument]] = Field(default_factory=list)

    class Settings:
        name = "products"
        indexes = [
            IndexModel([("name", TEXT), ("description", TEXT)], name="product_text_index"),
            "name",
            "category",
            "active",
        ]

