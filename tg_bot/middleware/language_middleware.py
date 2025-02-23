from aiogram import BaseMiddleware
from typing import Optional, Dict, Any, Callable, Awaitable, Union
import asyncio


class LanguageMiddleware(BaseMiddleware):
    def __init__(self, redis_connector):
        self.redis_connector = redis_connector
        super().__ini__()

    async def get_language_from_db(self):


    async def get_langiage_from_redis(self):
        