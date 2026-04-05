from pydantic import BaseModel
from app.domains.mesa.mesa_enums import StatusMesa
from app.domains.mesa.mesa_enums import LocalizacaoMesa

class CreateMesaSchema(BaseModel):
    numero: int
    capacidade: int
    status: StatusMesa
    localizacao: LocalizacaoMesa

class UpdateMesaSchema(BaseModel):
    numero: int
    capacidade: int
    status: StatusMesa
    localizacao: LocalizacaoMesa

class MesaSchema(BaseModel):
    id: int
    numero: int
    capacidade: int
    status: StatusMesa
    localizacao: LocalizacaoMesa
