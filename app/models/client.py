from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import Field


class Client(Document):
    """Representa um cliente do estabelecimento."""

    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    tax_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "clients"
        indexes = ["name", "email", "tax_id"]
