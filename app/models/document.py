from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from beanie import Document, Link
from pydantic import Field

from app.models.product import Product


class FileDocument(Document):
    """Metadados de um arquivo físico (imagem ou PDF) associado a um produto."""

    id: UUID = Field(default_factory=uuid4)
    product: Link[Product]

    original_filename: str
    content_type: str
    extension: str
    size_bytes: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def product_id(self) -> str:
        """Retorna o ID do produto como string para serialização no schema DocumentRead."""
        if isinstance(self.product, Product):
            return str(self.product.id)
        return str(self.product.ref.id)
    
    class Settings:
        name = "documents"
