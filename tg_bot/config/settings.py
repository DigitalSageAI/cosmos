import logging
import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def find_project_root(target_folder: str = "tg_bot") -> Path:
    """
    Search for the project's root directory by locating the specified target folder.
    
    :param target_folder: Name of the folder considered as project root.
    :return: Path to the project root.
    :raises FileNotFoundError: If the folder is not found.
    """
    current_path = Path(__file__).resolve()
    
    for parent in current_path.parents:
        if parent.name == target_folder:
            return parent
    
    raise FileNotFoundError(f"Project root folder '{target_folder}' not found in parent directories of {current_path}")


# Define base directory
BASE_DIR = find_project_root("tg_bot")
TRANSLATIONS_FILE = BASE_DIR / "locals" / "translations.json"

# Load environment variables
load_dotenv(BASE_DIR / "config" / ".env")


class CommonSettings(BaseSettings):
    """
    Common settings with environment file configuration.
    """
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8")


class DBConfig(BaseModel):
    """
    Database configuration model.
    """
    host: str
    port: int
    user: str
    password: str
    db_name: str

    def get_asyncpg_url(self) -> str:
        """
        Generate an asyncpg-compatible PostgreSQL connection URL.
        """
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class DatabaseSettings(CommonSettings):
    """
    Database settings with multiple configurations.
    """
    DB_CONFIGS: Dict[str, DBConfig] = Field(default_factory=dict)

    @classmethod
    def get_db_url(cls, key: str) -> str:
        """
        Retrieve the asyncpg URL for a specific database configuration.
        
        :param key: The database key.
        :return: Connection string.
        :raises ValueError: If the configuration for the given key is missing.
        """
        settings = cls()
        db_config = settings.DB_CONFIGS.get(key)
        if not db_config:
            raise ValueError(f"Database configuration for key '{key}' is missing.")
        return db_config.get_asyncpg_url()


class RedisSettings(CommonSettings):
    """
    Redis configuration settings.
    """
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_TIMEOUT: int


redis_settings = RedisSettings()

def load_env_vars() -> Dict[str, str]:
    """
    Load and validate required environment variables.
    
    :return: Dictionary of environment variables.
    :raises ValueError: If any required variable is missing.
    """
    env_vars = {
        "TG_BOT_API_TOKEN": os.getenv("TG_BOT_API_TOKEN"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),
        "ADMIN_ID": os.getenv("ADMIN_ID"),
    }
    
    missing_vars = [var for var, value in env_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {missing_vars}")
    
    return env_vars


env_vars = load_env_vars()

def setup_logger(name: str, log_file: str) -> logging.Logger:
    """
    Configure and return a logger with file output.
    
    :param name: Logger name.
    :param log_file: Path to the log file.
    :return: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(env_vars["LOG_LEVEL"].upper())
    
    if not logger.handlers:
        file_handler = logging.FileHandler(BASE_DIR / log_file, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
    
    return logger


bot_logger = setup_logger("bot_logger", "logs/bot_logs.log")
#fapi_logger = setup_logger("fast_api", "api/logs/api_logs.log")
