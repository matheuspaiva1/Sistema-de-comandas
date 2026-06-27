from io import BytesIO
from uuid import UUID

from beanie import PydanticObjectId
from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import StreamingResponse

from app.schemas.document import DocumentRead
from app.services.document_service import DocumentService

documents_router = APIRouter(prefix="/documents", tags=["Documentos"])
products_documents_router = APIRouter(prefix="/products", tags=["Documentos"])


@documents_router.get("/{document_id}", response_model=DocumentRead)
async def get_document_metadata(document_id: UUID):
    """Retorna os metadados de um documento."""
    document = await DocumentService().get_document(document_id)
    return DocumentRead.model_validate(document, from_attributes=True)


@documents_router.get("/{document_id}/download")
async def download_document(document_id: UUID):
    """Baixa ou exibe o arquivo do documento."""
    data, content_type, original_filename = await DocumentService().download_document(document_id)
    return StreamingResponse(
        content=BytesIO(data),
        media_type=content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{original_filename}"',
            "Content-Length": str(len(data)),
        },
    )


@documents_router.put("/{document_id}", response_model=DocumentRead)
async def replace_document_file(document_id: UUID, file: UploadFile = File(...)):
    """Substitui o arquivo de um documento."""
    document = await DocumentService().replace_document(document_id, file)
    return DocumentRead.model_validate(document, from_attributes=True)


@documents_router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: UUID):
    """Remove um documento e seu arquivo físico."""
    await DocumentService().delete_document(document_id)


@products_documents_router.post(
    "/{product_id}/documents",
    response_model=DocumentRead,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(product_id: PydanticObjectId, file: UploadFile = File(...)):
    """Faz upload de um novo documento para um produto."""
    document = await DocumentService().upload_document(product_id, file)
    return DocumentRead.model_validate(document, from_attributes=True)


@products_documents_router.get("/{product_id}/documents", response_model=list[DocumentRead])
async def list_product_documents(product_id: PydanticObjectId):
    """Lista os documentos de um produto."""
    documents = await DocumentService().list_documents_by_product(product_id)
    return [DocumentRead.model_validate(d, from_attributes=True) for d in documents]
