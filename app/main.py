from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.api.routes.product_router import router as product_router
from app.api.errors.handlers import register_error_handlers

app = FastAPI(
    title="Sistema de Comandas"
)

app.include_router(product_router)

register_error_handlers(app)
add_pagination(app)
