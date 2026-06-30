from typing import Optional

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

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

    def list_all(
        self,
        status: PaymentStatus | None = None,
        command_id: PydanticObjectId | None = None,
    ) -> FindMany[Payment]:
        query: dict = {}
        if status:
            query["status"] = status
        if command_id:
            query["command.$id"] = command_id
        return Payment.find(query, fetch_links=True).sort("-_id")

    async def update(self, payment: Payment, data: PaymentUpdate) -> Payment:
        update_data = data.model_dump(exclude_unset=True)
        await payment.set(update_data)
        return payment

    async def delete(self, payment: Payment) -> None:
        await payment.delete()
