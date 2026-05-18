from typing import Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from fastapi_pagination.ext.sqlmodel import paginate

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    """Repositório de acesso a dados para a entidade Product."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: ProductCreate) -> Product:
        """Persiste um novo produto no banco de dados."""
        product = Product.model_validate(data)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """Retorna um produto pelo seu ID, ou None se não encontrado."""
        return await self.session.get(Product, product_id)

    async def list_all(self):
        """Retorna lista paginada de todos os produtos."""
        return await paginate(self.session, select(Product))

    async def update(self, product: Product, data: ProductUpdate) -> Product:
        """Atualiza os campos fornecidos de um produto existente."""
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self, product: Product) -> None:
        """Remove um produto do banco de dados."""
        await self.session.delete(product)
        await self.session.commit()
