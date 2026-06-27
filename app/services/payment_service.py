from beanie import PydanticObjectId

from app.api.errors.exceptions import EntityNotFoundException
from app.models.payment import Payment
from app.repositories.payment_repository import PaymentRepository
from app.repositories.command_repository import CommandRepository
from app.schemas.payment import PaymentCreate, PaymentUpdate


class PaymentService:
    """Lógica de negócios para pagamentos de Comandas."""

    def __init__(self) -> None:
        self.repo = PaymentRepository()
        self.command_repo = CommandRepository()

    async def create_payment(self, data: PaymentCreate) -> Payment:
        command_id = PydanticObjectId(data.command_id)
        command = await self.command_repo.get_by_id(command_id)
        if not command:
            raise EntityNotFoundException("Comanda", data.command_id)
        return await self.repo.create(command, data)

    async def list_payments(self) -> list[Payment]:
        return await self.repo.list_all()

    async def get_payment(self, payment_id: PydanticObjectId) -> Payment:
        payment = await self.repo.get_by_id(payment_id)
        if not payment:
            raise EntityNotFoundException("Pagamento", str(payment_id))
        return payment

    async def update_payment(self, payment_id: PydanticObjectId, data: PaymentUpdate) -> Payment:
        payment = await self.get_payment(payment_id)
        return await self.repo.update(payment, data)

    async def delete_payment(self, payment_id: PydanticObjectId) -> None:
        payment = await self.get_payment(payment_id)
        await self.repo.delete(payment)
