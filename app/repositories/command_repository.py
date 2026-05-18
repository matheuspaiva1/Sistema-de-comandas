from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models.command import Command
from app.models.item_command import ItemCommand
from app.schemas.command import CommandCreate, CommandUpdate


class CommandRepository:
    """Repositório de acesso a dados para a entidade Command."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: CommandCreate) -> Command:
        """Persiste uma nova comanda e a retorna com relacionamentos carregados."""
        command = Command.model_validate(data)
        self.session.add(command)
        await self.session.commit()
        await self.session.refresh(command)
        created = await self.get_by_id(command.id)
        return created or command

    async def get_by_id(self, command_id: int) -> Optional[Command]:
        """Retorna uma comanda pelo ID com cliente e itens carregados, ou None."""
        statement = (
            select(Command)
            .where(Command.id == command_id)
            .options(
                selectinload(Command.client),
                selectinload(Command.items).selectinload(ItemCommand.product),
            )
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_all(self, client_id: int | None = None, status: str | None = None):
        """Retorna statement de listagem de comandas com filtros opcionais por cliente e status."""
        statement = (
            select(Command)
            .options(
                selectinload(Command.client),
                selectinload(Command.items).selectinload(ItemCommand.product),
            )
            .order_by(Command.opened_at.desc())
        )
        if client_id is not None:
            statement = statement.where(Command.client_id == client_id)
        if status is not None:
            statement = statement.where(Command.status == status)
        return statement

    async def update(self, command: Command, data: CommandUpdate) -> Command:
        """Atualiza os campos fornecidos de uma comanda existente."""
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(command, key, value)
        self.session.add(command)
        await self.session.commit()
        await self.session.refresh(command)
        updated = await self.get_by_id(command.id)
        return updated or command

    async def delete(self, command: Command) -> None:
        """Remove uma comanda do banco de dados."""
        await self.session.delete(command)
        await self.session.commit()