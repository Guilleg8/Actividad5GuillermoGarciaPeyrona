import random
import time
import rx
from rx import operators as ops
from app.models.sensor_data import SensorData


class SensorFactory:
    """Genera flujos reactivos simulando sensores físicos."""

    def __init__(self, scheduler):
        self.scheduler = scheduler

    def crear_stream(self, tipo: str, sensor_id: str, frecuencia: float):
        """Crea un Observable que emite datos periódicos."""
        return rx.interval(frecuencia).pipe(
            ops.map(lambda _: self._generar_dato(tipo, sensor_id)),
            ops.observe_on(self.scheduler)
        )

    def _generar_dato(self, tipo: str, sensor_id: str) -> SensorData:
        val = 0
        if tipo == "temperatura":
            val = random.gauss(37.5, 2.0)
        elif tipo == "cardiaco":
            val = random.gauss(80, 10) if random.random() > 0.1 else random.gauss(190, 5)
        elif tipo == "movimiento":
            val = random.expovariate(1 / 20)

        return SensorData(
            sensor_id=sensor_id,
            tipo=tipo,
            valor=round(val, 2),
            timestamp=time.time()
        )