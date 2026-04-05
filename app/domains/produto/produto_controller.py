from fastapi import APIRouter, HTTPException
from app.domains.produto.produto_schema import CreateProduct, UpdateProduct
from app.domains.produto import produto_service

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post(
    "",
    summary="Criar produto",
    description="""
Request:
- Body JSON no formato `CreateProduct`.

Response:
- Retorna o produto criado com identificador gerado.
""",
    response_description="Produto criado com sucesso",
)
def create(product: CreateProduct):
    return produto_service.create_products(product.model_dump())

@router.get(
    "",
    summary="Listar produtos",
    description="""
Request:
- Query params: `page` (padrão 1) e `page_size` (padrão 10).

Response:
- Retorna a lista paginada de produtos.
""",
    response_description="Lista de produtos retornada",
)
def list(page: int = 1, page_size: int = 10):
    return produto_service.list_products(page, page_size)

@router.get(
    "/{id}",
    summary="Buscar produto por ID",
    description="""
Request:
- Path param: `id` do produto.

Response:
- Retorna os dados do produto.
- Retorna 404 quando o produto não existe.
""",
    response_description="Produto encontrado",
)
def search(id: int):
    result = produto_service.search_product(id)
    if not result:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return result

@router.put(
    "/{id}",
    summary="Atualizar produto",
    description="""
Request:
- Path param: `id` do produto.
- Body JSON parcial no formato `UpdateProduct`.

Response:
- Retorna o produto atualizado.
- Retorna 404 quando o produto não existe.
""",
    response_description="Produto atualizado",
)
def update(id:int, product: UpdateProduct):
    result = produto_service.update_product(id, product.model_dump(exclude_none=True))
    if not result:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return result

@router.delete(
    "/{id}",
    summary="Remover produto",
    description="""
Request:
- Path param: `id` do produto.

Response:
- Retorna mensagem de confirmação de remoção.
""",
    response_description="Produto removido",
)
def delete(id: int):
    produto_service.delete_product(id)
    return {"detail": "Produto removido com sucesso"}

@router.get(
    "/count",
    summary="Contar produtos",
    description="""
Request:
- Sem body e sem parâmetros.

Response:
- Retorna o total de produtos cadastrados.
""",
    response_description="Total de produtos retornado",
)
def count():
    return {"Total: ": produto_service.count_products()}