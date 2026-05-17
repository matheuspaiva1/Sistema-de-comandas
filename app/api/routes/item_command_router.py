from fastapi import APIRouter, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import apaginate

from app.api.deps import SessionDep
from app.schemas.item_command import ItemCommandCreate, ItemCommandRead, ItemCommandUpdate
from app.services.item_command_service import ItemCommandService

router = APIRouter(prefix="/itens-comanda", tags=["Itens da Comanda"])


@router.post("/", response_model=ItemCommandRead, status_code=status.HTTP_201_CREATED)
async def create_item(data: ItemCommandCreate, session: SessionDep):
    service = ItemCommandService(session)
    return await service.create_item(data)


@router.get("/", response_model=Page[ItemCommandRead])
async def list_items(
    session: SessionDep,
    command_id: int | None = Query(default=None, ge=1),
    product_id: int | None = Query(default=None, ge=1),
):
    service = ItemCommandService(session)
    statement = await service.list_items(command_id=command_id, product_id=product_id)
    return await apaginate(session, statement)


@router.get("/{item_id}", response_model=ItemCommandRead)
async def get_item(item_id: int, session: SessionDep):
    service = ItemCommandService(session)
    return await service.get_item(item_id)


@router.put("/{item_id}", response_model=ItemCommandRead)
async def update_item(item_id: int, data: ItemCommandUpdate, session: SessionDep):
    service = ItemCommandService(session)
    return await service.update_item(item_id, data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, session: SessionDep):
    service = ItemCommandService(session)
    await service.delete_item(item_id)
