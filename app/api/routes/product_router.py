from typing import Sequence

from fastapi import APIRouter, status
from fastapi_pagination import Page

from app.api.deps import SessionDep
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Produtos"]
)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate, session: SessionDep) -> Product:
    service = ProductService(session)
    return await service.create_product(data)


@router.get("/", response_model=Page[ProductRead])
async def list_products(session: SessionDep):
    service = ProductService(session)
    return await service.list_products()


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, session: SessionDep) -> Product:
    service = ProductService(session)
    return await service.get_product(product_id)


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int, data: ProductUpdate, session: SessionDep
) -> Product:
    service = ProductService(session)
    return await service.update_product(product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, session: SessionDep) -> None:
    service = ProductService(session)
    await service.delete_product(product_id)
