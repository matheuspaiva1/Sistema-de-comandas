from datetime import datetime

from sqlmodel import SQLModel


class ClientCreate(SQLModel):
    name: str
    phone: str | None = None
    email: str | None = None
    tax_id: str | None = None


class ClientUpdate(SQLModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    tax_id: str | None = None


class ClientRead(SQLModel):
    id: int
    name: str
    phone: str | None = None
    email: str | None = None
    tax_id: str | None = None
    created_at: datetime