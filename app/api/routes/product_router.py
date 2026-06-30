from beanie import PydanticObjectId
from fastapi import APIRouter, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate

from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Produtos"])


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate):
    """Cria um novo produto no cardápio."""
    return await ProductService().create_product(data)


@router.get("/", response_model=Page[ProductRead])
async def list_products(search: str | None = Query(default=None)):
    """Lista produtos com filtro opcional por nome."""
    return await paginate(ProductService().list_products(search=search))


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: PydanticObjectId):
    """Retorna um produto pelo ID."""
    return await ProductService().get_product(product_id)


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(product_id: PydanticObjectId, data: ProductUpdate):
    """Atualiza os dados de um produto."""
    return await ProductService().update_product(product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: PydanticObjectId):
    """Remove um produto pelo ID."""
    await ProductService().delete_product(product_id)
