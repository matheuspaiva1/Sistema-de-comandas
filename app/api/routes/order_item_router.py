from fastapi import APIRouter, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import apaginate

from app.api.deps import SessionDep
from app.schemas.order_item import OrderItemCreate, OrderItemRead, OrderItemUpdate
from app.services.order_item_service import OrderItemService

router = APIRouter(prefix="/itens-pedido", tags=["Itens do Pedido"])


@router.post("/", response_model=OrderItemRead, status_code=status.HTTP_201_CREATED)
async def create_order_item(data: OrderItemCreate, session: SessionDep):
    service = OrderItemService(session)
    return await service.create_order_item(data)


@router.get("/", response_model=Page[OrderItemRead])
async def list_order_items(
    session: SessionDep,
    order_id: int | None = Query(default=None, ge=1),
    product_id: int | None = Query(default=None, ge=1),
):
    service = OrderItemService(session)
    statement = await service.list_order_items(order_id=order_id, product_id=product_id)
    return await apaginate(session, statement)


@router.get("/{item_id}", response_model=OrderItemRead)
async def get_order_item(item_id: int, session: SessionDep):
    service = OrderItemService(session)
    return await service.get_order_item(item_id)


@router.put("/{item_id}", response_model=OrderItemRead)
async def update_order_item(item_id: int, data: OrderItemUpdate, session: SessionDep):
    service = OrderItemService(session)
    return await service.update_order_item(item_id, data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_item(item_id: int, session: SessionDep):
    service = OrderItemService(session)
    await service.delete_order_item(item_id)
