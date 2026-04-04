from app.domains.comanda.comanda_repository import ComandaRepository

comanda_repository = ComandaRepository()

def create_commands(data: dict):
    return comanda_repository.insert(data)

def list_commands(page: int, page_size: int):
    return comanda_repository.list(page, page_size)

def search_commands(id: int):
    return comanda_repository.get(id)

def update_commands(id: int, data: dict):
    return comanda_repository.update(id, data)

def delete_commands(id: int) -> bool:
    return comanda_repository.delete(id)

def count_commands():
    return comanda_repository.count()
