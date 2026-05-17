from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from fastapi_pagination.ext.sqlmodel import paginate

from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate


class PaymentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: PaymentCreate) -> Payment:
        payment = Payment.model_validate(data)
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def get_by_id(self, payment_id: int) -> Optional[Payment]:
        return await self.session.get(Payment, payment_id)

    async def list_all(self):
        return await paginate(self.session, select(Payment).order_by(Payment.id.desc()))

    async def update(self, payment: Payment, data: PaymentUpdate) -> Payment:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(payment, key, value)
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def delete(self, payment: Payment) -> None:
        await self.session.delete(payment)
        await self.session.commit()
