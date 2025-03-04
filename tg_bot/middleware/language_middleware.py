from aiogram import BaseMiddleware
from typing import Optional, Dict, Any, Callable, Awaitable, Union
import asyncio

class LanguageMiddleware(BaseMiddleware):
    """
    Middleware for handling user language preferences in a Telegram bot.
    It retrieves the user's language from Redis or a database and sets it in the event data.
    """

    def __init__(self, redis_connector, user_service):
        """
        Initializes the LanguageMiddleware with Redis and user service connectors.

        :param redis_connector: Connector for interacting with Redis.
        :param user_service: Service for interacting with user data in the database.
        """
        super().__init__()
        self.redis_connector = redis_connector
        self.user_service = user_service

    async def __call__(
        self,
        handler: Callable[..., Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        """
        Processes incoming events to determine and set the user's language.

        :param handler: The next middleware or handler in the chain.
        :param event: The event being processed.
        :param data: A dictionary containing event data.
        :return: The result of the next handler in the chain.
        """
        tg_id = data['event_from_user'].id
        language = await self.get_language_from_redis(tg_id)
        if not language:
            language = await self.get_language_from_db(tg_id)
            if language:
                await self.set_language_to_redis(tg_id, language)
            else:
                language = "en"

        data["user_lang"] = language
        return await handler(event, data)

    async def get_language_from_db(self, tg_id: int) -> str:
        """
        Retrieves the user's language from the database.

        :param tg_id: The Telegram ID of the user.
        :return: The language code of the user.
        """
        language = await self.user_service.get_user_language(tg_id)
        return language if language else None

    async def get_language_from_redis(self, tg_id: int) -> Optional[str]:
        """
        Retrieves the user's language from Redis.

        :param tg_id: The Telegram ID of the user.
        :return: The language code of the user if found, otherwise None.
        """
        redis_key = f"user_id:{tg_id}"
        redis_client = await self.redis_connector.get_client(db=0)
        if redis_client is not None:
            language = await redis_client.hget(redis_key, "language")
            if language:
                return language
        return None

    async def set_language_to_redis(self, tg_id: int, lang: str) -> None:
        """
        Sets the user's language in Redis.

        :param tg_id: The Telegram ID of the user.
        :param lang: The language code to set for the user.
        """
        redis_key = f"user:{tg_id}:lang"
        data = {"language": lang}
        redis_client = await self.redis_connector.get_client(db=0)
        if redis_client is not None:
            async with redis_client.pipeline() as pipe:
                await pipe.hset(redis_key, mapping=data)
                await pipe.expire(redis_key, 3600)
                await pipe.execute()