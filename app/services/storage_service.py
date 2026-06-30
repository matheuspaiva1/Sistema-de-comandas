"""Serviço de armazenamento de objetos usando MinIO."""

from io import BytesIO
from uuid import UUID

from minio import Minio
from minio.error import S3Error

from app.core.config import settings


class StorageService:
    """Encapsula operações de upload, download e deleção de arquivos no MinIO."""

    def __init__(self) -> None:
        self.client = Minio(
            endpoint=settings.minio_endpoint,
            access_key=settings.minio_root_user,
            secret_key=settings.minio_root_password,
            secure=settings.minio_secure,
        )
        self.bucket = settings.minio_bucket
        self._ensure_bucket()

    def _ensure_bucket(self) -> None:
        """Cria o bucket padrão caso ele ainda não exista."""
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    @staticmethod
    def _object_name(document_id: UUID, extension: str) -> str:
        """Gera o nome do objeto no formato '<uuid><extensão>'."""
        return f"{document_id}{extension}"

    def upload(
        self,
        document_id: UUID,
        extension: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> str:
        """Faz upload de bytes para o MinIO e retorna o object_name utilizado.

        Args:
            document_id: UUID do documento.
            extension: Extensão do arquivo (ex: '.pdf', '.png').
            data: Conteúdo do arquivo em bytes.
            content_type: MIME type do arquivo.

        Returns:
            O nome do objeto armazenado no bucket.
        """
        object_name = self._object_name(document_id, extension)
        stream = BytesIO(data)
        self.client.put_object(
            bucket_name=self.bucket,
            object_name=object_name,
            data=stream,
            length=len(data),
            content_type=content_type,
        )
        return object_name

    def download(self, document_id: UUID, extension: str) -> bytes:
        """Baixa o conteúdo de um objeto do MinIO e retorna como bytes.

        Args:
            document_id: UUID do documento.
            extension: Extensão do arquivo.

        Returns:
            O conteúdo do arquivo em bytes.

        Raises:
            S3Error: Se o objeto não existir no bucket.
        """
        object_name = self._object_name(document_id, extension)
        response = None
        try:
            response = self.client.get_object(
                bucket_name=self.bucket,
                object_name=object_name,
            )
            return response.read()
        finally:
            if response is not None:
                response.close()
                response.release_conn()

    def delete(self, document_id: UUID, extension: str) -> None:
        """Remove um objeto do MinIO.

        Args:
            document_id: UUID do documento.
            extension: Extensão do arquivo.
        """
        object_name = self._object_name(document_id, extension)
        self.client.remove_object(
            bucket_name=self.bucket,
            object_name=object_name,
        )

    def exists(self, document_id: UUID, extension: str) -> bool:
        """Verifica se um objeto existe no bucket.

        Args:
            document_id: UUID do documento.
            extension: Extensão do arquivo.

        Returns:
            True se o objeto existir, False caso contrário.
        """
        object_name = self._object_name(document_id, extension)
        try:
            self.client.stat_object(
                bucket_name=self.bucket,
                object_name=object_name,
            )
            return True
        except S3Error:
            return False
