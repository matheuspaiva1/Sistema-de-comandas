from beanie import PydanticObjectId
from fastapi import APIRouter, Query, status

from app.models.command import CommandStatus
from app.schemas.command import CommandCreate, CommandRead, CommandUpdate
from app.schemas.item_command import ItemCommandCreate, ItemCommandRead
from app.services.command_service import CommandService

router = APIRouter(prefix="/comandas", tags=["Comandas"])


@router.post("/", response_model=CommandRead, status_code=status.HTTP_201_CREATED)
async def create_command(data: CommandCreate):
    """Cria uma nova comanda."""
    return await CommandService().create_command(data)


@router.get("/", response_model=list[CommandRead])
async def list_commands(
    client_id: str | None = Query(default=None),
    status_: CommandStatus | None = Query(default=None, alias="status"),
):
    """Lista comandas com filtros opcionais por cliente e status."""
    return await CommandService().list_commands(client_id=client_id, status=status_)


@router.get("/{command_id}", response_model=CommandRead)
async def get_command(command_id: PydanticObjectId):
    """Retorna uma comanda pelo ID."""
    return await CommandService().get_command(command_id)


@router.put("/{command_id}", response_model=CommandRead)
async def update_command(command_id: PydanticObjectId, data: CommandUpdate):
    """Atualiza os dados de uma comanda."""
    return await CommandService().update_command(command_id, data)


@router.delete("/{command_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_command(command_id: PydanticObjectId):
    """Remove uma comanda pelo ID."""
    await CommandService().delete_command(command_id)


@router.post("/{command_id}/items", response_model=CommandRead, status_code=status.HTTP_201_CREATED)
async def add_item(command_id: PydanticObjectId, data: ItemCommandCreate):
    """Adiciona um item à comanda."""
    return await CommandService().add_item(command_id, data)


@router.delete("/{command_id}/items/{item_index}", response_model=CommandRead)
async def remove_item(command_id: PydanticObjectId, item_index: int):
    """Remove um item da comanda pelo índice na lista."""
    return await CommandService().remove_item(command_id, item_index)
