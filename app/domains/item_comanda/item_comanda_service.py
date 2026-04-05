from decimal import Decimal

from app.core.exceptions import NotFoundError, BadRequestError
from app.domains.comanda.comanda_repository import ComandaRepository
from app.domains.item_comanda.item_comanda_repository import ItemComandaRepository
from app.domains.produto import produto_service

_comanda_repo = ComandaRepository()
_item_repo = ItemComandaRepository()


def _para_decimal(valor) -> Decimal:
    try:
        if isinstance(valor, Decimal):
            return valor
        return Decimal(str(valor))
    except Exception:
        raise BadRequestError("valor_unitario inválido")


def create_item(data: dict) -> dict:
    if not _comanda_repo.get(int(data["comanda_id"])):
        raise NotFoundError("Comanda não encontrada")

    if not produto_service.search_product(int(data["produto_id"])):
        raise NotFoundError("Produto não encontrado")

    quantidade = int(data["quantidade"])
    valor_unitario = _para_decimal(data["valor_unitario"])

    payload = data.copy()

    payload["quantidade"] = quantidade
    payload["valor_unitario"] = valor_unitario
    payload["valor_total"] = Decimal(quantidade) * valor_unitario

    return _item_repo.insert(payload)


def list_items(page: int, page_size: int, comanda_id: int | None = None) -> list[dict]:
    return _item_repo.list(page, page_size, comanda_id=comanda_id)


def get_item(record_id: int) -> dict | None:
    return _item_repo.get(record_id)


def update_item(record_id: int, data: dict) -> dict | None:
    existing = _item_repo.get(record_id)
    if not existing:
        return None

    payload = data.copy()

    if payload.get("produto_id") is not None:
        if not produto_service.search_product(int(payload["produto_id"])):
            raise NotFoundError("Produto não encontrado")

    if "quantidade" in payload:
        quantidade = int(payload["quantidade"])
    else:
        quantidade = int(existing["quantidade"])

    if "valor_unitario" in payload:
        valor_unitario = _para_decimal(payload["valor_unitario"])
    else:
        valor_unitario = _para_decimal(existing["valor_unitario"])

    payload["quantidade"] = quantidade
    payload["valor_unitario"] = valor_unitario
    payload["valor_total"] = Decimal(quantidade) * valor_unitario

    return _item_repo.update(record_id, payload)


def delete_item(record_id: int) -> bool:
    return _item_repo.delete(record_id)


def count_items(comanda_id: int | None = None) -> int:
    return _item_repo.count(comanda_id=comanda_id)