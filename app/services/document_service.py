from uuid import UUID

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany
from fastapi import UploadFile

from app.models.document import FileDocument
from app.repositories.document_repository import DocumentRepository
from app.api.errors.exceptions import DocumentNotFoundException, InvalidFileException
from app.services.product_service import ProductService


class DocumentService:
    """Lógica de negócios para documentos associados a Produtos."""

    ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".gif"}
    MAX_FILE_SIZE = 50 * 1024 * 1024

    def __init__(self) -> None:
        self.repo = DocumentRepository()
        self.product_service = ProductService()

    def _parse_upload(self, file: UploadFile) -> tuple[str, str, str]:
        if not file.filename:
            raise InvalidFileException("Nome do arquivo inválido")
        parts = file.filename.rsplit(".", 1)
        if len(parts) != 2:
            raise InvalidFileException("Arquivo deve ter extensão")
        extension = f".{parts[1].lower()}"
        if extension not in self.ALLOWED_EXTENSIONS:
            raise InvalidFileException(f"Extensão não permitida: {extension}")
        return file.filename, file.content_type or "application/octet-stream", extension

    async def _read_and_validate(self, file: UploadFile) -> tuple[str, str, str, bytes]:
        original_filename, content_type, extension = self._parse_upload(file)
        content = await file.read()
        if len(content) == 0:
            raise InvalidFileException("Arquivo vazio")
        if len(content) > self.MAX_FILE_SIZE:
            raise InvalidFileException(f"Arquivo excede {self.MAX_FILE_SIZE // 1024 // 1024}MB")
        return original_filename, content_type, extension, content

    async def upload_document(self, product_id: PydanticObjectId, file: UploadFile) -> FileDocument:
        product = await self.product_service.get_product(product_id)
        original_filename, content_type, extension, content = await self._read_and_validate(file)
        return await self.repo.create(
            product=product,
            original_filename=original_filename,
            content_type=content_type,
            extension=extension,
            size_bytes=len(content),
            file_content=content,
        )

    async def get_document(self, document_id: UUID) -> FileDocument:
        document = await self.repo.get_by_id(document_id)
        if not document:
            raise DocumentNotFoundException(document_id)
        return document

    def list_documents_by_product(self, product_id: PydanticObjectId) -> FindMany[FileDocument]:
        return self.repo.list_by_product(product_id)

    async def download_document(self, document_id: UUID) -> tuple[bytes, str, str]:
        """Baixa o arquivo do MinIO e retorna (bytes, content_type, original_filename)."""
        result = await self.repo.download_file(document_id)
        if result is None:
            raise DocumentNotFoundException(document_id)
        return result

    async def replace_document(self, document_id: UUID, file: UploadFile) -> FileDocument:
        await self.get_document(document_id)
        original_filename, content_type, extension, content = await self._read_and_validate(file)
        document = await self.repo.update_file(
            document_id=document_id,
            original_filename=original_filename,
            content_type=content_type,
            extension=extension,
            size_bytes=len(content),
            file_content=content,
        )
        if not document:
            raise DocumentNotFoundException(document_id)
        return document

    async def delete_document(self, document_id: UUID) -> None:
        await self.get_document(document_id)
        if not await self.repo.delete(document_id):
            raise DocumentNotFoundException(document_id)
