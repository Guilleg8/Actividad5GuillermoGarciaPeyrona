import asyncio
import time
import rx
from rx import operators as ops
from rx.subject import Subject
from rx.scheduler.eventloop import AsyncIOScheduler

from app.core.config import APP_NAME, ALERT_THRESHOLDS
from app.core.logger import logger
from app.models.sensor_data import SensorData
from app.services.sensor_factory import SensorFactory


class JurassicMonitorService:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.scheduler = AsyncIOScheduler(self.loop)
        self.factory = SensorFactory(self.scheduler)

        # Estado del sistema (Métricas en memoria)
        self.metrics = {
            "total_events": 0,
            "tps_history": [],
            "latency_avg": 0.0,
            "alerts_triggered": 0,
            "last_data": {}
        }

        # Subject principal para transmitir datos a WebSockets
        self.broadcast_stream = Subject()
        self.is_running = False

    def iniciar_sistema(self):
        if self.is_running:
            return

        print(f"--- Iniciando Servicios de {APP_NAME} ---")
        self.is_running = True

        # 1. Crear flujos
        s1 = self.factory.crear_stream("cardiaco", "T-Rex-01", 0.1)
        s2 = self.factory.crear_stream("temperatura", "T-Rex-01", 2.0)
        s3 = self.factory.crear_stream("movimiento", "Raptor-Squad", 0.05)
        s4 = self.factory.crear_stream("cardiaco", "Brachio-05", 1.0)

        # 2. Fusionar flujos
        self.main_stream = rx.merge(s1, s2, s3, s4).pipe(ops.share())

        # --- PIPELINES REACTIVOS ---

        # A. Visualización (WebSocket) con Sampling
        self.main_stream.pipe(
            ops.sample(0.1),
            ops.map(lambda d: self._update_last_data(d))
        ).subscribe(self.broadcast_stream)

        # B. Métricas (TPS) con Buffering
        self.main_stream.pipe(
            ops.buffer_with_time(1.0),
            ops.map(lambda batch: len(batch))
        ).subscribe(
            on_next=lambda count: self._update_tps(count),
            scheduler=self.scheduler
        )

        # C. Alertas con Throttle
        self.main_stream.pipe(
            ops.filter(lambda d: d.valor > ALERT_THRESHOLDS.get(d.tipo, 999)),
            ops.throttle_first(2.0)
        ).subscribe(
            on_next=lambda d: asyncio.create_task(self._log_alert(d)),
            scheduler=self.scheduler
        )

    def _update_last_data(self, data: SensorData):
        self.metrics["last_data"][data.sensor_id] = data
        latency = (time.time() - data.timestamp) * 1000
        self.metrics["latency_avg"] = (self.metrics["latency_avg"] * 0.9) + (latency * 0.1)
        return data

    def _update_tps(self, count):
        self.metrics["total_events"] += count
        self.metrics["tps_history"].append(count)
        if len(self.metrics["tps_history"]) > 60:
            self.metrics["tps_history"].pop(0)

    async def _log_alert(self, data: SensorData):
        self.metrics["alerts_triggered"] += 1
        msg = f"🚨 ALERTA: {data.sensor_id} [{data.tipo}] Valor: {data.valor}"
        await logger.error(msg)
        print(msg)


# Instancia Singleton para ser importada por la API
monitor_service = JurassicMonitorService()