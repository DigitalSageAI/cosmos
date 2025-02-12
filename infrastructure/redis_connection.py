import redis.asyncio as redis
import asyncio

class RedisConnector:
    """Asynchronous connector for Redis.

    This class provides methods to establish and manage a connection to a Redis server.
    """

    def __init__(self, db: int, logger, host: str = 'localhost', port: int = 6379):
        """
        Initialize a RedisConnector instance.

        Args:
            db (int): Redis database index.
            logger: Logger instance for recording messages.
            host (str, optional): Hostname of the Redis server. Defaults to 'localhost'.
            port (int, optional): Port of the Redis server. Defaults to 6379.

        Internal Attributes:
            _lock (asyncio.Lock): Asynchronous lock used to synchronize connection initialization,
                                  preventing concurrent attempts to establish a connection.
        """
        self.db = db
        self.logger = logger
        self.host = host
        self.port = port
        self.client = None
        self._lock = asyncio.Lock()

    async def connect(self, timeout: int = 5):
        """
        Establish a connection to the Redis server and validate it with a ping.

        On success, the client instance is stored.
        On failure, the error is logged and the client is set to None.

        Args:
            timeout (int, optional): Connection timeout in seconds. Defaults to 5.
        """
        try:
            client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True,
                socket_timeout=timeout
            )
            await client.ping()
            self.client = client
            self.logger.info(f"Connected to Redis (DB={self.db}) successfully!")
        except Exception as e:
            self.logger.error(f"Redis connection error (DB={self.db}): {e}")
            self.client = None

    async def get_client(self):
        """
        Return the active Redis client, connecting if necessary.

        If the client has not been created yet, a lock (_lock) is used to ensure that
        multiple coroutines do not initialize the connection concurrently.

        Returns:
            The Redis client instance.
        """
        if self.client is None:
            async with self._lock:
                if self.client is None:
                    await self.connect()
        return self.client
    
    async def close_conn(self):
        """
        Close the active Redis connection, if it exists.
        """
        if self.client:
            await self.client.close()
            self.logger.info(f"Redis connection (DB={self.db}) closed!")
            self.client = None
