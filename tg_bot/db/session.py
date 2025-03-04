import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from tg_bot.config.settings import DatabaseSettings
from sqlalchemy.orm import DeclarativeBase

# Предположим, что вы хотите получить URL для определённого ключа
database_url = DatabaseSettings.get_db_url('tg_db')


engine = create_async_engine(
    url=database_url,
    echo=True
)
async_session_maker = async_sessionmaker(engine, expire_on_commit = False)


class Base(DeclarativeBase):
    pass



