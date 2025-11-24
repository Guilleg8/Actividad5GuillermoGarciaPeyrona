from dataclasses import dataclass

@dataclass
class SensorData:
    sensor_id: str
    tipo: str
    valor: float
    timestamp: float