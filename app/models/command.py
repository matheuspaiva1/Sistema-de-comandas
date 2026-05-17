from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from sqlmodel import Field, Relationship, SQLModel


class CommandStatus(str, Enum):
    ABERTA = "ABERTA"
    FECHADA = "FECHADA"
    CANCELADA = "CANCELADA"


class Command(SQLModel, table=True):
    __tablename__ = "commands"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(default_factory=lambda: uuid4().hex[:10].upper(), index=True)
    client_id: int = Field(foreign_key="clients.id", index=True)
    status: CommandStatus = Field(default=CommandStatus.ABERTA, index=True)
    opened_at: datetime = Field(default_factory=datetime.utcnow)
    closed_at: datetime | None = None
    total_amount: float = Field(default=0.0)
    table_id: int | None = Field(default=None, foreign_key="tables.id", index=True)

    client: "Client" = Relationship(back_populates="commands")
    # orders (pedidos) removed
    table: Optional["Table"] = Relationship(back_populates="commands")
    payments: list["Payment"] = Relationship(back_populates="command")
    items: list["ItemCommand"] = Relationship(back_populates="command")