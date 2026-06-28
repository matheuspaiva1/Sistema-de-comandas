from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação carregadas a partir do arquivo .env."""

    app_name: str = "Sistema de Comandas"
    database_name: str = "yourmenu"
    upload_dir: str = "app/uploads"

    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_root_user: str = "admin"
    mongo_root_password: str = "adminpassword"
    mongo_url_override: Optional[str] = Field(default=None, validation_alias="MONGO_URL")

    @property
    def mongo_url(self) -> str:
        """Retorna MONGO_URL quando definida ou monta a connection string do MongoDB."""
        if self.mongo_url_override:
            return self.mongo_url_override
        return (
            f"mongodb://{self.mongo_root_user}:{self.mongo_root_password}"
            f"@{self.mongo_host}:{self.mongo_port}/"
        )

    minio_host: str = "localhost"
    minio_port: int = 9000
    minio_root_user: str = "admin"
    minio_root_password: str = "adminpassword"
    minio_bucket: str = "documents"
    minio_secure: bool = False

    @property
    def minio_endpoint(self) -> str:
        """Endpoint do MinIO no formato host:port."""
        return f"{self.minio_host}:{self.minio_port}"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
