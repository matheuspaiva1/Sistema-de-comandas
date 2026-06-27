from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação carregadas a partir do arquivo .env."""

    app_name: str = "Sistema de Comandas"
    mongo_url: str
    database_name: str = "yourmenu"
    upload_dir: str = "app/uploads"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
