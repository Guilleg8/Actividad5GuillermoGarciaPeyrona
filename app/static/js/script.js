// app/static/js/script.js

const MAX_TABLE_ROWS = 15;

document.addEventListener('DOMContentLoaded', () => {
    connectWebSocket();
    // Refrescar métricas cada 2 segundos
    setInterval(fetchMetrics, 2000);
});

// --- 1. WebSocket para Datos en Tiempo Real ---
function connectWebSocket() {
    // Detecta automáticamente si es ws:// o wss:// (seguro)
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/live`;

    const ws = new WebSocket(wsUrl);
    const statusBadge = document.getElementById('connection-status');

    ws.onopen = () => {
        statusBadge.className = 'badge bg-success';
        statusBadge.innerHTML = '<span class="live-indicator connected"></span> Sistema Online';
        console.log("WS Conectado");
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        updateTable(data);
        document.getElementById('last-update').innerText = "Último dato: " + data.timestamp.split('T')[1].split('.')[0];
    };

    ws.onclose = () => {
        statusBadge.className = 'badge bg-danger';
        statusBadge.innerHTML = '<span class="live-indicator disconnected"></span> Offline (Reconectando...)';
        // Reintentar conexión en 3 segundos
        setTimeout(connectWebSocket, 3000);
    };

    ws.onerror = (err) => {
        console.error("Error en WS:", err);
        ws.close();
    };
}

// --- 2. Actualizar Tabla ---
function updateTable(data) {
    const tbody = document.getElementById('sensor-table-body');
    const row = document.createElement('tr');

    // Lógica de Alerta Visual
    let isAlert = false;
    let statusText = "Normal";

    // Umbrales visuales (coinciden con el backend)
    if ((data.type === 'cardiaco' && data.value > 180) ||
        (data.type === 'temperatura' && data.value > 40) ||
        (data.type === 'movimiento' && data.value > 80)) {
        row.classList.add('alert-row');
        isAlert = true;
        statusText = "CRÍTICO";
    }

    row.innerHTML = `
        <td>${data.timestamp.split('T')[1].slice(0,8)}</td>
        <td class="fw-bold text-warning">${data.sensor}</td>
        <td>${data.type.toUpperCase()}</td>
        <td class="fw-bold">${data.value.toFixed(2)}</td>
        <td>${isAlert ? '⚠️ ' + statusText : '✅ OK'}</td>
    `;

    tbody.prepend(row); // Añadir arriba

    // Limpiar filas viejas para no saturar memoria del navegador
    if (tbody.children.length > MAX_TABLE_ROWS) {
        tbody.removeChild(tbody.lastChild);
    }
}

// --- 3. Polling para Métricas y Gráfico ---
async function fetchMetrics() {
    try {
        // Actualizar imagen del gráfico con timestamp para evitar caché
        const chartImg = document.getElementById('chart-img');
        if(chartImg) {
            chartImg.src = `/metrics/chart?t=${new Date().getTime()}`;
        }

        // Obtener datos numéricos
        const response = await fetch('/metrics/status');
        if (!response.ok) throw new Error("Error HTTP");

        const data = await response.json();

        document.getElementById('cpu-val').innerText = data.resource_usage.cpu_percent + '%';
        document.getElementById('mem-val').innerText = data.resource_usage.memory_mb + ' MB';
        document.getElementById('tps-val').innerText = data.performance_metrics.current_tps;
        // El backend envía "alerts", no "active_alerts"
        document.getElementById('alerts-val').innerText = data.performance_metrics.alerts;
    } catch (e) {
        console.error("Error obteniendo métricas:", e);
    }

}