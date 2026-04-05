from fastapi import APIRouter, HTTPException, Query

from app.domains.item_comanda import item_comanda_service
from app.domains.item_comanda.item_comanda_schema import (
    CreateItemComanda,
    UpdateItemComanda,
    ItemComandaResponse,
)

router = APIRouter(prefix="/itens-comanda", tags=["Itens de comanda"])


@router.post("", response_model=ItemComandaResponse, status_code=201)
def create(item: CreateItemComanda):
    return item_comanda_service.create_item(item.model_dump())


@router.get("", response_model=list[ItemComandaResponse])
def list_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    comanda_id: int | None = Query(None, ge=1),
):
    return item_comanda_service.list_items(page, page_size, comanda_id=comanda_id)


@router.get("/count")
def count(comanda_id: int | None = Query(None, ge=1)):
    return {"total": item_comanda_service.count_items(comanda_id=comanda_id)}


@router.get("/{id}", response_model=ItemComandaResponse)
def get(id: int):
    result = item_comanda_service.get_item(id)
    if not result:
        raise HTTPException(status_code=404, detail="Item de comanda não encontrado")
    return result


@router.put("/{id}", response_model=ItemComandaResponse)
def update(id: int, item: UpdateItemComanda):
    result = item_comanda_service.update_item(
        id, item.model_dump(exclude_none=True)
    )
    if not result:
        raise HTTPException(status_code=404, detail="Item de comanda não encontrado")
    return result


@router.delete("/{id}", status_code=204)
def delete(id: int):
    if not item_comanda_service.delete_item(id):
        raise HTTPException(status_code=404, detail="Item de comanda não encontrado")