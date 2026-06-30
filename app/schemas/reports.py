from typing import Optional
from pydantic import BaseModel


class RevenueByCategoryResponse(BaseModel):
    category: str
    total_revenue: float
    total_quantity: int
    products_count: int


class ClientConsumptionResponse(BaseModel):
    client_id: str
    client_name: str
    client_email: Optional[str] = None
    total_spent: float
    commands_count: int


class TablePerformanceResponse(BaseModel):
    table_id: Optional[str] = None
    table_number: int
    table_location: str
    total_billing: float
    commands_count: int
    avg_billing: float


class CommandsCountResponse(BaseModel):
    total_commands: int
