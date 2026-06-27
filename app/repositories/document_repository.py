from typing import Optional
from uuid import UUID

from beanie import PydanticObjectId

from app.models.document import FileDocument
from app.models.product import Product
from app.services.storage_service import StorageService


class DocumentRepository:
    """Repositório de metadados de documentos. Arquivos físicos são gerenciados pelo StorageService (MinIO)."""

    def __init__(self) -> None:
        self.storage = StorageService()

    async def create(
        self,
        product: Product,
        original_filename: str,
        content_type: str,
        extension: str,
        size_bytes: int,
        file_content: bytes,
    ) -> FileDocument:
        document = FileDocument(
            product=product,
            original_filename=original_filename,
            content_type=content_type,
            extension=extension,
            size_bytes=size_bytes,
        )
        await document.insert()
        self.storage.upload(
            document_id=document.id,
            extension=extension,
            data=file_content,
            content_type=content_type,
        )
        return document

    async def get_by_id(self, document_id: UUID) -> Optional[FileDocument]:
        return await FileDocument.find_one({"_id": document_id}, fetch_links=True)

    async def list_by_product(self, product_id: PydanticObjectId) -> list[FileDocument]:
        return await FileDocument.find(
            FileDocument.product.id == product_id, 
            fetch_links=True,
        ).sort("-created_at").to_list()

    async def download_file(self, document_id: UUID) -> Optional[tuple[bytes, str, str]]:
        """Baixa o arquivo do MinIO e retorna (bytes, content_type, original_filename).

        Returns:
            Tupla com o conteúdo, MIME type e nome original, ou None se o documento não existir.
        """
        document = await self.get_by_id(document_id)
        if not document:
            return None
        if not self.storage.exists(document.id, document.extension):
            return None
        data = self.storage.download(document.id, document.extension)
        return data, document.content_type, document.original_filename

    async def update_file(
        self,
        document_id: UUID,
        original_filename: str,
        content_type: str,
        extension: str,
        size_bytes: int,
        file_content: bytes,
    ) -> Optional[FileDocument]:
        document = await self.get_by_id(document_id)
        if not document:
            return None

        old_extension = document.extension
        await document.set({
            "original_filename": original_filename,
            "content_type": content_type,
            "extension": extension,
            "size_bytes": size_bytes,
        })

        # Remove o arquivo antigo se a extensão mudou
        if old_extension != extension:
            self.storage.delete(document.id, old_extension)

        self.storage.upload(
            document_id=document.id,
            extension=extension,
            data=file_content,
            content_type=content_type,
        )
        return document

    async def delete(self, document_id: UUID) -> bool:
        document = await self.get_by_id(document_id)
        if not document:
            return False
        self.storage.delete(document.id, document.extension)
        await document.delete()
        return True

    async def delete_by_product(self, product_id: PydanticObjectId) -> int:
        documents = await self.list_by_product(product_id)
        count = 0
        for doc in documents:
            if await self.delete(doc.id):
                count += 1
        return count
