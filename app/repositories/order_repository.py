from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.order import OrderCreate, OrderUpdate


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: OrderCreate) -> Order:
        order = Order.model_validate(data)
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        created = await self.get_by_id(order.id)
        return created or order

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        statement = (
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.items).selectinload(OrderItem.product), selectinload(Order.command))
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_all(self, command_id: int | None = None, status: str | None = None):
        statement = (
            select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.product), selectinload(Order.command))
            .order_by(Order.created_at.desc())
        )
        if command_id is not None:
            statement = statement.where(Order.command_id == command_id)
        if status is not None:
            statement = statement.where(Order.status == status)
        return statement

    async def update(self, order: Order, data: OrderUpdate) -> Order:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(order, key, value)
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        updated = await self.get_by_id(order.id)
        return updated or order

    async def delete(self, order: Order) -> None:
        await self.session.delete(order)
        await self.session.commit()