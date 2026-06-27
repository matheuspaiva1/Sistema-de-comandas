from datetime import datetime
from enum import Enum
from typing import Optional

from beanie import Document, Link

from app.models.client import Client
from app.models.item_command import ItemCommand
from app.models.table import Table


class CommandStatus(str, Enum):
    ABERTA = "ABERTA"
    FECHADA = "FECHADA"
    CANCELADA = "CANCELADA"


class Command(Document):
    """Representa uma comanda aberta por um cliente, podendo estar vinculada a uma mesa."""

    client: Link[Client]
    table: Optional[Link[Table]] = None

    items: list[ItemCommand] = []

    status: CommandStatus = CommandStatus.ABERTA
    total_amount: float = 0.0
    opened_at: datetime = datetime.utcnow()
    closed_at: Optional[datetime] = None

    class Settings:
        name = "commands"
        indexes = ["status", "opened_at"]
