import os

from telebot.types import Message

from core import *
from core.config import APP_PATHS as PATH
from ..Logers import LoggingConfigurations
from ..db import AdminRate
from main import bot

logger = LoggingConfigurations.main

@bot.message_handler(commands=['database', 'db'], chat_types="private")
def database(message: Message):
    if str(message.from_user.id) == str(DEV) or str(message.from_user.id) == "5469853944": #UNVI or Arayas1337
        with open("/data/database.db", "rb") as database_file:
            bot.send_document(
                DEV,
                database_file
            )

@bot.message_handler(commands=['log', 'logs'], chat_types="private")
def database(message: Message):
    if str(message.from_user.id) == str(DEV):
        log_files = [file for file in os.listdir(PATH["logs"]) if file.endswith('.log')]
        for log_file in log_files:
            with open(f"{PATH["logs"]}{log_file}", "rb") as dlog_file:
                bot.send_document(
                    DEV,
                    dlog_file
                )

@bot.message_handler(commands=['set_rate'], chat_types=["supergroup", "private"])
def set_rates(message: Message):
    if int(message.from_user.id) == int(DEV):
        Rates = AdminRate(message.from_user.id)
        try:
            admin_id = message.text.split(" ")[1]
            setup_rate = message.text.split(" ")[2]
            Rates.replace_rates_by_id(setup_rate, admin_id)
            bot.send_message(DEV, "Рейтинг успешно установлен")
        except Exception as err:
            logger.error(f"Ошибка установки рейтинга \n error: {str(err)}")
        Rates.exit()


@bot.message_handler(commands=['clean_all_rates', 'clean_rates'], chat_types=["supergroup", "private"])
def clean_all_rates(message: Message):
    if int(message.from_user.id) == int(DEV):
        Rates = AdminRate(message.from_user.id)
        try:
            Rates.clean_all_rates()
            bot.send_message(DEV, "Рейтинг успешно очищен")
        except Exception as err:
            logger.error(f"Ошибка очистки рейтинга \n error: {str(err)}")
        Rates.exit()