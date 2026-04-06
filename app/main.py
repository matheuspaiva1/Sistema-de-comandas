from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppError
from app.domains.comanda import comanda_controller
from app.domains.item_comanda import item_comanda_controller
from app.domains.produto import produto_controller
from app.domains.shared.export import export_controller
from app.domains.shared.export import export_product_controller
from app.domains.shared.hash import hash_controller

app = FastAPI(
    title="Sistemas de comandas + Delta Lake",
    version="1.0.0",
    description="API refatorada com o motor puro python `deltalake`, operações CRUD e auto-increment via .seq",
)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


app.include_router(comanda_controller.router)
app.include_router(item_comanda_controller.router)
app.include_router(produto_controller.router)
app.include_router(export_controller.router)
app.include_router(export_product_controller.router)
app.include_router(hash_controller.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="[IP_ADDRESS]", port=8000)
