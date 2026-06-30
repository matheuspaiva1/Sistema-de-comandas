from typing import Optional

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


class ClientRepository:
    """Repositório de acesso a dados para a entidade Client."""

    async def create(self, data: ClientCreate) -> Client:
        client = Client(**data.model_dump())
        await client.insert()
        return client

    async def get_by_id(self, client_id: PydanticObjectId) -> Optional[Client]:
        return await Client.get(client_id)

    def list_all(self, search: str | None = None) -> FindMany[Client]:
        if search:
            return Client.find({"name": {"$regex": search, "$options": "i"}}).sort("name")
        return Client.find_all().sort("name")

    async def update(self, client: Client, data: ClientUpdate) -> Client:
        update_data = data.model_dump(exclude_unset=True)
        await client.set(update_data)
        return client

    async def delete(self, client: Client) -> None:
        await client.delete()
