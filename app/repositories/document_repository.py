from pathlib import Path
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.document import Document
from app.core.config import settings


class DocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def _file_path(self, document_id: UUID, extension: str) -> Path:
        return self.upload_dir / f"{document_id}{extension}"

    async def create(
        self,
        product_id: int,
        original_filename: str,
        content_type: str,
        extension: str,
        size_bytes: int,
        file_content: bytes,
    ) -> Document:
        document = Document(
            product_id=product_id,
            original_filename=original_filename,
            content_type=content_type,
            extension=extension,
            size_bytes=size_bytes,
        )
        self.session.add(document)
        await self.session.commit()
        await self.session.refresh(document)

        self._file_path(document.id, extension).write_bytes(file_content)
        return document

    async def get_by_id(self, document_id: UUID) -> Optional[Document]:
        return await self.session.get(Document, document_id)

    def list_by_product_statement(self, product_id: int):
        return (
            select(Document)
            .where(Document.product_id == product_id)
            .order_by(Document.created_at.desc())
        )

    async def get_file_path(self, document_id: UUID) -> Optional[Path]:
        document = await self.get_by_id(document_id)
        if not document:
            return None

        file_path = self._file_path(document.id, document.extension)
        if file_path.exists():
            return file_path
        return None

    async def update_file(
        self,
        document_id: UUID,
        original_filename: str,
        content_type: str,
        extension: str,
        size_bytes: int,
        file_content: bytes,
    ) -> Optional[Document]:
        document = await self.get_by_id(document_id)
        if not document:
            return None

        old_path = self._file_path(document.id, document.extension)

        document.original_filename = original_filename
        document.content_type = content_type
        document.extension = extension
        document.size_bytes = size_bytes
        self.session.add(document)
        await self.session.commit()
        await self.session.refresh(document)

        new_path = self._file_path(document.id, extension)
        if old_path != new_path and old_path.exists():
            old_path.unlink()

        new_path.write_bytes(file_content)
        return document

    async def delete(self, document_id: UUID) -> bool:
        document = await self.get_by_id(document_id)
        if not document:
            return False

        file_path = self._file_path(document.id, document.extension)
        if file_path.exists():
            file_path.unlink()

        await self.session.delete(document)
        await self.session.commit()
        return True

    async def delete_by_product(self, product_id: int) -> int:
        result = await self.session.execute(
            select(Document).where(Document.product_id == product_id)
        )
        documents = result.scalars().all()
        count = 0
        for doc in documents:
            if await self.delete(doc.id):
                count += 1
        return count
