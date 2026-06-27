from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import PyObjectId


class ClientCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    tax_id: Optional[str] = None


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    tax_id: Optional[str] = None


class ClientRead(BaseModel):
    id: PyObjectId
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    tax_id: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
