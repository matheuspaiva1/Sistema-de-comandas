from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlmodel import SQLModel

from app.core.config import settings


engine = create_async_engine(
    settings.database_url,
    echo=True
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    import app.models  # noqa: F401

    async with engine.begin() as conn:
        # create tables if not present
        await conn.run_sync(SQLModel.metadata.create_all)

        try:
            result = await conn.execute(text("PRAGMA table_info('commands')"))
            rows = result.all()
            cols = [row[1] for row in rows]
            if 'table_id' not in cols:
                await conn.execute(text('ALTER TABLE commands ADD COLUMN table_id INTEGER'))
        except Exception:
            pass

        try:
            await conn.execute(
                text("UPDATE tables SET status = 'LIVRE' WHERE status IS NULL OR status NOT IN ('LIVRE','OCUPADA')")
            )
        except Exception:
            pass
