from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Client(SQLModel, table=True):
    """Representa um cliente do estabelecimento."""

    __tablename__ = "clients"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, index=True)
    phone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=255, index=True)
    tax_id: str | None = Field(default=None, max_length=20, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    commands: list["Command"] = Relationship(back_populates="client")