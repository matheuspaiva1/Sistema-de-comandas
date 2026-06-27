from typing import Optional

from beanie import PydanticObjectId

from app.models.product import Product, CategoryEnum
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    """Repositório de acesso a dados para a entidade Product."""

    async def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        await product.insert()
        return product

    async def get_by_id(self, product_id: PydanticObjectId) -> Optional[Product]:
        return await Product.get(product_id)

    async def list_all(
        self,
        search: str | None = None,
        category: CategoryEnum | None = None,
        active_only: bool = True,
    ) -> list[Product]:
        query: dict = {}
        if active_only:
            query["active"] = True
        if category:
            query["category"] = category
        if search:
            query["name"] = {"$regex": search, "$options": "i"}
        return await Product.find(query).sort("name").to_list()

    async def update(self, product: Product, data: ProductUpdate) -> Product:
        update_data = data.model_dump(exclude_unset=True)
        await product.set(update_data)
        return product

    async def delete(self, product: Product) -> None:
        await product.delete()
