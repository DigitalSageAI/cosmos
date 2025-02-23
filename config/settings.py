from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging
import os
from typing import Dict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv()

class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    

class DBConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    db_name: str

    def get_asyncpg_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

class DatabaseSettings(CommonSettings):
    DB_CONFIGS: Dict[str, DBConfig] = Field(default_factory=dict)

    @classmethod
    def get_(cls, key: str) -> str:
        settings = cls() 
        db_config = settings.DB_CONFIGS.get(key)
        if not db_config:
            raise ValueError(f"Database configuration for key '{key}' is missing.")
        return db_config.get_asyncpg_url()


class RedisSettings(CommonSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_TIMEOUT: int

redis_settings = RedisSettings()

def load_env_vars():
    load_dotenv()
    env_vars = {
        "TG_BOT_API_TOKEN": os.getenv("TG_BOT_API_TOKEN"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),
        "ADMIN_ID": os.getenv("ADMIN_ID")
    }
    
    missing_vars = [var for var, value in env_vars.items() if not value]

    if missing_vars:
        raise ValueError(f"Не найдены env_vars в файле .env - {missing_vars}")
    
    return env_vars

env_vars = load_env_vars()


def loger_setup(logger_name, logger_file):
    level = env_vars["LOG_LEVEL"]

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    if not logger.handlers:
        file_handler = logging.FileHandler(logger_file, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
    return logger

bot_logger = loger_setup('bot_logger', 'tg_bot/logs/bot_logs.log')
fapi_logger = loger_setup('fast_api', 'api/logs/api_logs.log')



