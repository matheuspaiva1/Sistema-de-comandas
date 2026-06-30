from beanie import PydanticObjectId
from fastapi import APIRouter, status
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate

from app.schemas.payment import PaymentCreate, PaymentRead, PaymentUpdate
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Pagamentos"])


@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
async def create_payment(data: PaymentCreate):
    """Registra um novo pagamento vinculado a uma comanda."""
    return await PaymentService().create_payment(data)


@router.get("/", response_model=Page[PaymentRead])
async def list_payments():
    """Lista todos os pagamentos."""
    return await paginate(PaymentService().list_payments())


@router.get("/{payment_id}", response_model=PaymentRead)
async def get_payment(payment_id: PydanticObjectId):
    """Retorna um pagamento pelo ID."""
    return await PaymentService().get_payment(payment_id)


@router.put("/{payment_id}", response_model=PaymentRead)
async def update_payment(payment_id: PydanticObjectId, data: PaymentUpdate):
    """Atualiza os dados de um pagamento."""
    return await PaymentService().update_payment(payment_id, data)


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(payment_id: PydanticObjectId):
    """Remove um pagamento pelo ID."""
    await PaymentService().delete_payment(payment_id)
