import logging
import asyncio
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

class AsyncLoggerWrapper:

    def __init__(self, name="jurassic_logger"):
        self.logger = logging.getLogger(name)

    async def info(self, msg):
        self.logger.info(msg)

    async def error(self, msg):
        self.logger.error(msg)

    async def warning(self, msg):
        self.logger.warning(msg)

logger = AsyncLoggerWrapper()