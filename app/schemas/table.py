from typing import Optional

from pydantic import BaseModel

from app.models.table import TableStatus
from app.schemas import PyObjectId


class TableCreate(BaseModel):
    number: int
    name: Optional[str] = None
    seats: Optional[int] = None
    location: Optional[str] = None


class TableUpdate(BaseModel):
    number: Optional[int] = None
    name: Optional[str] = None
    seats: Optional[int] = None
    location: Optional[str] = None
    status: Optional[TableStatus] = None


class TableRead(BaseModel):
    id: PyObjectId
    number: int
    name: Optional[str] = None
    seats: Optional[int] = None
    location: Optional[str] = None
    status: TableStatus

    model_config = {"from_attributes": True}
