from fastapi import APIRouter, HTTPException
from app.domains.produto.produto_schema import CreateProduct, UpdateProduct
from app.domains.produto.produto_service import produto_service

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("")
def create(product: CreateProduct):
    return produto_service.create_products(product.model_dump())

@router.get("")
def list(page: int = 1, page_size: int = 10):
    return produto_service.list_products(page, page_size)

@router.get("/{id}")
def search(id: int):
    result = produto_service.search_product(id)
    if not result:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return result

@router.put("/{id}")
def update(id:int, product: UpdateProduct):
    result = produto_service.update_product(id, product.model_dump(exclude_none=True))
    if not result:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return result

@router.delete("/{id}")
def delete(id: int):
    produto_service.delete_product(id)
    return {"detail": "Produto removido com sucesso"}

@router.get("/count")
def count():
    return {"Total: ": produto_service.count_products()}