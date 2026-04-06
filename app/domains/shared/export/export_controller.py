from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.domains.shared.export.export_service import ExportService
from app.domains.comanda.comanda_repository import ComandaRepository

router = APIRouter(prefix="/export", tags=["Export"])

def get_export_service():
    return ExportService(ComandaRepository())

@router.get(
    "/csv",
    summary="Exportar comandas em CSV",
    description="""
Request:
- Sem body e sem parâmetros.

Response:
- Retorna arquivo CSV em stream para download (`comandas.csv`).
""",
    response_description="Arquivo CSV de comandas gerado",
)
def export_csv(service: ExportService = Depends(get_export_service)):
    return StreamingResponse(
        service.stream_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=comandas.csv"}
    )

@router.get(
    "/zip",
    summary="Exportar comandas em ZIP",
    description="""
Request:
- Sem body e sem parâmetros.

Response:
- Retorna arquivo ZIP em stream para download (`comandas.zip`).
""",
    response_description="Arquivo ZIP de comandas gerado",
)
def export_zip(service: ExportService = Depends(get_export_service)):
    return StreamingResponse(
        service.stream_zip(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=comandas.zip"}
    )