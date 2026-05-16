
class BusinessRuleException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class UnauthorizedException(Exception):
    def __init__(self, message: str = "Não autorizado"):
        super().__init__(message)
        self.message = message


class ForbiddenException(Exception):
    def __init__(self, message: str = "Acesso proibido"):
        super().__init__(message)
        self.message = message


class EntityNotFoundException(Exception):
    def __init__(self, entity_name: str, entity_id: int):
        super().__init__(f"{entity_name} com id={entity_id} não encontrado(a).")
        self.entity_name = entity_name
        self.entity_id = entity_id


class ProductNotFoundException(EntityNotFoundException):
    def __init__(self, product_id: int):
        super().__init__("Produto", product_id)


class CantDeleteEntityException(Exception):
    def __init__(self, entity_name: str, entity_id: int, reason: str = None):
        message = f"{entity_name} com id={entity_id} não pode ser deletado(a)."
        if reason:
            message += f" Motivo: {reason}"
        super().__init__(message)
        self.entity_name = entity_name
        self.entity_id = entity_id
        self.reason = reason


class EntityAlreadyExistsException(Exception):
    def __init__(self, entity_name: str, identifier_name: str, identifier_value: str):
        super().__init__(f"{entity_name} com {identifier_name} '{identifier_value}' já existe.")
        self.entity_name = entity_name
        self.identifier_name = identifier_name
        self.identifier_value = identifier_value


class InvalidDataException(Exception):
    def __init__(self, field: str, message: str):
        super().__init__(f"Erro no campo '{field}': {message}")
        self.field = field
        self.message = message
