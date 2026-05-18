from uuid import UUID

from fastapi import APIRouter, status, File, UploadFile
from fastapi.responses import FileResponse
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import apaginate

from app.api.deps import SessionDep
from app.schemas.document import DocumentRead
from app.services.document_service import DocumentService

documents_router = APIRouter(prefix="/documents", tags=["Documentos"])
products_documents_router = APIRouter(prefix="/products", tags=["Documentos"])


@documents_router.get("/{document_id}", response_model=DocumentRead)
async def get_document_metadata(document_id: UUID, session: SessionDep) -> DocumentRead:
    """Recupera metadados de um documento."""
    service = DocumentService(session)
    document = await service.get_document(document_id)
    return DocumentRead.model_validate(document)


@documents_router.get("/{document_id}/download")
async def download_document(document_id: UUID, session: SessionDep):
    """Baixa ou exibe o arquivo do documento."""
    service = DocumentService(session)
    file_path, content_type, original_filename = await service.download_document(document_id)
    return FileResponse(
        path=file_path,
        media_type=content_type,
        filename=original_filename,
    )


@documents_router.put("/{document_id}", response_model=DocumentRead)
async def replace_document_file(
    document_id: UUID,
    session: SessionDep,
    file: UploadFile = File(...),
) -> DocumentRead:
    """Substitui o arquivo de um documento."""
    service = DocumentService(session)
    document = await service.replace_document(document_id, file)
    return DocumentRead.model_validate(document)


@documents_router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: UUID, session: SessionDep) -> None:
    """Deleta um documento e seu arquivo."""
    service = DocumentService(session)
    await service.delete_document(document_id)


@products_documents_router.post(
    "/{product_id}/documents",
    response_model=DocumentRead,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    product_id: int,
    session: SessionDep,
    file: UploadFile = File(...),
) -> DocumentRead:
    """Faz upload de um novo documento para um produto."""
    service = DocumentService(session)
    document = await service.upload_document(product_id, file)
    return DocumentRead.model_validate(document)


@products_documents_router.get(
    "/{product_id}/documents",
    response_model=Page[DocumentRead],
)
async def list_product_documents(product_id: int, session: SessionDep):
    """Lista os documentos de um produto (paginado)."""
    service = DocumentService(session)
    await service.ensure_product_exists(product_id)
    statement = service.list_documents_by_product_statement(product_id)
    return await apaginate(session, statement)
