from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


from app.models.table import Table
from app.schemas.table import TableCreate, TableUpdate


class TableRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: TableCreate) -> Table:
        table = Table.model_validate(data)
        self.session.add(table)
        await self.session.commit()
        await self.session.refresh(table)
        return table

    async def get_by_id(self, table_id: int) -> Optional[Table]:
        return await self.session.get(Table, table_id)

    async def list_all(self):
        return select(Table).order_by(Table.number)

    async def update(self, table: Table, data: TableUpdate) -> Table:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(table, key, value)
        self.session.add(table)
        await self.session.commit()
        await self.session.refresh(table)
        return table

    async def delete(self, table: Table) -> None:
        await self.session.delete(table)
        await self.session.commit()
