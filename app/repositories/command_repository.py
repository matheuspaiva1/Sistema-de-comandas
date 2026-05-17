from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models.command import Command
from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.command import CommandCreate, CommandUpdate


class CommandRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: CommandCreate) -> Command:
        command = Command.model_validate(data)
        self.session.add(command)
        await self.session.commit()
        await self.session.refresh(command)
        created = await self.get_by_id(command.id)
        return created or command

    async def get_by_id(self, command_id: int) -> Optional[Command]:
        statement = (
            select(Command)
            .where(Command.id == command_id)
            .options(
                selectinload(Command.client),
                selectinload(Command.orders)
                .selectinload(Order.items)
                .selectinload(OrderItem.product),
            )
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_all(self, client_id: int | None = None, status: str | None = None):
        statement = (
            select(Command)
            .options(
                selectinload(Command.client),
                selectinload(Command.orders)
                .selectinload(Order.items)
                .selectinload(OrderItem.product),
            )
            .order_by(Command.opened_at.desc())
        )
        if client_id is not None:
            statement = statement.where(Command.client_id == client_id)
        if status is not None:
            statement = statement.where(Command.status == status)
        return statement

    async def update(self, command: Command, data: CommandUpdate) -> Command:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(command, key, value)
        self.session.add(command)
        await self.session.commit()
        await self.session.refresh(command)
        updated = await self.get_by_id(command.id)
        return updated or command

    async def delete(self, command: Command) -> None:
        await self.session.delete(command)
        await self.session.commit()