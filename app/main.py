from fastapi import FastAPI
from app.api import comanda_controller, export_controller, hash_controller

app = FastAPI(title="Sistema de Comandas API", version="1.0.0")

app.include_router(comanda_controller.router)
app.include_router(export_controller.router)
app.include_router(hash_controller.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)