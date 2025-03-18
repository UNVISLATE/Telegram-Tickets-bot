import statistics

from telebot.types import Message, ReactionTypeEmoji

import core.markups
from core import *
from core.Logers import LoggingConfigurations
from core.db import User, AdminRate, BlackList
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

@bot.message_handler(commands=['rate_ping'], chat_types="supergroup")
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

@bot.message_handler(commands=['rate_history'], chat_types=["supergroup", "private"])
def rate_history(message: Message):
    Rates = AdminRate(message.from_user.id)
    my_rates_list = Rates.get_rate()
    if my_rates_list is not None:
        rates_list_msg = ""
        rate_num = 0
        for rate_data in reversed(my_rates_list):
            if rate_num < 10:
                rates_list_msg += (
                    f"UID: {rate_data[3]}\n"
                    f"date: {rate_data[2]}\n"
                    f"rate: {rate_data[1]}\n"
                    f"============\n"
                )
            rate_num += 1
        rates_list_msg += f"0-10/{rate_num}"
        my_rates_list = [rate_obj[1] for rate_obj in my_rates_list]
        average_rating = statistics.mean(my_rates_list)
        bot.send_message(message.chat.id, rates_list_msg,message_thread_id=message.message_thread_id)
        bot.send_message(message.chat.id, f"Ваш рейтинг: {round(average_rating, 1)}", message_thread_id=message.message_thread_id)
    else:
        bot.send_message(message.chat.id, "Оценок не найдено.", message_thread_id=message.message_thread_id)
    Rates.exit()

@bot.message_handler(commands=['ban'], chat_types=["supergroup"])
def ban_user(message: Message):
    messageID = message.id
    adminID = message.from_user.id
    adminNAME = message.from_user.username
    if GROUP_ID == int(message.chat.id) and message.is_topic_message is not None:
        ticketID = message.message_thread_id
        userD = User(ticketID=ticketID)
        if userD.userdata is not None:
            if int(userD.userdata.id) in [1281134018, 5469853944]:
                bot.reply_to(message, "Дохуя без смертный? пизды дать?")
            else:
                if BlackList().add_to_blacklist(int(userD.userdata.id), adminNAME, ""):
                    bot.reply_to(message, "Пользователь успешно заблокирован.")
                else:
                    bot.reply_to(message, "Ошибка блокировки пользователя... он что безсмертный?")
        else:
            bot.reply_to(message, "userID для этого топика не найден.")
        userD.exit()

@bot.message_handler(commands=['unban'], chat_types=["supergroup"])
def unban_user(message: Message):
    messageID = message.id
    adminID = message.from_user.id
    adminNAME = message.from_user.username
    if GROUP_ID == int(message.chat.id) and message.is_topic_message is not None:
        ticketID = message.message_thread_id
        userD = User(ticketID=ticketID)
        if userD.userdata is not None:
            if int(userD.userdata.id) in [1281134018, 5469853944]:
                bot.reply_to(message, "Бог есть бог, его не заблокировать поэтому и разблокировать не надо :з")
            else:
                if BlackList().remove_from_blacklist(int(userD.userdata.id)):
                    bot.reply_to(message, "Пользователь успешно разблокирован.")
                else:
                    bot.reply_to(message, "Ошибка разблокировки пользователя... не судьба :з")
        else:
            bot.reply_to(message, "userID для этого топика не найден.")
        userD.exit()