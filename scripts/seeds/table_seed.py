import random
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.table import Table, TableStatus

async def seed_tables(session: AsyncSession, count: int = 100) -> list[Table]:
    """Cria mesas no sistema."""
    tables = []
    
    for i in range(1, count + 1):
        table = Table(
            number=i,
            name=f"Mesa {i}",
            seats=random.choice([2, 4, 6, 8, 10]),
            location=random.choice(["Salão Principal", "Varanda", "Mezanino", "Jardim", "Balcão"]),
            status=random.choice(list(TableStatus)),
        )
        session.add(table)
        tables.append(table)
        
        if i % 20 == 0:
            print(f"  ✓ {i}/{count} mesas criadas")
            
    await session.commit()
    
    for t in tables:
        await session.refresh(t)
        
    return tables
