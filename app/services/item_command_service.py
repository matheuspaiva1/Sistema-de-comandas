from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors.exceptions import EntityNotFoundException
from app.models.item_command import ItemCommand
from app.repositories.item_command_repository import ItemCommandRepository
from app.repositories.command_repository import CommandRepository
from app.schemas.item_command import ItemCommandCreate, ItemCommandUpdate


class ItemCommandService:
    """
    Serviço responsável pelo gerenciamento de itens vinculados a uma Comanda.
    
    Permite adicionar produtos a uma comanda ativa, além de listar, atualizar
    quantidades/valores ou excluir itens já registrados nas comandas.
    """
    def __init__(self, session: AsyncSession) -> None:
        self.repo = ItemCommandRepository(session)
        self.command_repo = CommandRepository(session)

    async def create_item(self, data: ItemCommandCreate) -> ItemCommand:
        command = await self.command_repo.get_by_id(data.command_id)
        if not command:
            raise EntityNotFoundException("Comanda", data.command_id)
        return await self.repo.create(data)

    async def list_items(self, command_id: int | None = None, product_id: int | None = None):
        return await self.repo.list_all(command_id=command_id, product_id=product_id)

    async def get_item(self, item_id: int) -> ItemCommand:
        item = await self.repo.get_by_id(item_id)
        if not item:
            raise EntityNotFoundException("Item da Comanda", item_id)
        return item

    async def update_item(self, item_id: int, data: ItemCommandUpdate) -> ItemCommand:
        item = await self.get_item(item_id)
        return await self.repo.update(item, data)

    async def delete_item(self, item_id: int) -> None:
        item = await self.get_item(item_id)
        await self.repo.delete(item)
