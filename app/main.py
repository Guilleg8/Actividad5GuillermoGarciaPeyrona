from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


from app.services.monitor_service import monitor_service

from app.api import routers, websockets

app = FastAPI(
    title="Jurassic Park System",
    on_startup=[monitor_service.iniciar_sistema]
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(routers.router)
app.include_router(websockets.router)

@app.get("/")
async def read_index():
    return FileResponse("app/static/index.html")