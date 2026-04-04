from app.repository.produto_repository import ProdutoRepository

product_repo = ProdutoRepository()

def create_products(data:dict):
    return product_repo.insert(data)

def list_products(page:int, page_size:int):
    return product_repo.list(page, page_size)

def search_product(id:int):
    return product_repo.get(id)

def update_product(id:int, data:dict):
    return product_repo.update(id, data)

def delete_product(id:int):
    return product_repo.delete(id)

def count_products():
    return product_repo.count()