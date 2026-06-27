from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.command import CommandStatus
from app.schemas import PyObjectId
from app.schemas.client import ClientRead
from app.schemas.table import TableRead
from app.schemas.item_command import ItemCommandRead


class CommandCreate(BaseModel):
    client_id: PyObjectId
    table_id: Optional[PyObjectId] = None


class CommandUpdate(BaseModel):
    status: Optional[CommandStatus] = None
    closed_at: Optional[datetime] = None
    total_amount: Optional[float] = None


class CommandRead(BaseModel):
    id: PyObjectId
    status: CommandStatus
    opened_at: datetime
    closed_at: Optional[datetime] = None
    total_amount: float
    items: list[ItemCommandRead] = []
    client: Optional[ClientRead] = None
    table: Optional[TableRead] = None

    model_config = {"from_attributes": True}
