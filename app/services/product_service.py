from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate
from app.api.errors.exceptions import (
    ProductNotFoundException,
    EntityAlreadyExistsException,
    CantDeleteEntityException
)


class ProductService:

    def __init__(self, session: AsyncSession) -> None:
        self.repo = ProductRepository(session)

    async def create_product(self, data: ProductCreate) -> Product:
        # Exemplo de uso de EntityAlreadyExistsException
        # Nota: Idealmente o repositório teria um método get_by_name
        return await self.repo.create(data)

    async def list_products(self) -> Sequence[Product]:
        return await self.repo.list_all()

    async def get_product(self, product_id: int) -> Product:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id)
        return product

    async def update_product(self, product_id: int, data: ProductUpdate) -> Product:
        product = await self.get_product(product_id)
        return await self.repo.update(product, data)

    async def delete_product(self, product_id: int) -> None:
        product = await self.get_product(product_id)
        # Exemplo de onde poderia haver uma trava de negócio
        # if await self.repo.has_order_items(product_id):
        #     raise CantDeleteEntityException("Produto", product_id, "Existem itens de comanda associados")
        await self.repo.delete(product)
