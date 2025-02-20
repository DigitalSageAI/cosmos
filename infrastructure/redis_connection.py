import redis.asyncio as redis
import asyncio
from config.settings import RedisSettings


class RedisConnector:
    """Asynchronous connector for a Redis server.

    This class provides methods to establish and manage a connection
    to a Redis server.
    """

    def __init__(self, logger):
        """
        Initialize the RedisConnector instance.

        Args:
            logger: A logger instance for logging messages.

        Attributes:
            host (str): Redis server hostname obtained from RedisSettings.REDIS_HOST.
            port (int): Redis server port obtained from RedisSettings.REDIS_PORT.
            timeout (int): Connection timeout (in seconds) obtained from RedisSettings.REDIS_TIMEOUT.
            _lock (asyncio.Lock): An asynchronous lock to synchronize connection initialization.
            client: The Redis client instance (initially None).
        """
        self.logger = logger
        self.host = RedisSettings.REDIS_HOST
        self.port = RedisSettings.REDIS_PORT
        self.timeout = RedisSettings.REDIS_TIMEOUT
        self._lock = asyncio.Lock()
        self.client = None

    async def connect(self, db: int = 0):
        """
        Establish a connection to the Redis server using the specified database index
        and validate the connection with a ping.

        Upon a successful connection, the client instance is stored and a success
        message is logged. If the connection fails, the error is logged and the client
        is set to None.

        Args:
            db (int, optional): The Redis database index to connect to. Defaults to 0.
        """
        try:
            self.db = db  # Save the database index for logging purposes
            client = redis.Redis(
                host=self.host,
                port=self.port,
                db=db,
                decode_responses=True,
                socket_timeout=self.timeout
            )
            await client.ping()
            self.client = client
            self.logger.info(f"Connected to Redis (DB={self.db}) successfully!")
        except Exception as e:
            self.logger.error(f"Redis connection error (DB={self.db}): {e}")
            self.client = None

    async def get_client(self):
        """
        Retrieve the active Redis client instance, establishing a connection if necessary.

        This method uses an asynchronous lock to ensure that multiple coroutines do not
        initialize the connection concurrently. If the client is not already connected,
        it will establish a connection using the default database index (0).

        Returns:
            The active Redis client instance.
        """
        if self.client is None:
            async with self._lock:
                if self.client is None:
                    await self.connect()
        return self.client

    async def close_conn(self):
        """
        Close the active Redis connection, if it exists, and log the operation.
        After closing, the Redis client instance is set to None.
        """
        if self.client:
            await self.client.close()
            self.logger.info(f"Redis connection (DB={self.db}) closed!")
            self.client = None
