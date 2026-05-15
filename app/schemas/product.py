from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.product import CategoriaEnum


class ProductCreate(SQLModel):
    nome: str = Field(max_length=100)
    descricao: str = Field(max_length=500)
    categoria: CategoriaEnum
    preco: float
    ativo: Optional[bool] = True


class ProductUpdate(SQLModel):
    nome: Optional[str] = Field(default=None, max_length=100)
    descricao: Optional[str] = Field(default=None, max_length=500)
    categoria: Optional[CategoriaEnum] = None
    preco: Optional[float] = None
    ativo: Optional[bool] = None


class ProductRead(SQLModel):
    id: int
    nome: str
    descricao: str
    categoria: CategoriaEnum
    preco: float
    ativo: bool
