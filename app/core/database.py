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

        # Fix for schema drift in development: if commands table exists but
        # missing the `table_id` column, add it via ALTER TABLE so app code
        # that expects Command.table_id won't fail with OperationalError.
        try:
            result = await conn.execute(text("PRAGMA table_info('commands')"))
            rows = result.all()
            cols = [row[1] for row in rows]
            if 'table_id' not in cols:
                await conn.execute(text('ALTER TABLE commands ADD COLUMN table_id INTEGER'))
        except Exception:
            # If PRAGMA or ALTER fails, don't stop startup — the error will surface
            # on first DB access and can be investigated. We suppress here to keep
            # init non-fatal during development.
            pass

        # sanitize table status values that may have been written incorrectly
        try:
            await conn.execute(
                text("UPDATE tables SET status = 'LIVRE' WHERE status IS NULL OR status NOT IN ('LIVRE','OCUPADA')")
            )
        except Exception:
            pass
