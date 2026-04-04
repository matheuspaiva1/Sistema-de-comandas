from fastapi import FastAPI
from app.domains.comanda import comanda_controller
from app.domains.shared.export import export_controller
from app.domains.shared.hash import hash_controller

app = FastAPI(
    title="Sistemas de comandas + Delta Lake",
    version="1.0.0",
    description="API refatorada com o motor puro python `deltalake`, operações CRUD e auto-increment via .seq",
)

app.include_router(comanda_controller.router)
app.include_router(export_controller.router)
app.include_router(hash_controller.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="[IP_ADDRESS]", port=8000)
