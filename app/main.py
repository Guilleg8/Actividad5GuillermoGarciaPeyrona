from fastapi import FastAPI
from app.services.monitor_service import monitor_service
from app.api import routers, websockets

# Crear app y registrar evento de inicio
app = FastAPI(
    title="Jurassic Park System",
    on_startup=[monitor_service.iniciar_sistema]
)

# Incluir rutas
app.include_router(routers.router)
app.include_router(websockets.router)