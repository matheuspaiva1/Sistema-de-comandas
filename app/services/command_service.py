from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors.exceptions import EntityNotFoundException
from app.models.command import Command
from app.repositories.command_repository import CommandRepository
from app.repositories.order_repository import OrderRepository
from app.schemas.command import CommandCreate, CommandUpdate


class CommandService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = CommandRepository(session)
        self.order_repo = OrderRepository(session)

    async def create_command(self, data: CommandCreate) -> Command:
        return await self.repo.create(data)

    async def list_commands(self, client_id: int | None = None, status: str | None = None):
        return await self.repo.list_all(client_id=client_id, status=status)

    async def get_command(self, command_id: int) -> Command:
        command = await self.repo.get_by_id(command_id)
        if not command:
            raise EntityNotFoundException("Comanda", command_id)
        return command

    async def update_command(self, command_id: int, data: CommandUpdate) -> Command:
        command = await self.get_command(command_id)
        if data.status and data.status.value == "FECHADA" and data.closed_at is None:
            data.closed_at = datetime.utcnow()
        return await self.repo.update(command, data)

    async def delete_command(self, command_id: int) -> None:
        command = await self.get_command(command_id)
        await self.repo.delete(command)