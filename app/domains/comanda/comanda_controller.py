from fastapi import APIRouter, HTTPException
from app.domains.comanda.comanda_schema import (
    CreateCommands,
    UpdateCommands,
)
from app.domains.comanda import comanda_service

router = APIRouter(prefix="/comandas", tags=["Comandas"])

@router.post(
    "",
    summary="Criar comanda",
    description="""
Request:
- Body JSON no formato `CreateCommands`.

Response:
- Retorna a comanda criada com identificador gerado.
""",
    response_description="Comanda criada com sucesso",
)
def create(comanda: CreateCommands):
    return comanda_service.create_commands(comanda.model_dump())

@router.get(
    "",
    summary="Listar comandas",
    description="""
Request:
- Query params: `page` (padrão 1) e `page_size` (padrão 10).

Response:
- Retorna a lista paginada de comandas.
""",
    response_description="Lista de comandas retornada",
)
def list(page: int = 1, page_size: int = 10):
    return comanda_service.list_commands(page, page_size)

@router.get(
    "/count",
    summary="Contar comandas",
    description="""
Request:
- Sem body e sem parâmetros.

Response:
- Retorna o total de comandas cadastradas.
""",
    response_description="Total de comandas retornado",
)
def count():
    return {"total": comanda_service.count_commands()}

@router.get(
    "/{id}",
    summary="Buscar comanda por ID",
    description="""
Request:
- Path param: `id` da comanda.

Response:
- Retorna os dados da comanda.
- Retorna 404 quando a comanda não existe.
""",
    response_description="Comanda encontrada",
)
def search(id: int):
    result = comanda_service.search_commands(id)
    if not result:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")

    return result

@router.put(
    "/{id}",
    summary="Atualizar comanda",
    description="""
Request:
- Path param: `id` da comanda.
- Body JSON parcial no formato `UpdateCommands`.

Response:
- Retorna a comanda atualizada.
- Retorna 404 quando a comanda não existe.
""",
    response_description="Comanda atualizada",
)
def update(id: int, comanda: UpdateCommands):
    result = comanda_service.update_commands(id, comanda.model_dump(exclude_none=True))
    if not result:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")

    return result

@router.delete(
    "/{id}",
    summary="Remover comanda",
    description="""
Request:
- Path param: `id` da comanda.

Response:
- Retorna mensagem de confirmação de remoção.
- Retorna 404 quando a comanda não existe.
""",
    response_description="Comanda removida",
)
def delete(id: int):
    if not comanda_service.delete_commands(id):
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    return {"detail": "Comanda deletada com sucesso"}