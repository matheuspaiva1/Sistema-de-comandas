from pydantic import BaseModel

class CreateCommands (BaseModel):
    clientId: int
    tableId: int

class UpdateCommands (BaseModel):
    status: str | None = None
    fullValue: float | None = None

class Commands(BaseModel):
    id: int
    clientId: int
    tableId: int
    status: str
    fullValue: float

    class Config:
        fromAttributes = True

    