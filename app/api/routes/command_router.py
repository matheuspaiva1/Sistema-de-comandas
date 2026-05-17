from fastapi import APIRouter, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import apaginate

from app.api.deps import SessionDep
from app.schemas.command import CommandCreate, CommandRead, CommandUpdate
from app.services.command_service import CommandService

router = APIRouter(prefix="/comandas", tags=["Comandas"])


@router.post("/", response_model=CommandRead, status_code=status.HTTP_201_CREATED)
async def create_command(data: CommandCreate, session: SessionDep):
    service = CommandService(session)
    return await service.create_command(data)


@router.get("/", response_model=Page[CommandRead])
async def list_commands(
    session: SessionDep,
    client_id: int | None = Query(default=None, ge=1),
    status_: str | None = Query(default=None, alias="status"),
):
    service = CommandService(session)
    statement = await service.list_commands(client_id=client_id, status=status_)
    return await apaginate(session, statement)


@router.get("/{command_id}", response_model=CommandRead)
async def get_command(command_id: int, session: SessionDep):
    service = CommandService(session)
    return await service.get_command(command_id)


@router.put("/{command_id}", response_model=CommandRead)
async def update_command(command_id: int, data: CommandUpdate, session: SessionDep):
    service = CommandService(session)
    return await service.update_command(command_id, data)


@router.delete("/{command_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_command(command_id: int, session: SessionDep):
    service = CommandService(session)
    await service.delete_command(command_id)