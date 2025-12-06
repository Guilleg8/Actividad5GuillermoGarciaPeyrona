import io
import psutil
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fastapi import APIRouter, Response
from app.services.monitor_service import monitor_service

router = APIRouter()


@router.get("/metrics/status")
async def get_system_status():
    process = psutil.Process()
    mem_info = process.memory_info()

    hist = monitor_service.metrics["tps_history"]
    current_tps = hist[-1] if hist else 0

    return {
        "system_health": "OK",
        "resource_usage": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_mb": round(mem_info.rss / 1024 / 1024, 2)
        },
        "performance_metrics": {
            "current_tps": current_tps,
            "total_events": monitor_service.metrics["total_events"],
            "avg_latency_ms": round(monitor_service.metrics["latency_avg"], 3),
            "alerts": monitor_service.metrics["alerts_triggered"]
        }
    }


@router.get("/metrics/chart")
def get_performance_chart():

    history = monitor_service.metrics["tps_history"]
    if not history:
        return Response(content="Cargando datos...", media_type="text/plain")

    plt.figure(figsize=(10, 4))
    plt.plot(history, label='TPS', color='green')
    plt.title('Monitor Reactivo - Jurassic Park')
    plt.grid(True, alpha=0.3)
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return Response(content=buf.getvalue(), media_type="image/png")