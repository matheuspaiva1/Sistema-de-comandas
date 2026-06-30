from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.api.errors.exceptions import EntityNotFoundException
from app.models.table import Table, TableStatus
from app.repositories.table_repository import TableRepository
from app.schemas.table import TableCreate, TableUpdate


class TableService:
    """Lógica de negócios para a entidade Table."""

    def __init__(self) -> None:
        self.repo = TableRepository()

    async def create_table(self, data: TableCreate) -> Table:
        return await self.repo.create(data)

    def list_tables(self, status: TableStatus | None = None) -> FindMany[Table]:
        return self.repo.list_all(status=status)

    async def get_table(self, table_id: PydanticObjectId) -> Table:
        table = await self.repo.get_by_id(table_id)
        if not table:
            raise EntityNotFoundException("Mesa", str(table_id))
        return table

    async def update_table(self, table_id: PydanticObjectId, data: TableUpdate) -> Table:
        table = await self.get_table(table_id)
        return await self.repo.update(table, data)

    async def delete_table(self, table_id: PydanticObjectId) -> None:
        table = await self.get_table(table_id)
        await self.repo.delete(table)
