from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


class ClientRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: ClientCreate) -> Client:
        client = Client.model_validate(data)
        self.session.add(client)
        await self.session.commit()
        await self.session.refresh(client)
        return client

    async def get_by_id(self, client_id: int) -> Optional[Client]:
        return await self.session.get(Client, client_id)

    async def list_all(self, search: str | None = None):
        statement = select(Client).order_by(Client.nome.asc())
        if search:
            statement = statement.where(Client.nome.ilike(f"%{search}%"))
        return statement

    async def update(self, client: Client, data: ClientUpdate) -> Client:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(client, key, value)
        self.session.add(client)
        await self.session.commit()
        await self.session.refresh(client)
        return client

    async def delete(self, client: Client) -> None:
        await self.session.delete(client)
        await self.session.commit()