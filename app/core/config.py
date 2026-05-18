from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação carregadas a partir do arquivo .env."""

    app_name: str = "Sistema de Comandas"
    database_url: str
    upload_dir: str = "app/uploads"

    class Config:
        """Configuração do Pydantic para leitura do .env."""

        env_file = ".env"


settings = Settings()
