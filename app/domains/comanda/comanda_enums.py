from enum import Enum

class StatusComanda(str, Enum):
    ABERTA = "aberta"
    FECHADA = "fechada"
    CANCELADA = "cancelada"
