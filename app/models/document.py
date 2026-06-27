from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from beanie import Document, Link

from app.models.product import Product


class FileDocument(Document):
    """Metadados de um arquivo físico (imagem ou PDF) associado a um produto."""

    id: UUID = uuid4()
    product: Link[Product]

    original_filename: str
    content_type: str
    extension: str
    size_bytes: int
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "documents"
