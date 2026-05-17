from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class TableStatus(str, Enum):
    LIVRE = "LIVRE"
    OCUPADA = "OCUPADA"


class Table(SQLModel, table=True):
    __tablename__ = "tables"

    id: Optional[int] = Field(default=None, primary_key=True)
    number: int = Field(index=True)
    name: str | None = None
    seats: int | None = None
    location: str | None = None
    status: TableStatus = Field(default=TableStatus.LIVRE, index=True)

    commands: list["Command"] = Relationship(back_populates="table")
