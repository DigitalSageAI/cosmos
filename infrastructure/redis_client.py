# redis_client.py
from config.settings import bot_logger
from infrastructure.redis_connection import RedisConnector

redis_connector = RedisConnector(bot_logger)