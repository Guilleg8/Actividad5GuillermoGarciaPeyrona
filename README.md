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
```
---

##⚙️ Instalación y Ejecución

###1.Clonar el repositorio
git clone <url-del-repo>
cd jurassic-monitor

###2. Configurar entorno virtualSe recomienda usar un entorno virtual para aislar las dependencias.Bashpython -m venv .venv
En Windows:
.venv\Scripts\activate
En Mac/Linux:
source .venv/bin/activate

###3. Instalar dependencias
Es crucial instalar uvicorn[standard] para el soporte completo de WebSockets, tal como se especifica en el archivo requirements.
pip install -r requirements

###4. Ejecutar el Servidor
Utiliza el script run.py incluido. Este script configura automáticamente asyncio.WindowsSelectorEventLoopPolicy si detecta que estás en Windows, evitando errores de concurrencia.
python run.py

Nota: El servidor arrancará en http://0.0.0.0:8000 con la recarga automática desactivada (reload=False) para garantizar la estabilidad del bucle de eventos en Windows.

5. Acceder al Dashboard
Abre tu navegador web y visita:👉 http://localhost:8000

---

##🧠 Conceptos de Backpressure Implementados

El sistema gestiona la alta carga de datos en monitor_service.py mediante los siguientes operadores reactivos:
 **1. Visualización**: ops.sample(0.1) Toma solo el último dato cada 100ms. Evita saturar el WebSocket y el renderizado JS del cliente, independientemente de la frecuencia de entrada.
 **2. Métricas**: (TPS)ops.buffer_with_time(1.0)Acumula todos los eventos de 1 segundo en una lista (batch). Permite contar el volumen total de transacciones con una sola operación por segundo.
 **3. Alertas**: ops.throttle_first(2.0)Tras detectar una alerta crítica, silencia alertas idénticas del mismo flujo durante 2 segundos. Previene el "spam" de logs cuando un sensor mantiene valores críticos.

---

📝 Créditos
Desarrollado por Guillermo García Peyrona como parte de la Actividad de Monitorización Reactiva.
