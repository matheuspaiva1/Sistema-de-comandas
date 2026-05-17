from datetime import datetime

from sqlmodel import SQLModel


class ClientCreate(SQLModel):
    nome: str
    telefone: str | None = None
    email: str | None = None


class ClientUpdate(SQLModel):
    nome: str | None = None
    telefone: str | None = None
    email: str | None = None


class ClientRead(SQLModel):
    id: int
    nome: str
    telefone: str | None = None
    email: str | None = None
    created_at: datetime