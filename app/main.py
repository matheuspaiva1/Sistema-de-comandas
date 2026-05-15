from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.api.routes.product_router import router as product_router

app = FastAPI(
    title="Sistema de Comandas"
)

app.include_router(product_router)

add_pagination(app)
