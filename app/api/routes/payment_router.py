from fastapi import APIRouter, status
from fastapi_pagination import Page

from app.api.deps import SessionDep
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentRead, PaymentUpdate
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Pagamentos"])


@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
async def create_payment(data: PaymentCreate, session: SessionDep) -> Payment:
    service = PaymentService(session)
    return await service.create_payment(data)


@router.get("/", response_model=Page[PaymentRead])
async def list_payments(session: SessionDep):
    service = PaymentService(session)
    return await service.list_payments()


@router.get("/{payment_id}", response_model=PaymentRead)
async def get_payment(payment_id: int, session: SessionDep) -> Payment:
    service = PaymentService(session)
    return await service.get_payment(payment_id)


@router.put("/{payment_id}", response_model=PaymentRead)
async def update_payment(payment_id: int, data: PaymentUpdate, session: SessionDep) -> Payment:
    service = PaymentService(session)
    return await service.update_payment(payment_id, data)


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(payment_id: int, session: SessionDep) -> None:
    service = PaymentService(session)
    await service.delete_payment(payment_id)
