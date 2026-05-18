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
    """
    Serviço responsável pela lógica de negócios dos Produtos.
    
    Gerencia o cadastro, atualização de preços/descrições, exclusão e
    listagem de produtos ativos e inativos do cardápio do estabelecimento.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.repo = ProductRepository(session)

    async def create_product(self, data: ProductCreate) -> Product:
        """Cria e retorna um novo produto."""
        return await self.repo.create(data)

    async def list_products(self):
        """Retorna lista paginada de todos os produtos."""
        return await self.repo.list_all()

    async def get_product(self, product_id: int) -> Product:
        """Retorna um produto pelo ID ou lança ProductNotFoundException."""
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id)
        return product

    async def update_product(self, product_id: int, data: ProductUpdate) -> Product:
        """Atualiza os dados de um produto existente."""
        product = await self.get_product(product_id)
        return await self.repo.update(product, data)

    async def delete_product(self, product_id: int) -> None:
        """Remove um produto pelo ID."""
        product = await self.get_product(product_id)
        
        await self.repo.delete(product)
