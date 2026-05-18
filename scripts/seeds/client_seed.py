import random
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.client import Client

fake = Faker("pt_BR")

async def seed_clients(session: AsyncSession, count: int = 120) -> list[Client]:
    """Cria clientes fictícios."""
    clients = []
    
    for i in range(count):
        client = Client(
            name=fake.name(),
            phone=fake.cellphone_number(),
            email=fake.unique.email(),
            tax_id=fake.cpf() if random.random() > 0.3 else None,
        )
        session.add(client)
        clients.append(client)
        
        if (i + 1) % 20 == 0:
            print(f"  ✓ {i + 1}/{count} clientes criados")
            
    await session.commit()
    
    for c in clients:
        await session.refresh(c)
        
    return clients
