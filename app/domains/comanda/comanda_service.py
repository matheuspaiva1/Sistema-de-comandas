from app.domains.item_comanda.item_comanda_schema import ItemComandaResponse
from datetime import datetime
from app.domains.comanda.comanda_repository import ComandaRepository
from app.domains.comanda.comanda_schema import CreateComandaSchema
from app.domains.comanda.comanda_enums import StatusComanda
from app.domains.item_comanda import item_comanda_service
from app.domains.produto import produto_service
from app.core.exceptions import NotFoundError

comanda_repository = ComandaRepository()

def create_commands(schema: CreateComandaSchema):
    data = {
        "numero": comanda_repository.count() + 1,
        "data_abertura": datetime.now(),
        "data_fechamento": None,
        "cliente_id": schema.cliente_id,
        "mesa_id": schema.mesa_id,
        "status": StatusComanda.ABERTA.value,
        "valor_total": 0.0
    }
    
    comanda = comanda_repository.insert(data)
    comanda_id = comanda["id"]
    
    total_acumulado = 0.0
    itens_criados = []
    
    for produto_id in schema.itens:
        produto = produto_service.search_product(produto_id)
        if not produto:
            continue
            
        item_payload = {
            "comanda_id": comanda_id,
            "produto_id": produto_id,
            "quantidade": 1,
            "valor_unitario": produto["price"]
        }
        
        item_criado = item_comanda_service.create_item(item_payload)
        itens_criados.append(item_criado)
        total_acumulado += float(item_criado["valor_total"])
        
    # Atualiza o valor_total da comanda no banco para persistência
    if total_acumulado > 0:
        updated_comanda = comanda_repository.update(comanda_id, {"valor_total": total_acumulado})
        if updated_comanda:
            comanda = updated_comanda
        
    # Adiciona os itens criados ao objeto de retorno
    comanda["itens"] = itens_criados
    return comanda

def list_commands(page: int, page_size: int):
    comandas = comanda_repository.list(page, page_size)
    
    for comanda in comandas:
        todos_itens = item_comanda_service.list_items(1, 1000) # Busca generosa
        comanda["itens"] = [i for i in todos_itens if i["comanda_id"] == comanda["id"]]
        
    return comandas

def search_commands(id: int):
    comanda = comanda_repository.get(id)
    if not comanda:
        raise NotFoundError("Comanda não encontrada")
    
    # Busca itens associados
    todos_itens = item_comanda_service.list_items(1, 1000)
    comanda["itens"] = [i for i in todos_itens if i["comanda_id"] == id]
    
    return comanda

def update_commands(id: int, data: dict):
    if data.get("status") == StatusComanda.FECHADA.value:
        data["data_fechamento"] = datetime.now()
        
    result = comanda_repository.update(id, data)
    if not result:
        raise NotFoundError("Comanda não encontrada")
    
    # Retorna com itens carregados
    return search_commands(id)

def delete_commands(id: int) -> bool:
    return comanda_repository.delete(id)

def count_commands():
    return comanda_repository.count()
