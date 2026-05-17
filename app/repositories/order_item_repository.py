from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models.order_item import OrderItem
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate


class OrderItemRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: OrderItemCreate) -> OrderItem:
        item = OrderItem.model_validate(data)
        self.session.add(item)
        await self.session.commit()
        # reload item with related product and order to avoid lazy IO during serialization
        statement = (
            select(OrderItem)
            .where(OrderItem.id == item.id)
            .options(selectinload(OrderItem.product), selectinload(OrderItem.order))
        )
        result = await self.session.execute(statement)
        return result.scalar_one()

    async def get_by_id(self, item_id: int) -> Optional[OrderItem]:
        statement = (
            select(OrderItem)
            .where(OrderItem.id == item_id)
            .options(selectinload(OrderItem.product), selectinload(OrderItem.order))
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_all(self, order_id: int | None = None, product_id: int | None = None):
        statement = select(OrderItem).options(selectinload(OrderItem.product)).order_by(OrderItem.id.desc())
        if order_id is not None:
            statement = statement.where(OrderItem.order_id == order_id)
        if product_id is not None:
            statement = statement.where(OrderItem.product_id == product_id)
        return statement

    async def update(self, item: OrderItem, data: OrderItemUpdate) -> OrderItem:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete(self, item: OrderItem) -> None:
        await self.session.delete(item)
        await self.session.commit()
