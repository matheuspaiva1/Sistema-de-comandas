import random
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.command import Command, CommandStatus
from app.models.payment import Payment, PaymentMethod, PaymentStatus

async def seed_payments(session: AsyncSession, commands: list[Command]) -> list[Payment]:
    """Cria pagamentos para as comandas fechadas."""
    payments = []
    
    for command in commands:
        if command.status == CommandStatus.FECHADA:
            payment = Payment(
                command_id=command.id,
                amount=command.total_amount,
                method=random.choice(list(PaymentMethod)),
                status=PaymentStatus.PAGO,
                paid_at=command.closed_at
            )
            session.add(payment)
            payments.append(payment)
            
        elif command.status == CommandStatus.CANCELADA and random.random() > 0.8:
            payment = Payment(
                command_id=command.id,
                amount=command.total_amount,
                method=random.choice(list(PaymentMethod)),
                status=PaymentStatus.ESTORNADO,
                paid_at=command.opened_at + timedelta(minutes=10)
            )
            session.add(payment)
            payments.append(payment)
            
    await session.commit()
    
    for p in payments:
        await session.refresh(p)
        
    print(f"  ✓ {len(payments)} pagamentos processados")
    return payments
