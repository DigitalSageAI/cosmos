import asyncio
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    FSInputFile,
    Message
)
from aiogram.filters import Command


router = Router()


@router.message(Command('start'))
async def send_welcome(message: Message):
