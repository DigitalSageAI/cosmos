import asyncio
from typing import Dict
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    FSInputFile,
    Message
)
from aiogram.filters import Command

from tg_bot.locals.extractor_translations import translator

router = Router()


@router.message(Command('start'))
async def send_welcome(message: types.Message, **kwargs):
    for key, value in kwargs.items():
        print(f"{key=}: {value=}")
    #user_status = kwargs["user_status"]
    lang = kwargs["user_lang"]
    
    await message.reply(text=translator.get("start", lang))
    #await message.reply(text="hi")
    # user_status = user_data['user_status']
    # if user_status == 'admin':
    #     await message.reply(text="Привет, Администратор!")



@router.message(Command('menu'))
async def main_menu(message: types.Message, **kwargs):
    await message.reply(text="Menu")


@router.message(Command('ask_ai'))
async def main_menu(message: types.Message, **kwargs):
    await message.reply(text="AI")


@router.message(Command('change_language'))
async def main_menu(message: types.Message, **kwargs):
    await message.reply(text="change_language")