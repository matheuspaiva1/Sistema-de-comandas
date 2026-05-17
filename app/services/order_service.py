from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors.exceptions import EntityNotFoundException
from app.models.order import Order
from app.repositories.order_repository import OrderRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.command_repository import CommandRepository
from app.schemas.order import OrderCreate, OrderUpdate


class OrderService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = OrderRepository(session)
        self.item_repo = OrderItemRepository(session)
        self.command_repo = CommandRepository(session)

    async def create_order(self, data: OrderCreate) -> Order:
        command = await self.command_repo.get_by_id(data.command_id)
        if not command:
            raise EntityNotFoundException("Comanda", data.command_id)
        return await self.repo.create(data)

    async def list_orders(self, command_id: int | None = None, status: str | None = None):
        return await self.repo.list_all(command_id=command_id, status=status)

    async def get_order(self, order_id: int) -> Order:
        order = await self.repo.get_by_id(order_id)
        if not order:
            raise EntityNotFoundException("Pedido", order_id)
        return order

    async def update_order(self, order_id: int, data: OrderUpdate) -> Order:
        order = await self.get_order(order_id)
        return await self.repo.update(order, data)

    async def delete_order(self, order_id: int) -> None:
        order = await self.get_order(order_id)
        await self.repo.delete(order)