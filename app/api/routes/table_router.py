from beanie import PydanticObjectId
from fastapi import APIRouter, status
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate

from app.schemas.table import TableCreate, TableRead, TableUpdate
from app.services.table_service import TableService

router = APIRouter(prefix="/tables", tags=["Mesas"])


@router.post("/", response_model=TableRead, status_code=status.HTTP_201_CREATED)
async def create_table(data: TableCreate):
    """Cria uma nova mesa."""
    return await TableService().create_table(data)


@router.get("/", response_model=Page[TableRead])
async def list_tables():
    """Lista todas as mesas."""
    return await paginate(TableService().list_tables())


@router.get("/{table_id}", response_model=TableRead)
async def get_table(table_id: PydanticObjectId):
    """Retorna uma mesa pelo ID."""
    return await TableService().get_table(table_id)


@router.put("/{table_id}", response_model=TableRead)
async def update_table(table_id: PydanticObjectId, data: TableUpdate):
    """Atualiza os dados de uma mesa."""
    return await TableService().update_table(table_id, data)


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(table_id: PydanticObjectId):
    """Remove uma mesa pelo ID."""
    await TableService().delete_table(table_id)
