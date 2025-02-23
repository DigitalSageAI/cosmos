import asyncio
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    FSInputFile,
    Message
)
from aiogram.filters import Command
from typing import Dict

router = Router()


@router.message(Command('start'))
async def send_welcome(message: types.Message, **kwargs):
    #user_status = kwargs[user_status]
    await message.reply(text="Привет, Администратор!")
    # user_status = user_data['user_status']
    # if user_status == 'admin':
    #     await message.reply(text="Привет, Администратор!")