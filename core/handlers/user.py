from telebot.types import Message

import core.markups
from core.Logers import LoggingConfigurations
from core.db import User
from data.TEXT_MESSAGES import *
from main import bot

logger = LoggingConfigurations.main

@bot.message_handler(commands=['start'], chat_types="private")
def start(message: Message):
    user_id = int(message.from_user.id)
    userNAME = message.from_user.username
    if userNAME is None:
        userNAME = message.from_user.full_name
    userLINK = f"https://t.me/{message.from_user.username}"
    userLANGUAGE = message.from_user.language_code
    userOBJ = User(user_id, userNAME, full_data=message)
    user_data = userOBJ.set_language("ru" if userLANGUAGE == "ru" else "en")
    bot.send_message(
        user_id,
        HELLO[userOBJ.userdata.language if userOBJ.userdata.language == "ru" else "en"],
        reply_markup=core.markups.hello_kb()
    )
    userOBJ.exit()