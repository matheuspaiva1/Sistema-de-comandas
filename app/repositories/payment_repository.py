from typing import Optional

from beanie import PydanticObjectId

from app.models.payment import Payment, PaymentStatus
from app.models.command import Command
from app.schemas.payment import PaymentCreate, PaymentUpdate


class PaymentRepository:
    """Repositório de acesso a dados para a entidade Payment."""

    async def create(self, command: Command, data: PaymentCreate) -> Payment:
        payment = Payment(command=command, **data.model_dump(exclude={"command_id"}))
        await payment.insert()
        return payment

    async def get_by_id(self, payment_id: PydanticObjectId) -> Optional[Payment]:
        return await Payment.get(payment_id, fetch_links=True)

    async def list_by_command(self, command_id: PydanticObjectId) -> list[Payment]:
        return await Payment.find(
            Payment.command.id == command_id, 
            fetch_links=True,
        ).to_list()

    async def list_all(self, status: PaymentStatus | None = None) -> list[Payment]:
        query = {"status": status} if status else {}
        return await Payment.find(query, fetch_links=True).sort("-_id").to_list()

    async def update(self, payment: Payment, data: PaymentUpdate) -> Payment:
        update_data = data.model_dump(exclude_unset=True)
        await payment.set(update_data)
        return payment

    async def delete(self, payment: Payment) -> None:
        await payment.delete()
