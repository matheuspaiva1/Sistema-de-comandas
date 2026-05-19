from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select

from app.models.item_command import ItemCommand
from app.schemas.item_command import ItemCommandCreate, ItemCommandUpdate


class ItemCommandRepository:
    """Repositório de acesso a dados para a entidade ItemCommand."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: ItemCommandCreate) -> ItemCommand:
        """Persiste um novo item de comanda e o retorna com relacionamentos carregados."""
        item = ItemCommand.model_validate(data)
        self.session.add(item)
        await self.session.commit()

        statement = (
            select(ItemCommand)
            .where(ItemCommand.id == item.id)
            .options(joinedload(ItemCommand.product), joinedload(ItemCommand.command))
        )
        result = await self.session.execute(statement)
        return result.scalar_one()

    async def get_by_id(self, item_id: int) -> Optional[ItemCommand]:
        """Retorna um item de comanda pelo ID com produto e comanda carregados, ou None."""
        statement = (
            select(ItemCommand)
            .where(ItemCommand.id == item_id)
            .options(joinedload(ItemCommand.product), joinedload(ItemCommand.command))
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_all(self, command_id: int | None = None, product_id: int | None = None):
        """Retorna statement de listagem de itens com filtros opcionais por comanda e produto."""
        statement = select(ItemCommand).options(joinedload(ItemCommand.product)).order_by(ItemCommand.id.desc())
        if command_id is not None:
            statement = statement.where(ItemCommand.command_id == command_id)
        if product_id is not None:
            statement = statement.where(ItemCommand.product_id == product_id)
        return statement

    async def update(self, item: ItemCommand, data: ItemCommandUpdate) -> ItemCommand:
        """Atualiza os campos fornecidos de um item de comanda existente."""
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete(self, item: ItemCommand) -> None:
        """Remove um item de comanda do banco de dados."""
        await self.session.delete(item)
        await self.session.commit()
