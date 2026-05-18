
class BusinessRuleException(Exception):
    """Exceção genérica para violações de regras de negócio."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class UnauthorizedException(Exception):
    """Exceção para acesso não autenticado (HTTP 401)."""

    def __init__(self, message: str = "Não autorizado"):
        super().__init__(message)
        self.message = message


class ForbiddenException(Exception):
    """Exceção para acesso proibido a um recurso (HTTP 403)."""

    def __init__(self, message: str = "Acesso proibido"):
        super().__init__(message)
        self.message = message


class EntityNotFoundException(Exception):
    """Exceção lançada quando uma entidade não é encontrada pelo ID (HTTP 404)."""

    def __init__(self, entity_name: str, entity_id: int):
        super().__init__(f"{entity_name} com id={entity_id} não encontrado(a).")
        self.entity_name = entity_name
        self.entity_id = entity_id


class ProductNotFoundException(EntityNotFoundException):
    """Especialização de EntityNotFoundException para a entidade Produto."""

    def __init__(self, product_id: int):
        super().__init__("Produto", product_id)


class CantDeleteEntityException(Exception):
    """Exceção lançada quando uma entidade não pode ser removida por regra de negócio."""

    def __init__(self, entity_name: str, entity_id: int, reason: str = None):
        message = f"{entity_name} com id={entity_id} não pode ser deletado(a)."
        if reason:
            message += f" Motivo: {reason}"
        super().__init__(message)
        self.entity_name = entity_name
        self.entity_id = entity_id
        self.reason = reason


class EntityAlreadyExistsException(Exception):
    """Exceção lançada quando se tenta criar uma entidade com identificador já existente."""

    def __init__(self, entity_name: str, identifier_name: str, identifier_value: str):
        super().__init__(f"{entity_name} com {identifier_name} '{identifier_value}' já existe.")
        self.entity_name = entity_name
        self.identifier_name = identifier_name
        self.identifier_value = identifier_value


class InvalidDataException(Exception):
    """Exceção lançada quando um campo recebe um valor inválido."""

    def __init__(self, field: str, message: str):
        super().__init__(f"Erro no campo '{field}': {message}")
        self.field = field
        self.message = message


class DocumentNotFoundException(Exception):
    """Exceção lançada quando um documento não é encontrado pelo UUID (HTTP 404)."""

    def __init__(self, document_id):
        super().__init__(f"Documento com id={document_id} não encontrado(a).")
        self.document_id = document_id


class InvalidFileException(Exception):
    """Exceção lançada quando o arquivo enviado é inválido (extensão, tamanho ou conteúdo)."""

    def __init__(self, message: str):
        super().__init__(f"Erro no arquivo: {message}")
        self.message = message
