from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.api.errors.exceptions import EntityNotFoundException
from app.models.payment import Payment, PaymentStatus
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

    def list_payments(
        self,
        status: PaymentStatus | None = None,
        command_id: str | None = None,
    ) -> FindMany[Payment]:
        parsed_command_id = PydanticObjectId(command_id) if command_id else None
        return self.repo.list_all(status=status, command_id=parsed_command_id)

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
