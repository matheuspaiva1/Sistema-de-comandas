from fastapi import APIRouter, HTTPException, Query

from app.domains.item_comanda import item_comanda_service
from app.domains.item_comanda.item_comanda_schema import (
    CreateItemComanda,
    UpdateItemComanda,
    ItemComandaResponse,
)

router = APIRouter(prefix="/itens-comanda", tags=["Itens de comanda"])


@router.post(
    "",
    response_model=ItemComandaResponse,
    status_code=201,
    summary="Criar item de comanda",
    description="""
Request:
- Body JSON no formato `CreateItemComanda`.
- Campos: `comanda_id`, `produto_id`, `quantidade` e `valor_unitario`.

Response:
- Retorna o item de comanda criado no formato `ItemComandaResponse`.
""",
    response_description="Item de comanda criado com sucesso",
)
def create(item: CreateItemComanda):
    return item_comanda_service.create_item(item.model_dump())


@router.get(
    "",
    response_model=list[ItemComandaResponse],
    summary="Listar itens de comanda",
    description="""
Request:
- Query params: `page` (padrão 1), `page_size` (padrão 10) e `comanda_id` opcional.

Response:
- Retorna a lista paginada de itens de comanda no formato `ItemComandaResponse`.
""",
    response_description="Lista de itens de comanda retornada",
)
def list_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    return item_comanda_service.list_items(page, page_size)


@router.get(
    "/count",
    summary="Contar itens de comanda",
    description="""
Request:
- Query param opcional `comanda_id` para filtrar a contagem.

Response:
- Retorna o total de itens de comanda.
""",
    response_description="Total de itens de comanda retornado",
)
def count():
    return {"total": item_comanda_service.count_items()}


@router.get(
    "/{id}",
    response_model=ItemComandaResponse,
    summary="Buscar item de comanda por ID",
    description="""
Request:
- Path param: `id` do item de comanda.

Response:
- Retorna o item de comanda no formato `ItemComandaResponse`.
- Retorna 404 quando o item não existe.
""",
    response_description="Item de comanda encontrado",
)
def get(id: int):
    result = item_comanda_service.get_item(id)
    if not result:
        raise HTTPException(status_code=404, detail="Item de comanda não encontrado")
    return result


@router.put(
    "/{id}",
    response_model=ItemComandaResponse,
    summary="Atualizar item de comanda",
    description="""
Request:
- Path param: `id` do item de comanda.
- Body JSON parcial no formato `UpdateItemComanda`.

Response:
- Retorna o item de comanda atualizado no formato `ItemComandaResponse`.
- Retorna 404 quando o item não existe.
""",
    response_description="Item de comanda atualizado",
)
def update(id: int, item: UpdateItemComanda):
    result = item_comanda_service.update_item(
        id, item.model_dump(exclude_none=True)
    )
    if not result:
        raise HTTPException(status_code=404, detail="Item de comanda não encontrado")
    return result


@router.delete(
    "/{id}",
    status_code=204,
    summary="Remover item de comanda",
    description="""
Request:
- Path param: `id` do item de comanda.

Response:
- Retorna status 204 sem conteúdo quando a remoção é bem-sucedida.
- Retorna 404 quando o item não existe.
""",
    response_description="Item de comanda removido com sucesso",
)
def delete(id: int):
    if not item_comanda_service.delete_item(id):
        raise HTTPException(status_code=404, detail="Item de comanda não encontrado")