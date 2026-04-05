from enum import Enum

class StatusMesa(Enum):
    LIVRE = "livre"
    OCUPADA = "ocupada"
    RESERVADA = "reservada"
    MANUTENCAO = "manutencao"

class LocalizacaoMesa(Enum):
    INTERNO = "interno"
    EXTERNO = "externo"
    BAR = "bar"
    VARANDA = "varanda"
