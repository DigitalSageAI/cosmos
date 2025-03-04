from aiogram import BaseMiddleware
from typing import Dict, Any, Callable, Awaitable

from tg_bot.config.settings import env_vars

class NewUserMiddleware(BaseMiddleware):
    def __init__(self, redis_connector, user_service):
        super().__init__()
        self.redis_connector = redis_connector
        self.user_service = user_service

    async def __call__(
        self,
        handler: Callable[..., Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        """Processing incoming messages for new users"""
        if not self._is_start_command(event.message.text):
            return await handler(event, data)

        tg_id = data['event_from_user'].id
        utm = self._extract_utm_from_message(event.message.text)

        if await self._is_new_user(tg_id):
            await self._add_new_user(tg_id, data, utm)
        else:
            await self._set_user_status(tg_id, data)

        return await handler(event, data)

    def _is_start_command(self, message_text: str) -> bool:
        """Checks if the message is the /start command"""
        return message_text.startswith('/start')

    def _extract_utm_from_message(self, message_text: str) -> str | None:
        """Extracts the UTM tag from the message"""
        parts = message_text.split()
        return parts[1] if len(parts) > 1 else None

    async def _is_new_user(self, tg_id: int) -> bool:
        """Checks if the user is new"""
        return not await self.user_service.check_exist_user(tg_id)

    async def _add_new_user(self, tg_id: int, data: Dict[str, Any], utm: str) -> None:
        """Adds a new user to the database and Redis"""
        await self.user_service.add_new_user(
            tg_id,
            data['event_from_user'].username,
            data['event_from_user'].language_code,
            utm
        )
        redis_key = f"user_id:{tg_id}"
        data = {"language": data['event_from_user'].language_code}
        redis_client = await self.redis_connector.get_client(db=0)
        if redis_client is not None:
            async with redis_client.pipeline() as pipe:
                await pipe.hset(redis_key, mapping=data)
                await pipe.expire(redis_key, 3600)  # setting TTL - 1 hour (3600 secs)
                await pipe.execute() 

    async def _set_user_status(self, tg_id: int, data: Dict[str, Any]) -> None:
        """Sets the user status"""
        data['user_status'] = {'user_status': self._get_user_status(tg_id)}

    def _get_user_status(self, tg_id: int) -> str:
        """Determines the user status"""
        return 'admin' if tg_id == env_vars['ADMIN_ID'] else 'base_user'

