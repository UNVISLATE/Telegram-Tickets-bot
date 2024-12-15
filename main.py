import logging
import time
import uuid
import statistics

import telebot as tb
import telebot.types
from telebot.types import Message, ReactionTypeEmoji
from telebot.util import content_type_service, content_type_media, update_types

import core.kb
from core.Logers import LoggingConfigurations
from core.db import User, UserData, AdminRate

from core import *
from core.messages import send_message

from data.TEXT_MESSAGES import *

loger = LoggingConfigurations.main

bot = tb.TeleBot(TOKEN)

@bot.message_handler(commands=['start'], chat_types="private")
def start(message: Message):
    userID = int(message.from_user.id)
    userNAME = f"@{message.from_user.username}"
    if userNAME is None:
        userNAME = message.from_user.full_name
    userLINK = f"https://t.me/{message.from_user.username}"
    userLANGUAGE = message.from_user.language_code
    userOBJ = User(userID, userNAME, full_data=message)
    user_data = userOBJ.set_language("ru" if userLANGUAGE == "ru" else "en")
    bot.send_message(
        userID,
        HELLO[userOBJ.userdata.language if userOBJ.userdata.language == "ru" else "en"],
        reply_markup=core.kb.hello_kb()
    )
    userOBJ.exit()

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

@bot.message_handler(commands=['my_rate', 'rate_info', 'rating', 'my'], chat_types="supergroup")
def my_rate(message: Message):
    Rates = AdminRate(message.from_user.id)
    my_rates_list = Rates.get_rate()
    if my_rates_list is not None:
        my_rates_list = [rate_obj[1] for rate_obj in my_rates_list]
        average_rating = statistics.mean(my_rates_list)
        bot.send_message(message.chat.id, f"Ваш рейтинг: {round(average_rating, 1)}", message_thread_id=message.message_thread_id)
    else:
        bot.send_message(message.chat.id, "Оценок не найдено.", message_thread_id=message.message_thread_id)


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
                    reply_markup=core.kb.rate_support(adminID)
                )
                bot.send_message(GROUP_ID, "Диалог оценки успешно отправлен", message_thread_id=message.message_thread_id)
            except Exception as err:
                bot.reply_to(message, "Ошибка при отправке диалога оценки.")
                loger.error(f"Ошибка отправки диалога оценки \n error: {str(err)}")
        else:
            bot.reply_to(message,"userID для этого топика не найден.")
        userD.exit()


@bot.message_handler(
    content_types=content_type_media,
    chat_types="private"
)
def content_user(message: Message):
    userID = message.from_user.id
    userNAME = message.from_user.username
    if userNAME is None:
        userNAME = message.from_user.full_name
    userLANGUAGE = message.from_user.language_code
    contentTYPE = message.content_type
    userOBJ = User(userID, userNAME)
    userTICKET = userOBJ.userdata.ticketID
    try:
        bot.edit_forum_topic(
            chat_id=GROUP_ID,
            message_thread_id=str(userTICKET),
            name=f"{userNAME} | {str(uuid.uuid4())[:13]}"
        )
        # костыль для проверки существует ли топик ?? для удаления сис сообщения о переименовании 175-177 ??
        # Telegram Bot API не позволяет на данный момент адекватно проверить существует ли топик
    except:
        forum_topic = bot.create_forum_topic(GROUP_ID, userNAME)
        userOBJ.set_ticket(forum_topic.message_thread_id)
        userTICKET = forum_topic.message_thread_id
        bot.send_message(message.from_user.id, CREATED[userOBJ.userdata.language])
        bot.send_message(
            GROUP_ID,
            f"Создан тикет для:\n"
            f"userID: {userOBJ.userdata.id}\n"
            f"username: @{userOBJ.userdata.username}\n"
            f"язык: {userOBJ.userdata.language}\n"
            f"=======================\n"
            f"ticketID: {userTICKET}\n\n"
            f"Для ответа пользователю пишите в этом топике(тикете).",
            message_thread_id=userTICKET
        )
    try:
        bot.copy_message(GROUP_ID, message.chat.id, message.message_id, message_thread_id=userTICKET)
    except Exception as err:
        bot.send_message(
            GROUP_ID,
            f"У пользователя произошла ошибка при отправке сообщения",
            message_thread_id=userTICKET
        )
        bot.send_message(message.from_user.id, "При отправке сообщения произошла непредвиденная ошибка\nпопробуйте снова или напишите @arayas1337")
        bot.send_message(DEV, f"У пользователя @{message.from_user.username} произошла непредвиденная ошибка\nmain.content_user\nerror: {str(err)}")
        loger.error(f"Ошибка отправки сообщения \n error: {str(err)}")
    loger.info(f"сообщение от пользователя: uid: {userID} | username: {userNAME} | [{message.text if message.content_type == "text" else message.content_type}]")
    userOBJ.exit()

@bot.message_handler(
    content_types=content_type_media,
    chat_types=["supergroup"]
)
def content_admin(message: Message):
    messageID = message.id
    adminID = message.from_user.id
    adminNAME = message.from_user.username
    if GROUP_ID == int(message.chat.id) and message.is_topic_message is not None:
        ticketID = message.message_thread_id
        userD = User(ticketID=ticketID)
        if userD.userdata is not None:
            try:
                userID = userD.userdata.id
                send_message(bot, message, userID, adminNAME)
            except Exception as err:
                bot.reply_to(message, "Ошибка при отправке контента пользователю.")
                bot.send_message(
                    DEV,
                    f"У администратора @{message.from_user.username} произошла непредвиденная ошибка\n"
                    f"main.content_user\n"
                    f"error: {str(err)}"
                )
                loger.error(f"Ошибка отправки сообщения \n error: {str(err)}")
        else:
            bot.reply_to(
                message,
                "userID для этого топика не найден."
            )
            #bot.close_forum_topic(message.chat.id, message.message_thread_id)
        userD.exit()

@bot.message_handler(content_types=content_type_service)
def sys_message_clean(message: Message):
    try:
        bot.delete_message(message.chat.id,message.message_id)
    except Exception as err:
        pass
        #loger.warning(f"sys_message_clean | error: {str(err)}")

@bot.callback_query_handler(func=lambda call: True)
def rate_callback(call: telebot.types.CallbackQuery):
    bot.delete_message(call.from_user.id, call.message.message_id)
    data = str(call.data)
    data = data.split('|')
    admin_id = data[0]
    rate = int(data[1])
    rate_mark = "⭐️"*rate
    user_id = call.from_user.id
    """
    if user_id == admin_id:
        bot.send_message(call.from_user.id, "Вы не можете оценить сами себя\nXD")
    """
    Rate = AdminRate(admin_id, user_id)
    Rate.new_rate(rate)
    Rate.exit()
    bot.send_message(GROUP_ID, f"администратор {admin_id} был оценен: {rate_mark} | {rate}/5")
    if rate == 5:
        bot.send_message(
            call.from_user.id,
            f"""
            Большое спасибо за то, что оценили нашу поддержку!
            
Мы очень рады, что вам понравился наш сервис. Если у вас возникнут какие-либо вопросы или проблемы в будущем, обращайтесь без колебаний! 😊

С уважением,
Ваша команда поддержки arayas-cheats.com
            """)
    else:
        bot.send_message(
            call.from_user.id,
            f"""
            Нам очень жаль, что вы остались не полностью довольны нашим сервисом. 
            
Мы ценим вашу обратную связь и постараемся сделать все возможное, чтобы улучшить наши услуги.

С уважением,
Ваша команда поддержки arayas-cheats.com
            """)


while True:
    try:
        bot.infinity_polling(
            5,
            logger_level=logging.DEBUG
        )
    except Exception as err:
        bot.send_message(DEV, f"infinity_polling.error | {str(err)}")
        time.sleep(15)