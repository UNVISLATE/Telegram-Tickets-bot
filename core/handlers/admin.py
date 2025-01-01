import statistics

from telebot.types import Message, ReactionTypeEmoji

import core.markups
from core import *
from core.Logers import LoggingConfigurations
from core.db import User, AdminRate
from main import bot

logger = LoggingConfigurations.main

@bot.message_handler(commands=['local', 'l', 'loc'], chat_types="supergroup")
def local(message: Message):
    bot.set_message_reaction(GROUP_ID, message.message_id, [ReactionTypeEmoji('😴')], is_big=False)


@bot.message_handler(commands=['info'], chat_types="supergroup")
def my_info(message: Message):
    bot.send_message(
        message.chat.id,
        f"Информация о вас:\n"
        f"ID: {message.from_user.id}\n"
        f"username: @{message.from_user.username}\n"
        f"fullname: {message.from_user.full_name}\n"
        f"language: {message.from_user.language_code}\n"
        f"premium: {message.from_user.is_premium}\n",
        message_thread_id=message.message_thread_id
    )
    my_rate(message=message)

@bot.message_handler(commands=['my_rate', 'rate_info', 'rating'], chat_types=["supergroup", "private"])
def my_rate(message: Message):
    Rates = AdminRate(message.from_user.id)
    my_rates_list = Rates.get_rate()
    if my_rates_list is not None:
        my_rates_list = [rate_obj[1] for rate_obj in my_rates_list]
        average_rating = statistics.mean(my_rates_list)
        bot.send_message(message.chat.id, f"Ваш рейтинг: {round(average_rating, 1)}", message_thread_id=message.message_thread_id)
    else:
        bot.send_message(message.chat.id, "Оценок не найдено.", message_thread_id=message.message_thread_id)
    Rates.exit()

@bot.message_handler(commands=['rate'], chat_types="supergroup")
def rate(message: Message):
    messageID = message.id
    adminID = message.from_user.id
    adminNAME = message.from_user.username
    if GROUP_ID == int(message.chat.id) and message.is_topic_message is not None:
        ticketID = message.message_thread_id
        userD = User(ticketID=ticketID)
        if userD.userdata is not None:
            try:
                userID = userD.userdata.id
                bot.send_message(
                    userID,
                    "Оцените работу поддержки от 1 до 5:",
                    reply_markup=core.markups.rate_support(adminID)
                )
                bot.send_message(GROUP_ID, "Диалог оценки успешно отправлен", message_thread_id=message.message_thread_id)
            except Exception as err:
                bot.reply_to(message, "Ошибка при отправке диалога оценки.")
                logger.error(f"Ошибка отправки диалога оценки \n error: {str(err)}")
        else:
            bot.reply_to(message,"userID для этого топика не найден.")
        userD.exit()