import logging
from time import sleep

import telebot as tb

from core import *
from core.Logers import LoggingConfigurations
from core.db import setup_database

logger = LoggingConfigurations.main
bot = tb.TeleBot(TOKEN)

from core.handlers import *

setup_database()

def run():
    try:
        bot.infinity_polling(
            timeout=5,
            long_polling_timeout=20,
            logger_level=logging.INFO
        )
    except Exception as err:
        logger.error(f"infinity_polling.error | {str(err)}")
        sleep(15)

if __name__ == '__main__':
    run()