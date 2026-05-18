from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors.exceptions import EntityNotFoundException
from app.models.payment import Payment
from app.repositories.payment_repository import PaymentRepository
from app.repositories.command_repository import CommandRepository
from app.schemas.payment import PaymentCreate, PaymentUpdate


class PaymentService:
    """
    Serviço responsável pelo fluxo de pagamentos de Comandas.
    
    Permite registrar novos pagamentos vinculados a comandas existentes,
    assim como consultar, atualizar e excluir históricos de pagamentos.
    """
    def __init__(self, session: AsyncSession) -> None:
        self.repo = PaymentRepository(session)
        self.command_repo = CommandRepository(session)

    async def create_payment(self, data: PaymentCreate) -> Payment:
        if data.command_id:
            command = await self.command_repo.get_by_id(data.command_id)
            if not command:
                raise EntityNotFoundException("Comanda", data.command_id)
        return await self.repo.create(data)

    async def list_payments(self):
        return await self.repo.list_all()

    async def get_payment(self, payment_id: int) -> Payment:
        payment = await self.repo.get_by_id(payment_id)
        if not payment:
            raise EntityNotFoundException("Pagamento", payment_id)
        return payment

    async def update_payment(self, payment_id: int, data: PaymentUpdate) -> Payment:
        payment = await self.get_payment(payment_id)
        return await self.repo.update(payment, data)

    async def delete_payment(self, payment_id: int) -> None:
        payment = await self.get_payment(payment_id)
        await self.repo.delete(payment)
