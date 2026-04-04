from fastapi import APIRouter, HTTPException
from app.domains.comanda.comanda_schema import (
    CreateCommands,
    UpdateCommands,
)
from app.services import comanda_service

router = APIRouter(prefix="/comandas", tags=["Comandas"])

@router.post("")
def create(comanda: CreateCommands):
    return comanda_service.create_commands(comanda.model_dump())

@router.get("")
def list(page: int = 1, page_size: int = 10):
    return comanda_service.list_commands(page, page_size)

@router.get("/count")
def count():
    return {"total": comanda_service.count_commands()}

@router.get("/{id}")
def search(id: int):
    result = comanda_service.search_commands(id)
    if not result:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")

    return result

@router.put("/{id}")
def update(id: int, comanda: UpdateCommands):
    result = comanda_service.update_commands(id, comanda.model_dump(exclude_none=True))
    if not result:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")

    return result

@router.delete("/{id}")
def delete(id: int):
    if not comanda_service.delete_commands(id):
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    return {"detail": "Comanda deletada com sucesso"}