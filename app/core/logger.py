import logging
import asyncio
import sys

# Configurar el formato del log para que se vea bien en la consola
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

class AsyncLoggerWrapper:
    """
    Un logger 'falso' asíncrono que usa el logging estándar de Python.
    Es 100% compatible con Windows y evita el error NotImplementedError.
    """
    def __init__(self, name="jurassic_logger"):
        self.logger = logging.getLogger(name)

    async def info(self, msg):
        # Imprime directamente (es lo suficientemente rápido para esta demo)
        self.logger.info(msg)

    async def error(self, msg):
        self.logger.error(msg)

    async def warning(self, msg):
        self.logger.warning(msg)

# Instancia global
logger = AsyncLoggerWrapper()