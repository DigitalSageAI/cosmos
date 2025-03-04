from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from tg_bot.config.settings import bot_logger, env_vars

from tg_bot.db.crud import UsersService
from infrastructure.redis_connection import RedisConnector
from tg_bot.db.session import async_session_maker

bot = Bot(token=env_vars['TG_BOT_API_TOKEN'])
dp = Dispatcher(storage=MemoryStorage())

user_service = UsersService(async_session_maker)
redis_connector = RedisConnector(bot_logger)