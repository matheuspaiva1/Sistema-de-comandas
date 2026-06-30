from datetime import datetime
from typing import Literal
from typing import Optional
from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany
from fastapi import HTTPException

from app.models.command import Command
from app.models.product import Product
from app.repositories.reports_repository import ReportsRepository


class ReportsService:
    """Serviço que implementa as regras de negócio para a extração de relatórios e consultas analíticas."""

    def __init__(self) -> None:
        self.repository = ReportsRepository()

    async def get_command_by_id(self, command_id: PydanticObjectId) -> Optional[Command]:
        """Consulta simples de comanda por ID, carregando os relacionamentos."""
        return await self.repository.get_by_id(command_id)

    async def search_products(self, query: str) -> list[Product]:
        """Realiza busca textual de produtos por nome e descrição."""
        if not query or not query.strip():
            return []
        return await self.repository.search_products_text(query)

    def get_commands_in_date_range(self, start_date: datetime, end_date: datetime) -> FindMany[Command]:
        """Retorna uma consulta Beanie (FindMany) de comandas filtradas por intervalo de data."""
        if start_date > end_date:
            raise HTTPException(status_code=400, detail="start_date deve ser menor ou igual a end_date")
        return self.repository.get_commands_by_date_range(start_date, end_date)

    def get_commands_summary(
        self,
        sort_by: Literal["opened_at", "closed_at", "total_amount"],
        order: Literal["asc", "desc"],
    ) -> FindMany[Command]:
        """Retorna uma consulta Beanie (FindMany) de comandas ordenadas."""
        return self.repository.get_commands_summary(sort_by, order)

    async def count_total_commands(self) -> int:
        """Contagem total de comandas."""
        return await self.repository.count_commands()

    async def get_revenue_by_category_report(self) -> list[dict]:
        """Gera o faturamento total e quantidade de itens vendidos por categoria de produto."""
        return await self.repository.get_revenue_by_category()

    async def get_client_consumption_ranking_report(self) -> list[dict]:
        """Gera o ranking de consumo total por cliente em comandas fechadas."""
        return await self.repository.get_client_consumption_ranking()

    async def get_table_performance_report(self) -> list[dict]:
        """Gera estatísticas de faturamento e ticket médio por mesa."""
        return await self.repository.get_table_performance_stats()
