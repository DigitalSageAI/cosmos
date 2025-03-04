import asyncio

from tg_bot.bot import *
from tg_bot.middleware.new_user_middleware import NewUserMiddleware
from tg_bot.middleware.language_middleware import LanguageMiddleware
from tg_bot.handlers.commands import router

from tg_bot.config.settings import bot_logger



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.update.outer_middleware(NewUserMiddleware(redis_connector,user_service))
    dp.update.outer_middleware(LanguageMiddleware(redis_connector,user_service))
    dp.include_router(router)

    redis_client = redis_connector.get_client(db=0)
    if not redis_client:
        bot_logger.error("Не удалось подключиться к Redis. Завершаем работу бота.")
        return
    
    try:
        bot_logger.info("Бот запущен. Нажмите Command+C для остановки.")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        bot_logger.info("Остановка бота по запросу пользователя...")
    finally:
        await redis_connector.close_conn()

if __name__ == '__main__':
    asyncio.run(main())