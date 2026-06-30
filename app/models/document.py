from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field


class FileDocument(Document):
    """Metadados de um arquivo físico (imagem ou PDF) associado a um produto."""

    id: UUID = Field(default_factory=uuid4)

    original_filename: str
    content_type: str
    extension: str
    size_bytes: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "documents"
