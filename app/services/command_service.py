from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.api.errors.exceptions import EntityNotFoundException
from app.models.command import Command, CommandStatus
from app.models.item_command import ItemCommand
from app.repositories.command_repository import CommandRepository
from app.repositories.client_repository import ClientRepository
from app.repositories.table_repository import TableRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.command import CommandCreate, CommandUpdate
from app.schemas.item_command import ItemCommandCreate


class CommandService:
    """Lógica de negócios para Comandas e seus itens embutidos."""

    def __init__(self) -> None:
        self.repo = CommandRepository()
        self.client_repo = ClientRepository()
        self.table_repo = TableRepository()
        self.product_repo = ProductRepository()

    async def create_command(self, data: CommandCreate) -> Command:
        client_id = PydanticObjectId(data.client_id)
        client = await self.client_repo.get_by_id(client_id)
        if not client:
            raise EntityNotFoundException("Cliente", data.client_id)

        table = None
        if data.table_id:
            table = await self.table_repo.get_by_id(PydanticObjectId(data.table_id))
            if not table:
                raise EntityNotFoundException("Mesa", data.table_id)

        return await self.repo.create(client, data, table)

    def list_commands(
        self,
        client_id: Optional[str] = None,
        status: Optional[CommandStatus] = None,
    ) -> FindMany[Command]:
        parsed_client_id = PydanticObjectId(client_id) if client_id else None
        return self.repo.list_all(client_id=parsed_client_id, status=status)

    async def get_command(self, command_id: PydanticObjectId) -> Command:
        command = await self.repo.get_by_id(command_id)
        if not command:
            raise EntityNotFoundException("Comanda", str(command_id))
        return command

    async def update_command(self, command_id: PydanticObjectId, data: CommandUpdate) -> Command:
        command = await self.get_command(command_id)
        if data.status == CommandStatus.FECHADA and command.closed_at is None:
            data.closed_at = datetime.utcnow()
        return await self.repo.update(command, data)

    async def add_item(self, command_id: PydanticObjectId, data: ItemCommandCreate) -> Command:
        command = await self.get_command(command_id)
        product = await self.product_repo.get_by_id(PydanticObjectId(data.product_id))
        if not product:
            raise EntityNotFoundException("Produto", data.product_id)
        item = ItemCommand(product=product, quantity=data.quantity, unit_price=data.unit_price, observation=data.observation)
        return await self.repo.add_item(command, item)

    async def remove_item(self, command_id: PydanticObjectId, item_index: int) -> Command:
        command = await self.get_command(command_id)
        if item_index < 0 or item_index >= len(command.items):
            raise EntityNotFoundException("Item da Comanda", str(item_index))
        return await self.repo.remove_item(command, item_index)

    async def delete_command(self, command_id: PydanticObjectId) -> None:
        command = await self.get_command(command_id)
        await self.repo.delete(command)
