from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors.exceptions import EntityNotFoundException
from app.models.order_item import OrderItem
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.command_repository import CommandRepository
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate


class OrderItemService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = OrderItemRepository(session)
        self.order_repo = OrderRepository(session)
        self.command_repo = CommandRepository(session)

    async def create_order_item(self, data: OrderItemCreate) -> OrderItem:
        order = await self.order_repo.get_by_id(data.order_id)
        if not order:
            raise EntityNotFoundException("Pedido", data.order_id)
        return await self.repo.create(data)

    async def list_order_items(self, order_id: int | None = None, product_id: int | None = None):
        return await self.repo.list_all(order_id=order_id, product_id=product_id)

    async def get_order_item(self, item_id: int) -> OrderItem:
        item = await self.repo.get_by_id(item_id)
        if not item:
            raise EntityNotFoundException("Item do Pedido", item_id)
        return item

    async def update_order_item(self, item_id: int, data: OrderItemUpdate) -> OrderItem:
        item = await self.get_order_item(item_id)
        return await self.repo.update(item, data)

    async def delete_order_item(self, item_id: int) -> None:
        item = await self.get_order_item(item_id)
        await self.repo.delete(item)