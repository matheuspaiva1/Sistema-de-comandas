from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors.exceptions import EntityNotFoundException
from app.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate, ClientUpdate


class ClientService:
    """
    Serviço responsável pela lógica de negócios associada a Clientes.
    
    Realiza a criação, leitura, atualização e exclusão (CRUD) de clientes
    fazendo a ponte entre os controladores da API e o repositório de clientes.
    """
    def __init__(self, session: AsyncSession) -> None:
        self.repo = ClientRepository(session)

    async def create_client(self, data: ClientCreate) -> Client:
        """Cria e retorna um novo cliente."""
        return await self.repo.create(data)

    async def list_clients(self, search: str | None = None):
        """Retorna statement de listagem de clientes com filtro opcional por nome."""
        return await self.repo.list_all(search=search)

    async def get_client(self, client_id: int) -> Client:
        """Retorna um cliente pelo ID ou lança EntityNotFoundException."""
        client = await self.repo.get_by_id(client_id)
        if not client:
            raise EntityNotFoundException("Cliente", client_id)
        return client

    async def update_client(self, client_id: int, data: ClientUpdate) -> Client:
        """Atualiza os dados de um cliente existente."""
        client = await self.get_client(client_id)
        return await self.repo.update(client, data)

    async def delete_client(self, client_id: int) -> None:
        """Remove um cliente pelo ID."""
        client = await self.get_client(client_id)
        await self.repo.delete(client)