import enum
from typing import Optional

from sqlmodel import Field, SQLModel


class CategoriaEnum(str, enum.Enum):
    BEBIDA = "BEBIDA"
    PRATO_PRINCIPAL = "PRATO_PRINCIPAL"
    ENTRADA = "ENTRADA"
    SOBREMESA = "SOBREMESA"
    LANCHE = "LANCHE"
    OUTRO = "OUTRO"


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    descricao: str = Field(max_length=500)
    categoria: CategoriaEnum
    preco: float
    ativo: bool = Field(default=True)
