from typing import Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: ProductCreate) -> Product:
        product = Product.model_validate(data)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        return await self.session.get(Product, product_id)

    async def list_all(self) -> Sequence[Product]:
        result = await self.session.exec(select(Product))
        return result.all()

    async def update(self, product: Product, data: ProductUpdate) -> Product:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self, product: Product) -> None:
        await self.session.delete(product)
        await self.session.commit()
