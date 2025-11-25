from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# --- CORRECCIÓN AQUÍ ---
# NO uses esto (importa el archivo):
# from app.services import monitor_service

# USA ESTO (importa la variable 'monitor_service' que está DENTRO del archivo 'monitor_service.py'):
from app.services.monitor_service import monitor_service
# -----------------------

from app.api import routers, websockets

app = FastAPI(
    title="Jurassic Park System",
    on_startup=[monitor_service.iniciar_sistema] # Ahora sí encontrará el método
)

# 1. Montar la carpeta estática (para CSS/JS/Img si tuvieras más)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 2. Rutas API
app.include_router(routers.router)
app.include_router(websockets.router)

# 3. Ruta Raíz -> Sirve el HTML
@app.get("/")
async def read_index():
    return FileResponse("app/static/index.html")