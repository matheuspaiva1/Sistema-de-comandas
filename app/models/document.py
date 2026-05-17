from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship

class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: int = Field(foreign_key="products.id", index=True)

    original_filename: str
    content_type: str
    extension: str
    size_bytes: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    product: "Product" = Relationship(back_populates="documents")