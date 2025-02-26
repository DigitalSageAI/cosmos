from typing import Optional

import redis.asyncio as redis
import asyncio
from config.settings import redis_settings

class RedisConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisConnector, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, logger):
        if self._initialized:
            return
        self.logger = logger
        self.host = redis_settings.REDIS_HOST
        self.port = redis_settings.REDIS_PORT
        self.timeout = redis_settings.REDIS_TIMEOUT
        self._lock = asyncio.Lock()

        self.clients = {}
        self._initialized = True

    async def connect(self, db: int):
        try:
            async with self._lock:
                if db not in self.clients:
                    client = redis.Redis(
                        host=self.host,
                        port=self.port,
                        db=db,
                        decode_responses=True,
                        socket_timeout=self.timeout
                    )
                    await client.ping()
                    self.clients[db] = client
                    self.logger.info(f"Connected to Redis (DB={db}) successfully!")
        except Exception as e:
            self.logger.error(f"Redis connection error (DB={db}): {e}")

    async def get_client(self, db: int):
        if db not in self.clients:
            await self.connect(db)
        return self.clients.get(db)

    async def close_conn(self, db: Optional[int] = None):
        async with self._lock:
            if db is not None:
                if db in self.clients:
                    await self.clients[db].close()
                    self.logger.info(f"Redis connection (DB={db}) closed!")
                    del self.clients[db]
            else:
                for db_key in list(self.clients.keys()):
                    await self.clients[db_key].close()
                    self.logger.info(f"Redis connection (DB={db_key}) closed!")
                    del self.clients[db_key]