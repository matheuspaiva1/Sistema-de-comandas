from fastapi import APIRouter, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import apaginate

from app.api.deps import SessionDep
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate
from app.services.client_service import ClientService

router = APIRouter(prefix="/clientes", tags=["Cliente"])


@router.post("/", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
async def create_client(data: ClientCreate, session: SessionDep):
    """Cria um novo cliente."""
    service = ClientService(session)
    return await service.create_client(data)


@router.get("/", response_model=Page[ClientRead])
async def list_clients(session: SessionDep, search: str | None = Query(default=None, max_length=100)):
    """Lista clientes com paginação e filtro opcional por nome."""
    service = ClientService(session)
    statement = await service.list_clients(search=search)
    return await apaginate(session, statement)


@router.get("/{client_id}", response_model=ClientRead)
async def get_client(client_id: int, session: SessionDep):
    """Retorna um cliente pelo ID."""
    service = ClientService(session)
    return await service.get_client(client_id)


@router.put("/{client_id}", response_model=ClientRead)
async def update_client(client_id: int, data: ClientUpdate, session: SessionDep):
    """Atualiza os dados de um cliente."""
    service = ClientService(session)
    return await service.update_client(client_id, data)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(client_id: int, session: SessionDep):
    """Remove um cliente pelo ID."""
    service = ClientService(session)
    await service.delete_client(client_id)