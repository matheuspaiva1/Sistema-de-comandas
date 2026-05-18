import random
from datetime import timedelta
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.command import Command, CommandStatus
from app.models.client import Client
from app.models.table import Table

fake = Faker("pt_BR")

async def seed_commands(session: AsyncSession, clients: list[Client], tables: list[Table], count: int = 150) -> list[Command]:
    """Cria comandas associadas aos clientes e mesas."""
    commands = []
    
    for i in range(count):
        client = random.choice(clients)
        table = random.choice(tables)
        status = random.choice(list(CommandStatus))
        
        opened_at = fake.date_time_between(start_date="-60d", end_date="now")
        closed_at = None
        
        if status in [CommandStatus.FECHADA, CommandStatus.CANCELADA]:
            closed_at = opened_at + timedelta(minutes=random.randint(45, 240))
            
        command = Command(
            code=fake.unique.random_number(digits=8),
            client_id=client.id,
            status=status,
            opened_at=opened_at,
            closed_at=closed_at,
            total_amount=0.0,
            table_id=table.id,
        )
        
        session.add(command)
        commands.append(command)
        
        if (i + 1) % 20 == 0:
            print(f"  ✓ {i + 1}/{count} comandas criadas")
            
    await session.commit()
    
    for c in commands:
        await session.refresh(c)
        
    return commands
