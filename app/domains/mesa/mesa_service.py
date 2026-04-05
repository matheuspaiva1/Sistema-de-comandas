from fastapi import HTTPException
from app.domains.mesa.mesa_shemas import CreateMesaSchema
from app.domains.mesa.mesa_models import Mesa
from app.domains.mesa.mesa_repository import MesaRepository
from app.domains.mesa.mesa_enums import StatusMesa, LocalizacaoMesa

mesa_repository = MesaRepository()

def _to_model(data: dict) -> Mesa:
    return Mesa(
        id=data["id"],
        numero=data["numero"],
        capacidade=data["capacidade"],
        status=StatusMesa(data["status"]),
        localizacao=LocalizacaoMesa(data["localizacao"])
    )

def create_mesa(schema: CreateMesaSchema) -> Mesa:
    data = schema.model_dump(mode='json')
    
    if data["capacidade"] <= 0:
        raise HTTPException(status_code=400, detail="A capacidade da mesa deve ser maior que zero")
        
    result_data = mesa_repository.insert(data)
    return _to_model(result_data)

def get_mesas(page: int, page_size: int) -> list[Mesa]:
    results = mesa_repository.list(page, page_size)
    return [_to_model(data) for data in results]

def get_mesa(id: int) -> Mesa:
    data = mesa_repository.get(id)
    if not data:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    return _to_model(data)

def update_mesa(id: int, schema: CreateMesaSchema) -> Mesa:
    data = schema.model_dump(mode='json', exclude_unset=True)
    
    if data.get("capacidade") is not None and data["capacidade"] <= 0:
        raise HTTPException(status_code=400, detail="A capacidade da mesa deve ser maior que zero")
        
    updated_data = mesa_repository.update(id, data)
    if not updated_data:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    
    return _to_model(updated_data)

def delete_mesa(id: int) -> dict:
    success = mesa_repository.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    return {"detail": "Mesa deletada com sucesso"}
