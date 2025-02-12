import asyncio
import aiogram
from bot import bot, dp
from infrastructure.redis_connection import RedisConnector
from config.settings import bot_logger


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    redis_connector = RedisConnector(1, bot_logger)
    redis_client = redis_connector.get_client()
    if not redis_client:
        bot_logger.error("Не удалось подключиться к Redis. Завершаем работу бота.")
        return
    
    try:
        bot_logger.info("Бот запущен. Нажмите Command+C для остановки.")
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        bot_logger.info("Остановка бота по запросу пользователя...")
    finally:
        await redis_connector.close_conn()

if __name__ == '__main__':
    asyncio.run(main())