from app.repository.comanda_repository import CommandsRepository

def create_commands(data: dict):
    return CommandsRepository.insert(data)

def list_commands(page:int, page_size:int):
    return CommandsRepository.list(page, page_size)

def search_commands(id: int):
    return CommandsRepository.get(id)

def update_commands(id: int, data: dict):
    return CommandsRepository.update(id, data)

def delete_commands(id: int) -> bool:
    return CommandsRepository.delete(id)

def count_commands():
    return CommandsRepository.count()

