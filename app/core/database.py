import beanie
import motor.motor_asyncio

from app.core.config import settings


async def init_db():
    """Inicializa a conexão com o MongoDB e registra os modelos no Beanie."""
    from app.models import Client, Table, Product, Payment, Command, Document

    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
    db = client[settings.database_name]

    await beanie.init_beanie(
        database=db,
        document_models=[Client, Table, Product, Payment, Command, Document],
    )
