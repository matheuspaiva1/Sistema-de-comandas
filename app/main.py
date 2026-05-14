from fastapi import FastAPI
from fastapi_pagination import add_pagination

app = FastAPI(
    title="Sistema de Comandas"
)

# app.include_router(...)

add_pagination(app)
