from app.domains.item_comanda.item_comanda_schema import ItemComandaResponse
from app.domains.comanda.comanda_enums import StatusComanda
from datetime import datetime
from pydantic import BaseModel

class CreateComandaSchema (BaseModel):
    itens: list[int]
    cliente_id: int
    mesa_id: int

class UpdateComandaSchema (BaseModel):
    data_abertura: datetime | None = None
    data_fechamento: datetime | None = None
    cliente_id: int | None = None
    mesa_id: int | None = None
    status: StatusComanda | None = None
    valor_total: float | None = None

class ComandaSchema(BaseModel):
    id: int
    numero: int
    data_abertura: datetime
    data_fechamento: datetime | None = None
    cliente_id: int
    mesa_id: int
    itens: list[ItemComandaResponse]
    status: StatusComanda
    valor_total: float

    class Config:
        fromAttributes = True
