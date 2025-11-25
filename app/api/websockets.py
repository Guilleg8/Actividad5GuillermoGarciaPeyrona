import asyncio
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.monitor_service import monitor_service
from app.models.sensor_data import SensorData

router = APIRouter()


@router.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # 1. Obtenemos el bucle de eventos actual (el "jefe" de FastAPI)
    loop = asyncio.get_running_loop()
    queue = asyncio.Queue()

    # 2. Función de puente SEGURO (Thread-Safe)
    def on_next(data: SensorData):
        # ESTA ES LA CLAVE:
        # Usamos call_soon_threadsafe para decirle al bucle principal:
        # "Oye, cuando tengas un hueco, mete esto en la cola".
        # Esto evita choques si RxPY está ejecutándose en otro hilo.
        loop.call_soon_threadsafe(queue.put_nowait, data)

    # 3. Suscripción
    # Nos aseguramos de que el servicio esté iniciado
    if not monitor_service.is_running:
        print("⚠️ El servicio de monitorización no estaba iniciado. Iniciando...")
        monitor_service.iniciar_sistema()

    disposable = monitor_service.broadcast_stream.subscribe(
        on_next=on_next,
        on_error=lambda e: print(f"Error en stream Rx: {e}")
    )

    try:
        while True:
            # 4. Esperar datos de la cola (esto es 100% async y seguro)
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