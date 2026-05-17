from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel

class DocumentRead(SQLModel):
    id: UUID
    product_id: int
    original_filename: str
    content_type: str
    extension: str
    size_bytes: int
    created_at: datetime
