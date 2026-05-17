from datetime import datetime

from pydantic import Field
from sqlmodel import SQLModel

from app.models.command import CommandStatus
from app.schemas.client import ClientRead
from app.schemas.order import OrderRead


class CommandCreate(SQLModel):
    client_id: int


class CommandUpdate(SQLModel):
    client_id: int | None = None
    status: CommandStatus | None = None
    closed_at: datetime | None = None
    total_amount: float | None = None


class CommandRead(SQLModel):
    id: int
    code: str
    client_id: int
    status: CommandStatus
    opened_at: datetime
    closed_at: datetime | None = None
    total_amount: float
    client: ClientRead | None = None
    orders: list[OrderRead] = Field(default_factory=list)