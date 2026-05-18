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
from app.models.command import Command, CommandStatus
from app.models.client import Client
from app.models.item_command import ItemCommand
from app.models.payment import Payment
from app.models.table import Table
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
                "category": cat.category,
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


@router.get("/commands/revenue")
async def get_revenue_by_period(
    session: SessionDep,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    """Retorna o faturamento total (soma das comandas fechadas) no período."""
    statement = select(func.sum(Command.total_amount)).where(Command.status == CommandStatus.FECHADA)
    if start_date:
        statement = statement.where(Command.opened_at >= start_date)
    if end_date:
        statement = statement.where(Command.opened_at <= end_date)
        
    result = await session.execute(statement)
    total_revenue = result.scalar() or 0.0
    
    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_revenue": total_revenue
    }


@router.get("/products/best-sellers")
async def get_best_sellers(session: SessionDep, limit: int = Query(10, ge=1, le=100)):
    """Lista os produtos mais vendidos baseados na quantidade total consumida."""
    statement = (
        select(
            Product.id,
            Product.name,
            func.sum(ItemCommand.quantity).label("total_sold"),
            func.sum(ItemCommand.quantity * ItemCommand.unit_price).label("total_revenue")
        )
        .join(ItemCommand, ItemCommand.product_id == Product.id)
        .group_by(Product.id, Product.name)
        .order_by(func.sum(ItemCommand.quantity).desc())
        .limit(limit)
    )
    result = await session.execute(statement)
    best_sellers = result.all()
    
    return [
        {
            "product_id": row.id,
            "name": row.name,
            "total_sold": row.total_sold,
            "total_revenue": float(row.total_revenue)
        }
        for row in best_sellers
    ]


@router.get("/clients/top")
async def get_top_clients(session: SessionDep, limit: int = Query(10, ge=1, le=100)):
    """Retorna os clientes que mais gastaram no restaurante."""
    statement = (
        select(
            Client.id,
            Client.name,
            func.sum(Command.total_amount).label("total_spent"),
            func.count(Command.id).label("total_visits")
        )
        .join(Command, Command.client_id == Client.id)
        .where(Command.status == CommandStatus.FECHADA)
        .group_by(Client.id, Client.name)
        .order_by(func.sum(Command.total_amount).desc())
        .limit(limit)
    )
    result = await session.execute(statement)
    top_clients = result.all()
    
    return [
        {
            "client_id": row.id,
            "name": row.name,
            "total_spent": float(row.total_spent),
            "total_visits": row.total_visits
        }
        for row in top_clients
    ]


@router.get("/payments/methods-stats")
async def get_payment_methods_stats(session: SessionDep):
    """Análise do faturamento agrupado por meio de pagamento."""
    statement = (
        select(
            Payment.method,
            func.count(Payment.id).label("transactions"),
            func.sum(Payment.amount).label("total_revenue")
        )
        .group_by(Payment.method)
        .order_by(func.sum(Payment.amount).desc())
    )
    result = await session.execute(statement)
    methods_data = result.all()
    
    total_overall = sum(row.total_revenue for row in methods_data if row.total_revenue)
    
    return {
        "total_revenue": float(total_overall),
        "by_method": [
            {
                "method": row.method,
                "transactions": row.transactions,
                "total": float(row.total_revenue) if row.total_revenue else 0,
                "percentage": round((float(row.total_revenue) / float(total_overall)) * 100, 2) if total_overall > 0 else 0
            }
            for row in methods_data
        ]
    }


@router.get("/tables/top")
async def get_top_tables(session: SessionDep, limit: int = Query(10, ge=1, le=100)):
    """Ranking das mesas que geraram o maior faturamento histórico."""
    statement = (
        select(
            Table.id,
            Table.name,
            Table.location,
            func.sum(Command.total_amount).label("total_revenue"),
            func.count(Command.id).label("total_commands")
        )
        .join(Command, Command.table_id == Table.id)
        .where(Command.status == CommandStatus.FECHADA)
        .group_by(Table.id, Table.name, Table.location)
        .order_by(func.sum(Command.total_amount).desc())
        .limit(limit)
    )
    result = await session.execute(statement)
    top_tables = result.all()
    
    return [
        {
            "table_id": row.id,
            "name": row.name,
            "location": row.location,
            "total_revenue": float(row.total_revenue) if row.total_revenue else 0,
            "total_commands": row.total_commands
        }
        for row in top_tables
    ]
