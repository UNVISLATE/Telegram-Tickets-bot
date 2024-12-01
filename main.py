import logging
import time
import uuid

import telebot as tb
from telebot.types import Message
from telebot.util import content_type_service

from core.Logers import LoggingConfigurations
from core.db import User, UserData
from core import *

from data.TEXT_MESSAGES import *

loger = LoggingConfigurations.main

bot = tb.TeleBot(TOKEN)

@bot.message_handler(commands=['start'], chat_types="private")
def start(message: Message):
    userID = message.from_user.id
    userNAME = message.from_user.username
    userLINK = f"https://t.me/{message.from_user.username}"
    userLANGUAGE = message.from_user.language_code
    userOBJ = User(userID, userNAME)
    user_data = userOBJ.set_language("ru" if userLANGUAGE == "ru" else "en")
    bot.send_message(
        userID,
        HELLO[userOBJ.userdata.language if userOBJ.userdata.language == "ru" else "en"]
    )

@bot.message_handler(
    content_types=["text", "video", "audio", "photo", "sticker", "document"],
    chat_types="private"
)
def content_user(message: Message):
    userID = message.from_user.id
    userNAME = message.from_user.username
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
            f"username: {userOBJ.userdata.username}\n"
            f"язык: {userOBJ.userdata.language}\n"
            f"=======================\n"
            f"ticketID: {userTICKET}\n\n"
            f"Для ответа пользователю пишите в этом топике(тикете).",
            message_thread_id=userTICKET
        )

    try:
        if message.content_type == "text":
            bot.send_message(GROUP_ID, message.text, message_thread_id=userTICKET)
        elif message.content_type == "video":
            bot.send_video(
                GROUP_ID,
                video=message.video.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                message_thread_id=userTICKET
            )
        elif message.content_type == "photo":
            bot.send_photo(
                GROUP_ID,
                photo=message.photo[-1].file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                message_thread_id=userTICKET
            )
        elif message.content_type == "audio":
            bot.send_audio(
                GROUP_ID,
                audio=message.audio.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                message_thread_id=userTICKET
            )
        elif message.content_type == "sticker":
            bot.send_sticker(
                GROUP_ID,
                sticker=message.sticker.file_id,
                message_thread_id=userTICKET
            )
        elif message.content_type == "document":
            bot.send_document(
                GROUP_ID,
                document=message.document.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                message_thread_id=userTICKET
            )
    except Exception as err:
        bot.send_message(message.from_user.id, "При отправке сообщения произошла непредвиденная ошибка\nсейчас вы можете написать @arayas1337 для решения вашей проблемы")
        bot.send_message(DEV, f"У пользователя @{message.from_user.username} произошла непредвиденная ошибка\nmain.content_user\nerror: {str(err)}")
        loger.error(f"Ошибка отправки сообщения \n error: {str(err)}")



@bot.message_handler(
    content_types=["location", "venue", "poll", "contact"],
    chat_types=["private", "supergroup"]
)
def not_supported(message: Message):
    messageID = message.id
    userID = message.from_user.id
    userNAME = message.from_user.username
    bot.send_message(
        userID,
        "The content type is not supported."
    )

@bot.message_handler(
    content_types=["text", "video", "audio", "photo", "sticker", "document"],
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
                if message.content_type == "text":
                    bot.send_message(userID, message.text)
                elif message.content_type == "video":
                    bot.send_video(
                        userID,
                        video=message.video.file_id,
                        caption=message.caption,
                        caption_entities=message.caption_entities
                    )
                elif message.content_type == "photo":
                    bot.send_photo(
                        userID,
                        photo=message.photo[-1].file_id,
                        caption=message.caption,
                        caption_entities=message.caption_entities
                    )
                elif message.content_type == "audio":
                    bot.send_audio(
                        userID,
                        audio=message.audio.file_id,
                        caption=message.caption,
                        caption_entities=message.caption_entities
                    )
                elif message.content_type == "sticker":
                    bot.send_sticker(
                        userID,
                        sticker=message.sticker.file_id
                    )
                elif message.content_type == "document":
                    bot.send_document(
                        userID,
                        document=message.document.file_id,
                        caption=message.caption,
                        caption_entities=message.caption_entities
                    )
            except Exception as err:
                bot.reply_to(message, "Ошибка при отправке контента пользователю. Пользователь удалил чат или заблокировал бота.")
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
                "userID для этого топика не найден.\nВероятно аккаунт был удален или топик был создан вручную"
            )
            #bot.close_forum_topic(message.chat.id, message.message_thread_id)

@bot.message_handler(content_types=content_type_service)
def sys_message_clean(message: Message):
    try:
        bot.delete_message(message.chat.id,message.message_id)
    except Exception as err:
        loger.warning(f"sys_message_clean | error: {str(err)}")

while True:
    try:
        bot.infinity_polling(
            5,
            logger_level=logging.DEBUG
        )
    except Exception as err:
        bot.send_message(DEV, f"infinity_polling.error | {str(err)}")
        time.sleep(15)