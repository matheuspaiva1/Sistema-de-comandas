from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.core.database import init_db
from app.api.routes.product_router import router as product_router
from app.api.routes.document_router import (
    documents_router,
    products_documents_router,
)
from app.api.routes.reports_router import router as reports_router
from app.api.routes.client_router import router as client_router
from app.api.routes.command_router import router as command_router
from app.api.routes.order_router import router as order_router
from app.api.routes.order_item_router import router as order_item_router
from app.api.errors.handlers import register_error_handlers

app = FastAPI(
    title="Sistema de Comandas",
    description="Sistema de Comandas com FastAPI, SQLModel e persistência relacional",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Produtos",
            "description": "Endpoints de produtos",
        },
        {
            "name": "Documentos",
            "description": "Endpoints de upload/download de documentos",
        },
        {
            "name": "Consultas Analíticas e Relatórios",
            "description": "Endpoints de consultas complexas, filtros e agregações",
        },
        {
            "name": "Comandas",
            "description": "Endpoints de comandas",
        },
        {
            "name": "Pedidos",
            "description": "Endpoints de pedidos",
        },
        {
            "name": "Itens do Pedido",
            "description": "Endpoints de itens do pedido",
        },
        {
            "name": "Cliente",
            "description": "Endpoints de clientes",
        },
    ],
)

app.include_router(product_router)
app.include_router(documents_router)
app.include_router(products_documents_router)
app.include_router(reports_router)
app.include_router(client_router)
app.include_router(command_router)
app.include_router(order_router)
app.include_router(order_item_router)


@app.on_event("startup")
async def on_startup():
    await init_db()

register_error_handlers(app)
add_pagination(app)
