from app.repository.comanda_repository import ComandaRepository

def create_comanda(data: dict):
    return ComandaRepository.insert(data)

def list_comandas(page:int, page_size:int):
    return ComandaRepository.list(page, page_size)

def search_comanda(id: int):
    return ComandaRepository.get(id)

def update_comanda(id: int, data: dict):
    return ComandaRepository.update(id, data)

def delete_comanda(id: int):
    return ComandaRepository.delete(id)

def count_comandas():
    return ComandaRepository.count()

