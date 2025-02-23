from aiogram import BaseMiddleware
from typing import Dict, Any, Callable, Awaitable
import asyncio

from db.crud import UsersService
from config.settings import env_vars


class NewUserMiddleware(BaseMiddleware):
    async def check_if_user_is_admin(self, tg_id: int) -> str:
        return 'admin' if tg_id == env_vars['ADMIN_ID'] else 'base_user'
            
        return 

    async def __call__(
        self,
        handler: Callable[..., Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ):
        text = event.message.text
        if text != '/start':
             return await handler(event, data)
        
        tg_id = data['event_from_user'].id
        if not await UsersService.check_exist_user(tg_id):
            await UsersService.add_new_user(
                tg_id,
                data['event_from_user'].username,
                data['event_from_user'].language_code
                )
            return await handler(event, data)
        data['user_status'] = {'user_status': await self.check_if_user_is_admin(tg_id)}
        return await handler(event, data)




    