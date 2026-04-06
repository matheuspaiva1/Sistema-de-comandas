from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CreateItemComanda(BaseModel):
    comanda_id: int = Field(..., ge=1)
    produto_id: int = Field(..., ge=1)
    quantidade: int = Field(..., ge=1)
    valor_unitario: Decimal = Field(..., gt=0)


class UpdateItemComanda(BaseModel):
    produto_id: int | None = Field(default=None, ge=1)
    quantidade: int | None = Field(default=None, ge=1)
    valor_unitario: Decimal | None = Field(default=None, gt=0)


class ItemComandaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    comanda_id: int
    produto_id: int
    quantidade: int
    valor_unitario: Decimal
    valor_total: Decimal
