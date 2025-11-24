import asyncio
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.monitor_service import monitor_service
from app.models.sensor_data import SensorData

router = APIRouter()


@router.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        def on_next(data: SensorData):
            # Enviar al cliente asíncronamente
            asyncio.create_task(websocket.send_json({
                "sensor": data.sensor_id,
                "type": data.tipo,
                "value": data.valor,
                "timestamp": datetime.fromtimestamp(data.timestamp).isoformat()
            }))

        # Suscribirse al stream de broadcast (que ya tiene backpressure)
        disposable = monitor_service.broadcast_stream.subscribe(on_next)

        # Loop para mantener conexión viva
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        disposable.dispose()
        print("Cliente WebSocket desconectado")