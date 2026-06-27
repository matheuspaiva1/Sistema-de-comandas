import enum

from beanie import Document


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

    class Settings:
        name = "products"
        indexes = ["name", "category", "active"]
