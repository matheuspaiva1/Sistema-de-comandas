from pydantic import BaseModel

class CreateComanda (BaseModel):
    clientId: int
    tableId: int

class UpdateComanda (BaseModel):
    status: str | None = None
    fullValue: float | None = None

class Comanda(BaseModel):
    id: int
    clientId: int
    tableId: int
    status: str
    fullValue: float

    class Config:
        fromAttributes = True

    