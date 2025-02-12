from dotenv import load_dotenv
import logging
import os
 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def loger_setup(logger_name, logger_file):
    level = env_vars["LOG_LEVEL"]

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    if not logger.handlers:
        file_handler = logging.FileHandler(logger_file, encoding="utf-8")
        formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formater)

        logger.addHandler(file_handler)
    return logger

bot_logger = loger_setup('bot_logger', 'tg_bot/logs/bot_logs.log')
fapi_logger = loger_setup('fast_api', 'api/logs/api_logs.log')

def load_env_vars():
    load_dotenv()
    env_vars = {
        "TG_BOT_API_KEY": os.getenv("TG_BOT_API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL")
    }
    
    missing_vars = [var for var, value in env_vars.items() if not value]

    if missing_vars:
        raise ValueError(f"Не найдены env_vars в файле .env - {missing_vars}")
    
    return env_vars

env_vars = load_env_vars()

