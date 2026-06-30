from enum import Enum
from typing import Optional

from beanie import Document


class TableStatus(str, Enum):
    LIVRE = "LIVRE"
    OCUPADA = "OCUPADA"


class Table(Document):
    """Representa uma mesa física do estabelecimento."""

    number: int
    name: Optional[str] = None
    seats: Optional[int] = None
    location: Optional[str] = None
    status: TableStatus = TableStatus.LIVRE

    class Settings:
        name = "tables"
        indexes = ["number", "status"]
