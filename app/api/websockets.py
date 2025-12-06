import asyncio
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.monitor_service import monitor_service
from app.models.sensor_data import SensorData

router = APIRouter()


@router.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    loop = asyncio.get_running_loop()
    queue = asyncio.Queue()

    def on_next(data: SensorData):
        loop.call_soon_threadsafe(queue.put_nowait, data)

    if not monitor_service.is_running:
        print("⚠️ El servicio de monitorización no estaba iniciado. Iniciando...")
        monitor_service.iniciar_sistema()

    disposable = monitor_service.broadcast_stream.subscribe(
        on_next=on_next,
        on_error=lambda e: print(f"Error en stream Rx: {e}")
    )

    try:
        while True:
            data = await queue.get()

            await websocket.send_json({
                "sensor": data.sensor_id,
                "type": data.tipo,
                "value": data.valor,
                "timestamp": datetime.fromtimestamp(data.timestamp).isoformat()
            })

    except WebSocketDisconnect:
        print("Cliente desconectado")
    except Exception as e:
        print(f"Error FATAL en WebSocket: {e}")
    finally:
        disposable.dispose()