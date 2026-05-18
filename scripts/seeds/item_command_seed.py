import random
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.command import Command
from app.models.product import Product
from app.models.item_command import ItemCommand

async def seed_item_commands(session: AsyncSession, commands: list[Command], products: list[Product]) -> list[ItemCommand]:
    """Cria itens para as comandas."""
    item_commands = []
    
    for i, command in enumerate(commands):
        num_items = random.randint(1, 6)
        total_comanda = 0.0
        
        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(1, 4)
            unit_price = product.price
            
            item = ItemCommand(
                command_id=command.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price
            )
            total_comanda += (quantity * unit_price)
            
            session.add(item)
            item_commands.append(item)
            
        command.total_amount = total_comanda
        session.add(command)
        
        if (i + 1) % 20 == 0:
            print(f"  ✓ Itens criados para {i + 1}/{len(commands)} comandas")
            
    await session.commit()
    
    for item in item_commands:
        await session.refresh(item)
        
    return item_commands
