from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


class ClientRepository:
    """Repositório de acesso a dados para a entidade Client."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: ClientCreate) -> Client:
        """Persiste um novo cliente no banco de dados."""
        client = Client.model_validate(data)
        self.session.add(client)
        await self.session.commit()
        await self.session.refresh(client)
        return client

    async def get_by_id(self, client_id: int) -> Optional[Client]:
        """Retorna um cliente pelo seu ID, ou None se não encontrado."""
        return await self.session.get(Client, client_id)

    async def list_all(self, search: str | None = None):
        """Retorna statement de listagem de clientes, com filtro opcional por nome."""
        statement = select(Client).order_by(Client.name.asc())
        if search:
            statement = statement.where(Client.name.ilike(f"%{search}%"))
        return statement

    async def update(self, client: Client, data: ClientUpdate) -> Client:
        """Atualiza os campos fornecidos de um cliente existente."""
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(client, key, value)
        self.session.add(client)
        await self.session.commit()
        await self.session.refresh(client)
        return client

    async def delete(self, client: Client) -> None:
        """Remove um cliente do banco de dados."""
        await self.session.delete(client)
        await self.session.commit()