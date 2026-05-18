from sqlmodel import SQLModel

from app.models.table import TableStatus


class TableCreate(SQLModel):
    number: int
    name: str | None = None
    seats: int | None = None
    location: str | None = None


class TableUpdate(SQLModel):
    number: int | None = None
    name: str | None = None
    seats: int | None = None
    status: TableStatus | None = None
    location: str | None = None


class TableRead(SQLModel):
    id: int
    number: int
    name: str | None = None
    seats: int | None = None
    location: str | None = None
    status: TableStatus
