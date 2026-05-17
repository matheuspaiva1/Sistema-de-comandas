from fastapi import APIRouter, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import apaginate

from app.api.deps import SessionDep
from app.schemas.order import OrderCreate, OrderRead, OrderUpdate
from app.services.order_service import OrderService

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(data: OrderCreate, session: SessionDep):
    service = OrderService(session)
    return await service.create_order(data)


@router.get("/", response_model=Page[OrderRead])
async def list_orders(
    session: SessionDep,
    command_id: int | None = Query(default=None, ge=1),
    status_: str | None = Query(default=None, alias="status"),
):
    service = OrderService(session)
    statement = await service.list_orders(command_id=command_id, status=status_)
    return await apaginate(session, statement)


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: int, session: SessionDep):
    service = OrderService(session)
    return await service.get_order(order_id)


@router.put("/{order_id}", response_model=OrderRead)
async def update_order(order_id: int, data: OrderUpdate, session: SessionDep):
    service = OrderService(session)
    return await service.update_order(order_id, data)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, session: SessionDep):
    service = OrderService(session)
    await service.delete_order(order_id)