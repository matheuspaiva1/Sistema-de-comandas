class ItemComandaRepository:
    """
    Placeholder — to be implemented.
    """

    def insert(self, data: dict) -> dict:
        raise NotImplementedError

    def get(self, record_id: int) -> dict | None:
        raise NotImplementedError

    def list(self, page: int, page_size: int, comanda_id: int | None = None) -> list[dict]:
        raise NotImplementedError

    def update(self, record_id: int, data: dict) -> dict | None:
        raise NotImplementedError

    def delete(self, record_id: int) -> bool:
        raise NotImplementedError

    def count(self, comanda_id: int | None = None) -> int:
        raise NotImplementedError

    def vacuum(self, retention_hours: int = 168) -> None:
        raise NotImplementedError

    def iter_batches(self):
        raise NotImplementedError
