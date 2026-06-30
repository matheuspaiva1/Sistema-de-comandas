from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.models.product import Product, CategoryEnum
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate
from app.api.errors.exceptions import ProductNotFoundException


class ProductService:
    """Lógica de negócios para a entidade Product."""

    def __init__(self) -> None:
        self.repo = ProductRepository()

    async def create_product(self, data: ProductCreate) -> Product:
        return await self.repo.create(data)

    def list_products(
        self,
        search: str | None = None,
        category: CategoryEnum | None = None,
        active_only: bool = True,
    ) -> FindMany[Product]:
        return self.repo.list_all(search=search, category=category, active_only=active_only)

    async def get_product(self, product_id: PydanticObjectId) -> Product:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(str(product_id))
        return product

    async def update_product(self, product_id: PydanticObjectId, data: ProductUpdate) -> Product:
        product = await self.get_product(product_id)
        return await self.repo.update(product, data)

    async def delete_product(self, product_id: PydanticObjectId) -> None:
        product = await self.get_product(product_id)
        await self.repo.delete(product)
