from beanie import PydanticObjectId
from fastapi import APIRouter, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate

from app.schemas.client import ClientCreate, ClientRead, ClientUpdate
from app.services.client_service import ClientService

router = APIRouter(prefix="/clientes", tags=["Cliente"])


@router.post("/", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
async def create_client(data: ClientCreate):
    """Cria um novo cliente."""
    return await ClientService().create_client(data)


@router.get("/", response_model=Page[ClientRead])
async def list_clients(search: str | None = Query(default=None, max_length=100)):
    """Lista clientes com filtro opcional por nome."""
    return await paginate(ClientService().list_clients(search=search))


@router.get("/{client_id}", response_model=ClientRead)
async def get_client(client_id: PydanticObjectId):
    """Retorna um cliente pelo ID."""
    return await ClientService().get_client(client_id)


@router.put("/{client_id}", response_model=ClientRead)
async def update_client(client_id: PydanticObjectId, data: ClientUpdate):
    """Atualiza os dados de um cliente."""
    return await ClientService().update_client(client_id, data)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(client_id: PydanticObjectId):
    """Remove um cliente pelo ID."""
    await ClientService().delete_client(client_id)
