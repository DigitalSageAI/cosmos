import asyncio
import aiogram
from tg_bot.bot import bot, dp
from infrastructure.redis_connection import RedisConnector
from config.settings import bot_logger
from tg_bot.middleware.new_user_middleware import NewUserMiddleware
from tg_bot.handlers.commands import router

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.update.outer_middleware(NewUserMiddleware())
    dp.include_router(router)

    redis_connector = RedisConnector(bot_logger)
    redis_client = redis_connector.get_client(0)
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