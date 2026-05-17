from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors.exceptions import EntityNotFoundException
from app.models.table import Table
from app.repositories.table_repository import TableRepository
from app.schemas.table import TableCreate, TableUpdate


class TableService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = TableRepository(session)

    async def create_table(self, data: TableCreate) -> Table:
        return await self.repo.create(data)

    async def list_tables(self):
        return await self.repo.list_all()

    async def get_table(self, table_id: int) -> Table:
        table = await self.repo.get_by_id(table_id)
        if not table:
            raise EntityNotFoundException("Mesa", table_id)
        return table

    async def update_table(self, table_id: int, data: TableUpdate) -> Table:
        table = await self.get_table(table_id)
        return await self.repo.update(table, data)

    async def delete_table(self, table_id: int) -> None:
        table = await self.get_table(table_id)
        await self.repo.delete(table)
