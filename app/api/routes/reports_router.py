from datetime import datetime
from typing import Literal

from beanie import PydanticObjectId
from fastapi import APIRouter, Query, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate

from app.schemas.command import CommandRead
from app.schemas.product import ProductRead
from app.schemas.reports import (
    RevenueByCategoryResponse,
    ClientConsumptionResponse,
    TablePerformanceResponse,
    CommandsCountResponse,
)
from app.services.reports_service import ReportsService

router = APIRouter(
    prefix="/analytics",
    tags=["Consultas Analíticas e Relatórios"],
)


@router.get("/commands/by-date-range", response_model=Page[CommandRead])
async def get_commands_by_date_range(
    start_date: datetime = Query(..., description="Data e hora inicial (ISO format)"),
    end_date: datetime = Query(..., description="Data e hora final (ISO format)"),
):
    """Busca comandas que foram abertas dentro de um intervalo de datas com paginação."""
    return await paginate(ReportsService().get_commands_in_date_range(start_date, end_date))


@router.get("/products/search", response_model=list[ProductRead])
async def search_products(
    q: str = Query(
        ...,
        min_length=2,
        description="Termo de pesquisa para nome ou descrição do produto",
    ),
):
    """Realiza busca textual (MongoDB Full-Text Search) no nome e descrição do produto."""
    return await ReportsService().search_products(q)


@router.get("/commands/summary", response_model=Page[CommandRead])
async def get_commands_summary(
    sort_by: Literal["opened_at", "closed_at", "total_amount"] = Query(
        default="opened_at",
        description="Campo de ordenação: 'opened_at', 'closed_at', 'total_amount'",
    ),
    order: Literal["asc", "desc"] = Query(
        default="desc",
        description="Direção da ordenação: 'asc' ou 'desc'",
    ),
):
    """Lista todas as comandas de forma paginada e ordenada de acordo com os parâmetros passados."""
    return await paginate(ReportsService().get_commands_summary(sort_by, order))


@router.get("/commands/count", response_model=CommandsCountResponse)
async def get_commands_count():
    """Retorna o número total de comandas no sistema."""
    count = await ReportsService().count_total_commands()
    return CommandsCountResponse(total_commands=count)


@router.get("/commands/{command_id}", response_model=CommandRead)
async def get_command_by_id(command_id: PydanticObjectId):
    """Consulta simples de uma comanda por ID (resolvendo os Links de Cliente e Mesa)."""
    command = await ReportsService().get_command_by_id(command_id)
    if not command:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    return command


@router.get("/revenue-by-category", response_model=list[RevenueByCategoryResponse])
async def get_revenue_by_category():
    """Gera um relatório de faturamento bruto e volume de vendas acumulado por categoria de produto."""
    return await ReportsService().get_revenue_by_category_report()


@router.get("/client-ranking", response_model=list[ClientConsumptionResponse])
async def get_client_ranking():
    """Gera um ranking dos clientes que mais consumiram no estabelecimento (apenas comandas FECHADAS)."""
    return await ReportsService().get_client_consumption_ranking_report()


@router.get("/table-stats", response_model=list[TablePerformanceResponse])
async def get_table_stats():
    """Gera estatísticas consolidadas de faturamento e ticket médio por mesa do estabelecimento."""
    return await ReportsService().get_table_performance_report()
