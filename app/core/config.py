from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Sistema de Comandas"
    database_url: str
    upload_dir: str = "app/uploads"

    class Config:
        env_file = ".env"


settings = Settings()
