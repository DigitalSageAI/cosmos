from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.settings import env_vars

bot = Bot(token=env_vars['BOT_API_TOKEN'])
dp = Dispatcher(storage=MemoryStorage())