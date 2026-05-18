from fastapi import APIRouter, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import apaginate

from app.api.deps import SessionDep
from app.models.table import Table
from app.schemas.table import TableCreate, TableRead, TableUpdate
from app.services.table_service import TableService

router = APIRouter(prefix="/tables", tags=["Mesas"])


@router.post("/", response_model=TableRead, status_code=status.HTTP_201_CREATED)
async def create_table(data: TableCreate, session: SessionDep) -> Table:
    """Cria uma nova mesa."""
    service = TableService(session)
    return await service.create_table(data)


@router.get("/", response_model=Page[TableRead])
async def list_tables(session: SessionDep):
    """Lista todas as mesas com paginação."""
    service = TableService(session)
    statement = await service.list_tables()
    return await apaginate(session, statement)


@router.get("/{table_id}", response_model=TableRead)
async def get_table(table_id: int, session: SessionDep) -> Table:
    """Retorna uma mesa pelo ID."""
    service = TableService(session)
    return await service.get_table(table_id)


@router.put("/{table_id}", response_model=TableRead)
async def update_table(table_id: int, data: TableUpdate, session: SessionDep) -> Table:
    """Atualiza os dados de uma mesa."""
    service = TableService(session)
    return await service.update_table(table_id, data)


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(table_id: int, session: SessionDep) -> None:
    """Remove uma mesa pelo ID."""
    service = TableService(session)
    await service.delete_table(table_id)
