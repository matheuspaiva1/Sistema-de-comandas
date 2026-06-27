from typing import Optional

from beanie import PydanticObjectId

from app.models.command import Command, CommandStatus
from app.models.client import Client
from app.models.table import Table
from app.models.item_command import ItemCommand
from app.schemas.command import CommandCreate, CommandUpdate


class CommandRepository:
    """Repositório de acesso a dados para a entidade Command."""

    async def create(self, client: Client, data: CommandCreate, table: Optional[Table] = None) -> Command:
        command = Command(
            client=client,
            table=table,
            status=CommandStatus.ABERTA,
        )
        await command.insert()
        return command

    async def get_by_id(self, command_id: PydanticObjectId) -> Optional[Command]:
        return await Command.get(command_id, fetch_links=True)

    async def list_all(
        self,
        client_id: PydanticObjectId | None = None,
        status: CommandStatus | None = None,
    ) -> list[Command]:
        query: dict = {}
        if client_id:
            query["client.$id"] = client_id
        if status:
            query["status"] = status
        return await Command.find(query, fetch_links=True).sort("-opened_at").to_list()

    async def add_item(self, command: Command, item: ItemCommand) -> Command:
        """Adiciona um item embutido à comanda e recalcula o total."""
        command.items.append(item)
        command.total_amount = sum(i.quantity * i.unit_price for i in command.items)
        await command.save()
        return command

    async def remove_item(self, command: Command, item_index: int) -> Command:
        """Remove um item pelo índice na lista e recalcula o total."""
        command.items.pop(item_index)
        command.total_amount = sum(i.quantity * i.unit_price for i in command.items)
        await command.save()
        return command

    async def update(self, command: Command, data: CommandUpdate) -> Command:
        update_data = data.model_dump(exclude_unset=True)
        await command.set(update_data)
        return command

    async def delete(self, command: Command) -> None:
        await command.delete()
