from app.domains.mesa.mesa_enums import LocalizacaoMesa
from app.domains.mesa.mesa_enums import StatusMesa
from dataclasses import dataclass

@dataclass
class Mesa:
    id: int
    numero: int
    capacidade: int
    status: StatusMesa
    localizacao: LocalizacaoMesa
