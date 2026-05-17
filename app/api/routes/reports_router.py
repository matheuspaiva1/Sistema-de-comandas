from datetime import date
from typing import Optional

from fastapi import APIRouter, Query, HTTPException
from fastapi_pagination import Page
from sqlalchemy import func, and_, or_, extract
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.api.deps import SessionDep
from app.models.product import Product, CategoryEnum
from app.models.document import Document
from app.schemas.product import ProductRead
from app.schemas.document import DocumentRead
from fastapi_pagination.ext.sqlmodel import apaginate

router = APIRouter(
    prefix="/analytics",
    tags=["Consultas Analíticas e Relatórios"],
)


@router.get("/products/stats")
async def get_products_statistics(session: SessionDep):
    """Estatísticas gerais de produtos: total, por categoria e faixa de preços."""
    total_result = await session.execute(select(func.count(Product.id)))
    total_count = total_result.scalar()

    category_result = await session.execute(
        select(
            Product.category,
            func.count(Product.id).label("quantity"),
            func.avg(Product.price).label("avg_price"),
            func.min(Product.price).label("min_price"),
            func.max(Product.price).label("max_price"),
        ).group_by(Product.category)
    )
    categories = category_result.all()

    price_result = await session.execute(
        select(
            func.avg(Product.price).label("avg_price"),
            func.min(Product.price).label("min_price"),
            func.max(Product.price).label("max_price"),
        )
    )
    price_stats = price_result.one()

    return {
        "total_products": total_count,
        "average_price_overall": float(price_stats[0]) if price_stats[0] else 0,
        "min_price_overall": float(price_stats[1]) if price_stats[1] else 0,
        "max_price_overall": float(price_stats[2]) if price_stats[2] else 0,
        "by_category": [
            {
                "category": cat.category.value,
                "quantity": cat.quantity,
                "average_price": float(cat.avg_price) if cat.avg_price else 0,
                "min_price": float(cat.min_price) if cat.min_price else 0,
                "max_price": float(cat.max_price) if cat.max_price else 0,
            }
            for cat in categories
        ],
    }


@router.get("/products/most-expensive")
async def get_most_expensive_products(
    session: SessionDep,
    limit: int = Query(10, ge=1, le=100),
):
    """Retorna os produtos mais caros."""
    result = await session.execute(
        select(Product).order_by(Product.price.desc()).limit(limit)
    )
    return [ProductRead.model_validate(p) for p in result.scalars().all()]


@router.get("/products/cheapest")
async def get_cheapest_products(
    session: SessionDep,
    limit: int = Query(10, ge=1, le=100),
):
    """Retorna os produtos mais baratos."""
    result = await session.execute(
        select(Product).order_by(Product.price.asc()).limit(limit)
    )
    return [ProductRead.model_validate(p) for p in result.scalars().all()]


@router.get("/products/filtered", response_model=Page[ProductRead])
async def list_products_advanced_filter(
    session: SessionDep,
    category: Optional[CategoryEnum] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    active: Optional[bool] = Query(None),
    search: Optional[str] = Query(None, max_length=100),
    sort_by: Optional[str] = Query("name", pattern="^(name|price|category)$"),
    order: Optional[str] = Query("asc", pattern="^(asc|desc)$"),
):
    """Listagem com múltiplos filtros e ordenação."""
    filters = []

    if category:
        filters.append(Product.category == category)
    if min_price is not None:
        filters.append(Product.price >= min_price)
    if max_price is not None:
        filters.append(Product.price <= max_price)
    if active is not None:
        filters.append(Product.active == active)
    if search:
        search_term = f"%{search}%"
        filters.append(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
            )
        )

    statement = select(Product)
    if filters:
        statement = statement.where(and_(*filters))

    sort_column = {
        "name": Product.name,
        "price": Product.price,
        "category": Product.category,
    }.get(sort_by, Product.name)

    statement = statement.order_by(
        sort_column.desc() if order == "desc" else sort_column.asc()
    )
    return await apaginate(session, statement)


@router.get("/products/with-documents")
async def list_products_with_documents(session: SessionDep):
    """Lista produtos que possuem documentos associados."""
    statement = (
        select(Product)
        .where(Product.documents.any())
        .options(selectinload(Product.documents))
    )
    result = await session.execute(statement)
    products = result.scalars().unique().all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category.value,
            "price": p.price,
            "documents_count": len(p.documents),
            "documents": [
                {
                    "id": str(d.id),
                    "original_filename": d.original_filename,
                    "content_type": d.content_type,
                    "size_bytes": d.size_bytes,
                    "created_at": d.created_at.isoformat(),
                }
                for d in p.documents
            ],
        }
        for p in products
    ]


@router.get("/products/without-documents", response_model=Page[ProductRead])
async def list_products_without_documents(session: SessionDep):
    """Lista produtos que não possuem documentos associados."""
    statement = select(Product).where(~Product.documents.any())
    return await apaginate(session, statement)


@router.get("/documents/stats")
async def get_documents_statistics(session: SessionDep):
    """Estatísticas sobre os documentos cadastrados."""
    total_result = await session.execute(select(func.count(Document.id)))
    total_docs = total_result.scalar()

    size_result = await session.execute(
        select(
            func.sum(Document.size_bytes).label("total_size"),
            func.avg(Document.size_bytes).label("avg_size"),
            func.max(Document.size_bytes).label("max_size"),
        )
    )
    size_data = size_result.one()

    type_result = await session.execute(
        select(
            Document.content_type,
            func.count(Document.id).label("count"),
        ).group_by(Document.content_type)
    )

    return {
        "total_documents": total_docs,
        "total_size_bytes": size_data[0] or 0,
        "average_size_bytes": float(size_data[1]) if size_data[1] else 0,
        "max_size_bytes": float(size_data[2]) if size_data[2] else 0,
        "by_type": [
            {"content_type": row[0], "quantity": row[1]}
            for row in type_result.all()
        ],
    }


@router.get("/products/{product_id}/documents/stats")
async def get_product_documents_stats(product_id: int, session: SessionDep):
    """Estatísticas dos documentos de um produto específico."""
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    result = await session.execute(
        select(
            func.count(Document.id).label("total"),
            func.sum(Document.size_bytes).label("total_size"),
            func.avg(Document.size_bytes).label("avg_size"),
        ).where(Document.product_id == product_id)
    )
    stats = result.one()

    return {
        "product_id": product_id,
        "product_name": product.name,
        "total_documents": stats[0],
        "total_size_bytes": stats[1] or 0,
        "average_size_bytes": float(stats[2]) if stats[2] else 0,
    }


@router.get("/documents/filtered-by-date", response_model=Page[DocumentRead])
async def list_documents_by_date(
    session: SessionDep,
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None, ge=1, le=12),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    """Lista documentos com filtros por data e ano."""
    statement = select(Document)
    filters = []

    if start_date:
        filters.append(Document.created_at >= start_date)
    if end_date:
        filters.append(Document.created_at <= end_date)
    if year:
        filters.append(extract("year", Document.created_at) == year)
    if month:
        filters.append(extract("month", Document.created_at) == month)

    if filters:
        statement = statement.where(and_(*filters))

    statement = statement.order_by(Document.created_at.desc())
    return await apaginate(session, statement)
