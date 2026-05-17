from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models.item_command import ItemCommand
from app.schemas.item_command import ItemCommandCreate, ItemCommandUpdate


class ItemCommandRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: ItemCommandCreate) -> ItemCommand:
        item = ItemCommand.model_validate(data)
        self.session.add(item)
        await self.session.commit()
        # reload item with related product and command to avoid lazy IO during serialization
        statement = (
            select(ItemCommand)
            .where(ItemCommand.id == item.id)
            .options(selectinload(ItemCommand.product), selectinload(ItemCommand.command))
        )
        result = await self.session.execute(statement)
        return result.scalar_one()

    async def get_by_id(self, item_id: int) -> Optional[ItemCommand]:
        statement = (
            select(ItemCommand)
            .where(ItemCommand.id == item_id)
            .options(selectinload(ItemCommand.product), selectinload(ItemCommand.command))
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_all(self, command_id: int | None = None, product_id: int | None = None):
        statement = select(ItemCommand).options(selectinload(ItemCommand.product)).order_by(ItemCommand.id.desc())
        if command_id is not None:
            statement = statement.where(ItemCommand.command_id == command_id)
        if product_id is not None:
            statement = statement.where(ItemCommand.product_id == product_id)
        return statement

    async def update(self, item: ItemCommand, data: ItemCommandUpdate) -> ItemCommand:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete(self, item: ItemCommand) -> None:
        await self.session.delete(item)
        await self.session.commit()
