from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentRead(BaseModel):
    id: UUID
    product_id: str | None = None
    original_filename: str
    content_type: str
    extension: str
    size_bytes: int
    created_at: datetime

    model_config = {"from_attributes": True}
