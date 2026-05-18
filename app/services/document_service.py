from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.api.errors.exceptions import (
    DocumentNotFoundException,
    InvalidFileException,
)
from app.services.product_service import ProductService


class DocumentService:
    """
    Serviço responsável pelo gerenciamento de arquivos e documentos associados a Produtos.
    
    Controla o upload, download, substituição e remoção física de documentos
    no armazenamento local, além de persistir e validar os metadados dos arquivos
    (tamanho, extensão permitida e tipo MIME) no banco de dados.
    """
    ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".gif"}
    MAX_FILE_SIZE = 50 * 1024 * 1024 

    def __init__(self, session: AsyncSession) -> None:
        self.repo = DocumentRepository(session)
        self.product_service = ProductService(session)

    def _parse_upload(self, file: UploadFile) -> tuple[str, str, str]:
        """Valida e extrai nome, content-type e extensão do arquivo enviado."""
        if not file.filename:
            raise InvalidFileException("Nome do arquivo inválido")

        file_parts = file.filename.rsplit(".", 1)
        if len(file_parts) != 2:
            raise InvalidFileException("Arquivo deve ter extensão")

        _, extension_raw = file_parts
        extension = f".{extension_raw.lower()}"

        if extension not in self.ALLOWED_EXTENSIONS:
            raise InvalidFileException(f"Extensão não permitida: {extension}")

        return file.filename, file.content_type or "application/octet-stream", extension

    async def _read_and_validate(self, file: UploadFile) -> tuple[str, str, str, bytes]:
        """Lê o conteúdo do arquivo e valida tamanho e extensão."""
        original_filename, content_type, extension = self._parse_upload(file)
        file_content = await file.read()

        if len(file_content) == 0:
            raise InvalidFileException("Arquivo vazio")

        if len(file_content) > self.MAX_FILE_SIZE:
            raise InvalidFileException(
                f"Arquivo excede tamanho máximo de {self.MAX_FILE_SIZE / 1024 / 1024:.0f}MB"
            )

        return original_filename, content_type, extension, file_content

    async def upload_document(self, product_id: int, file: UploadFile) -> Document:
        """Valida o produto, processa o arquivo e persiste o documento."""
        await self.product_service.get_product(product_id)
        original_filename, content_type, extension, file_content = await self._read_and_validate(file)

        return await self.repo.create(
            product_id=product_id,
            original_filename=original_filename,
            content_type=content_type,
            extension=extension,
            size_bytes=len(file_content),
            file_content=file_content,
        )

    async def get_document(self, document_id: UUID) -> Document:
        """Retorna um documento pelo UUID ou lança DocumentNotFoundException."""
        document = await self.repo.get_by_id(document_id)
        if not document:
            raise DocumentNotFoundException(document_id)
        return document

    async def ensure_product_exists(self, product_id: int) -> None:
        """Garante que o produto existe, lançando exceção caso contrário."""
        await self.product_service.get_product(product_id)

    def list_documents_by_product_statement(self, product_id: int):
        """Retorna statement de listagem de documentos de um produto."""
        return self.repo.list_by_product_statement(product_id)

    async def download_document(self, document_id: UUID) -> tuple[str, str, str]:
        """Retorna caminho físico, content-type e nome original do arquivo para download."""
        document = await self.get_document(document_id)
        file_path = await self.repo.get_file_path(document_id)
        if file_path is None:
            raise DocumentNotFoundException(document_id)
        return str(file_path), document.content_type, document.original_filename

    async def replace_document(self, document_id: UUID, file: UploadFile) -> Document:
        """Substitui o arquivo físico e metadados de um documento existente."""
        await self.get_document(document_id)
        original_filename, content_type, extension, file_content = await self._read_and_validate(file)

        document = await self.repo.update_file(
            document_id=document_id,
            original_filename=original_filename,
            content_type=content_type,
            extension=extension,
            size_bytes=len(file_content),
            file_content=file_content,
        )
        if not document:
            raise DocumentNotFoundException(document_id)
        return document

    async def delete_document(self, document_id: UUID) -> None:
        """Remove o documento e seu arquivo físico pelo UUID."""
        await self.get_document(document_id)
        success = await self.repo.delete(document_id)
        if not success:
            raise DocumentNotFoundException(document_id)
