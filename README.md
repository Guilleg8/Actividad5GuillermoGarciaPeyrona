# 🦕 Jurassic Park Secure Monitor v1.0

**Jurassic Park Secure Monitor** es un sistema de monitorización en tiempo real diseñado para gestionar flujos de datos de alta frecuencia provenientes de sensores biométricos y ambientales de dinosaurios (simulados).

El proyecto implementa una **Arquitectura Reactiva** utilizando **RxPY** (Reactive Extensions for Python) y **FastAPI**, garantizando que el sistema sea capaz de manejar picos de carga mediante estrategias de **Backpressure**, manteniendo la interfaz fluida y el servidor estable.

---

## 🚀 Características Clave

* **📡 Monitorización en Tiempo Real:** Uso de **WebSockets** para transmitir datos de sensores al frontend instantáneamente.
* **⚡ Arquitectura Reactiva:** Procesamiento de flujos de datos asíncronos con **RxPY**.
* **🛡️ Gestión de Backpressure:** Implementación de tres estrategias clave en `monitor_service.py` para evitar la saturación:
    * **Sampling (`sample`):** Controla la frecuencia de refresco visual en el navegador.
    * **Buffering (`buffer_with_time`):** Agrupa eventos para el cálculo eficiente de métricas (TPS).
    * **Throttling (`throttle_first`):** Gestiona alertas críticas evitando duplicados masivos.
* **🧵 Thread-Safety:** Implementación robusta usando `asyncio.Queue` y `call_soon_threadsafe` para comunicar los hilos reactivos con el bucle de eventos de FastAPI.
* **📊 Dashboard Interactivo:** Interfaz oscura con gráficos históricos (Matplotlib), KPIs en tiempo real y diagramas de arquitectura dinámicos (Mermaid.js).

---

## 🛠️ Stack Tecnológico

* **Backend:** Python 3.13, FastAPI, Uvicorn (Standard).
* **Motor Reactivo:** RxPY (ReactiveX).
* **Asincronía:** Asyncio (con soporte específico para Windows SelectorEventLoop).
* **Frontend:** HTML5, Bootstrap 5, JavaScript (Vanilla), Mermaid.js.
* **Visualización Backend:** Matplotlib (Backend Agg) para generación de gráficos estáticos.

---

## 📂 Estructura del Proyecto

```text
jurassic_monitor/
├── app/
│   ├── api/
│   │   ├── routers.py       # Endpoints HTTP (KPIs, Gráficos PNG)
│   │   └── websockets.py    # Endpoint WS (Puente Thread-safe RxPY -> Asyncio)
│   ├── core/
│   │   ├── config.py        # Constantes (Umbrales de temperatura, cardiaco)
│   │   └── logger.py        # Wrapper de logging compatible con Asyncio
│   ├── models/
│   │   └── sensor_data.py   # Dataclass para estructura de datos
│   ├── services/
│   │   ├── monitor_service.py # Lógica central, Pipelines RxPY y Backpressure
│   │   └── sensor_factory.py  # Simulación de sensores (Observables)
│   ├── static/              # Frontend (CSS, JS, Imágenes, HTML)
│   └── main.py              # Configuración de FastAPI y montaje de estáticos
├── requirements             # Dependencias del proyecto
└── run.py                   # Script de ejecución (incluye fix para Windows)
