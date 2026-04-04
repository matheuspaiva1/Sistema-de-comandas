from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.domains.shared.export.export_service import ExportService
from app.domains.comanda.comanda_repository import ComandaRepository

router = APIRouter(prefix="/export", tags=["Export"])

def get_export_service():
    return ExportService(ComandaRepository())

@router.get("/csv")
def export_csv(service: ExportService = Depends(get_export_service)):
    return StreamingResponse(
        service.stream_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=comandas.csv"}
    )

@router.get("/zip")
def export_zip(service: ExportService = Depends(get_export_service)):
    return StreamingResponse(
        service.stream_zip(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=comandas.zip"}
    )