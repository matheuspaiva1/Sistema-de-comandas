from datetime import datetime
from typing import Optional
from beanie.odm.queries.find import FindMany
from pymongo.errors import OperationFailure

from app.models.command import Command
from app.models.product import Product


class ReportsRepository:
    """Repositório contendo consultas analíticas e agregações complexas para o sistema."""

    async def get_by_id(self, command_id) -> Optional[Command]:
        """Consulta simples por ID (comanda)."""
        return await Command.get(command_id, fetch_links=True)

    async def search_products_text(self, query: str) -> list[Product]:
        """Busca textual utilizando o índice de texto do MongoDB nos produtos."""
        try:
            return await Product.find({"$text": {"$search": query}}).to_list()
        except OperationFailure:
            return await Product.find(
                {
                    "$or": [
                        {"name": {"$regex": query, "$options": "i"}},
                        {"description": {"$regex": query, "$options": "i"}},
                    ]
                }
            ).to_list()

    def get_commands_by_date_range(self, start_date: datetime, end_date: datetime) -> FindMany[Command]:
        """Retorna comandas abertas ou fechadas dentro de um intervalo de datas."""
        return Command.find(
            {
                "$or": [
                    {"opened_at": {"$gte": start_date, "$lte": end_date}},
                    {"closed_at": {"$gte": start_date, "$lte": end_date}},
                ]
            },
            fetch_links=True,
        ).sort("-opened_at")

    def get_commands_summary(
        self,
        sort_by: str = "opened_at",
        order: str = "desc"
    ) -> FindMany[Command]:
        """Retorna uma consulta Beanie (FindMany) de todas as comandas ordenadas por um campo específico."""
        allowed_fields = {"opened_at", "closed_at", "total_amount"}
        if sort_by not in allowed_fields:
            sort_by = "opened_at"

        direction = "-" if order == "desc" else "+"
        sort_expression = f"{direction}{sort_by}"

        return Command.find(fetch_links=True).sort(sort_expression)

    async def count_commands(self) -> int:
        """Retorna a contagem total de comandas."""
        return await Command.count()

    async def get_revenue_by_category(self) -> list[dict]:
        """Aggregation Pipeline que cruza as comandas com os produtos para extrair o faturamento por categoria."""
        pipeline = [
            {"$unwind": "$items"},
            {
                "$lookup": {
                    "from": "products",
                    "localField": "items.product.$id",
                    "foreignField": "_id",
                    "as": "product_data"
                }
            },
            {"$unwind": "$product_data"},
            {
                "$group": {
                    "_id": "$product_data.category",
                    "total_revenue": {"$sum": {"$multiply": ["$items.quantity", "$items.unit_price"]}},
                    "total_quantity": {"$sum": "$items.quantity"},
                    "distinct_products": {"$addToSet": "$product_data.name"}
                }
            },
            {
                "$project": {
                    "category": "$_id",
                    "total_revenue": {"$round": ["$total_revenue", 2]},
                    "total_quantity": 1,
                    "products_count": {"$size": "$distinct_products"},
                    "_id": 0
                }
            },
            {"$sort": {"total_revenue": -1}}
        ]
        return await Command.aggregate(pipeline).to_list()

    async def get_client_consumption_ranking(self) -> list[dict]:
        """Aggregation Pipeline que calcula o gasto total de cada cliente em comandas fechadas."""
        pipeline = [
            {"$match": {"status": "FECHADA"}},
            {
                "$lookup": {
                    "from": "clients",
                    "localField": "client.$id",
                    "foreignField": "_id",
                    "as": "client_info"
                }
            },
            {"$unwind": "$client_info"},
            {
                "$group": {
                    "_id": "$client_info._id",
                    "client_name": {"$first": "$client_info.name"},
                    "client_email": {"$first": "$client_info.email"},
                    "total_spent": {"$sum": "$total_amount"},
                    "commands_count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "client_id": {"$toString": "$_id"},
                    "client_name": 1,
                    "client_email": 1,
                    "total_spent": {"$round": ["$total_spent", 2]},
                    "commands_count": 1,
                    "_id": 0
                }
            },
            {"$sort": {"total_spent": -1}}
        ]
        return await Command.aggregate(pipeline).to_list()

    async def get_table_performance_stats(self) -> list[dict]:
        """Aggregation Pipeline que calcula o faturamento acumulado e ticket médio por mesa física."""
        pipeline = [
            {
                "$lookup": {
                    "from": "tables",
                    "localField": "table.$id",
                    "foreignField": "_id",
                    "as": "table_info"
                }
            },
            {"$unwind": {"path": "$table_info", "preserveNullAndEmptyArrays": True}},
            {
                "$group": {
                    "_id": "$table_info._id",
                    "table_number": {"$first": "$table_info.number"},
                    "table_location": {"$first": "$table_info.location"},
                    "total_billing": {"$sum": "$total_amount"},
                    "commands_count": {"$sum": 1},
                    "avg_billing": {"$avg": "$total_amount"}
                }
            },
            {
                "$project": {
                    "table_id": {
                        "$cond": [
                            {"$eq": ["$_id", None]},
                            None,
                            {"$toString": "$_id"}
                        ]
                    },
                    "table_number": {"$cond": [{"$eq": ["$_id", None]}, 0, "$table_number"]},
                    "table_location": {"$cond": [{"$eq": ["$_id", None]}, "Sem Mesa", "$table_location"]},
                    "total_billing": {"$round": ["$total_billing", 2]},
                    "commands_count": 1,
                    "avg_billing": {"$round": ["$avg_billing", 2]},
                    "_id": 0
                }
            },
            {"$sort": {"total_billing": -1}}
        ]
        return await Command.aggregate(pipeline).to_list()
