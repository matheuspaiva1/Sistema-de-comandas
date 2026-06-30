from typing import Optional

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.models.table import Table, TableStatus
from app.schemas.table import TableCreate, TableUpdate


class TableRepository:
    """Repositório de acesso a dados para a entidade Table."""

    async def create(self, data: TableCreate) -> Table:
        table = Table(**data.model_dump())
        await table.insert()
        return table

    async def get_by_id(self, table_id: PydanticObjectId) -> Optional[Table]:
        return await Table.get(table_id)

    def list_all(self, status: TableStatus | None = None) -> FindMany[Table]:
        query = {"status": status} if status else {}
        return Table.find(query).sort("number")

    async def update(self, table: Table, data: TableUpdate) -> Table:
        update_data = data.model_dump(exclude_unset=True)
        await table.set(update_data)
        return table

    async def delete(self, table: Table) -> None:
        await table.delete()
