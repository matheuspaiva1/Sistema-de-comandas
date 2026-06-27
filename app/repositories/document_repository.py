from pathlib import Path
from typing import Optional
from uuid import UUID

from beanie import PydanticObjectId

from app.models.document import FileDocument
from app.models.product import Product
from app.core.config import settings


class DocumentRepository:
    """Repositório de metadados de documentos. Arquivos físicos são gerenciados pelo StorageService (MinIO)."""

    def __init__(self) -> None:
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def _file_path(self, document_id: UUID, extension: str) -> Path:
        return self.upload_dir / f"{document_id}{extension}"

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
        self._file_path(document.id, extension).write_bytes(file_content)
        return document

    async def get_by_id(self, document_id: UUID) -> Optional[FileDocument]:
        return await FileDocument.find_one({"_id": document_id}, fetch_links=True)

    async def list_by_product(self, product_id: PydanticObjectId) -> list[FileDocument]:
        return await FileDocument.find(
            FileDocument.product.id == product_id, 
            fetch_links=True,
        ).sort("-created_at").to_list()

    async def get_file_path(self, document_id: UUID) -> Optional[Path]:
        document = await self.get_by_id(document_id)
        if not document:
            return None
        path = self._file_path(document.id, document.extension)
        return path if path.exists() else None

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

        old_path = self._file_path(document.id, document.extension)
        await document.set({
            "original_filename": original_filename,
            "content_type": content_type,
            "extension": extension,
            "size_bytes": size_bytes,
        })

        new_path = self._file_path(document.id, extension)
        if old_path != new_path and old_path.exists():
            old_path.unlink()
        new_path.write_bytes(file_content)
        return document

    async def delete(self, document_id: UUID) -> bool:
        document = await self.get_by_id(document_id)
        if not document:
            return False
        path = self._file_path(document.id, document.extension)
        if path.exists():
            path.unlink()
        await document.delete()
        return True

    async def delete_by_product(self, product_id: PydanticObjectId) -> int:
        documents = await self.list_by_product(product_id)
        count = 0
        for doc in documents:
            if await self.delete(doc.id):
                count += 1
        return count
