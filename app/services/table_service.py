from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors.exceptions import EntityNotFoundException
from app.models.table import Table
from app.repositories.table_repository import TableRepository
from app.schemas.table import TableCreate, TableUpdate


class TableService:
    """
    Serviço responsável pelo gerenciamento das Mesas do estabelecimento.
    
    Controla a criação de novas mesas físicas, listagem de mesas por status,
    atualização de dados e exclusão de mesas no banco de dados.
    """
    def __init__(self, session: AsyncSession) -> None:
        self.repo = TableRepository(session)

    async def create_table(self, data: TableCreate) -> Table:
        """Cria e retorna uma nova mesa."""
        return await self.repo.create(data)

    async def list_tables(self):
        """Retorna statement de listagem de todas as mesas."""
        return await self.repo.list_all()

    async def get_table(self, table_id: int) -> Table:
        """Retorna uma mesa pelo ID ou lança EntityNotFoundException."""
        table = await self.repo.get_by_id(table_id)
        if not table:
            raise EntityNotFoundException("Mesa", table_id)
        return table

    async def update_table(self, table_id: int, data: TableUpdate) -> Table:
        """Atualiza os dados de uma mesa existente."""
        table = await self.get_table(table_id)
        return await self.repo.update(table, data)

    async def delete_table(self, table_id: int) -> None:
        """Remove uma mesa pelo ID."""
        table = await self.get_table(table_id)
        await self.repo.delete(table)
