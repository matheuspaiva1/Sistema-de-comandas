from fastapi import APIRouter

from app.domains.mesa.mesa_models import Mesa
from app.domains.mesa.mesa_shemas import CreateMesaSchema
from app.domains.mesa import mesa_service

router = APIRouter(prefix="/mesas", tags=["Mesa"])

@router.post("/")
def create_mesa(
    schema: CreateMesaSchema
) -> Mesa:
    result = mesa_service.create_mesa(schema)
    return result

@router.get("/")
def get_mesas(page: int, page_size: int):
    result = mesa_service.get_mesas(page, page_size)
    return result

@router.get("/{id}")
def get_mesa(id: int):
    result = mesa_service.get_mesa(id)
    return result

@router.put("/{id}")
def update_mesa(id: int, schema: CreateMesaSchema):
    result = mesa_service.update_mesa(id, schema)
    return result

@router.delete("/{id}")
def delete_mesa(id: int):
    result = mesa_service.delete_mesa(id)
    return result