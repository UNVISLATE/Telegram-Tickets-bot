import uuid

from telebot.types import Message
from telebot.util import content_type_service, content_type_media

from core import *
from data.TEXT_MESSAGES import *
from main import bot
from ..Logers import LoggingConfigurations
from ..db import User, Messages, BlackList
from ..types import AppMessage
from ..markups import rate_support

logger = LoggingConfigurations.main

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

    # blacklist check
    if BlackList().is_blacklisted(userID):
        ban_info = BlackList().get_blacklist_entry(userID)
        bot.send_message(
            message.from_user.id,
            f"Вы были заблокированы администратором {ban_info[0]}\nВам отказано в предоставлении поддержки."
        )
    else:
        try:
            bot.edit_forum_topic(
                chat_id=GROUP_ID,
                message_thread_id=str(userTICKET),
                name=f"{userNAME} | {str(uuid.uuid4())[:13]}"
            )
            # костыль для проверки существует ли топик ??
            # Telegram Bot API не позволяет на данный момент адекватно проверить существует ли топик
        except:
            forum_topic = bot.create_forum_topic(GROUP_ID, userNAME)
            userOBJ.set_ticket(forum_topic.message_thread_id)
            userTICKET = forum_topic.message_thread_id
            bot.send_message(message.from_user.id, CREATED[userOBJ.userdata.language])
            bot.send_message(
                GROUP_ID,
                f"Создан тикет {userTICKET}:\n"
                f"userID: {userOBJ.userdata.id}\n"
                f"username: @{userOBJ.userdata.username}\n"
                f"язык: {userOBJ.userdata.language}\n"
                f"=======================\n"
                f"ticketID: {userTICKET}",
                message_thread_id=userTICKET
            )
        try:
            msgid = bot.copy_message(GROUP_ID, message.chat.id, message.message_id, message_thread_id=userTICKET)
            msgDB = Messages(AppMessage(int(userTICKET), message, msgid, message.from_user.id))
            msgDB.add()
            msgDB.exit()
        except Exception as err:
            bot.send_message(
                GROUP_ID,
                f"У пользователя произошла ошибка при отправке сообщения",
                message_thread_id=userTICKET
            )
            bot.send_message(message.from_user.id, "При отправке сообщения произошла непредвиденная ошибка\nпопробуйте снова или напишите @arayas1337")
            bot.send_message(DEV, f"У пользователя @{message.from_user.username} произошла непредвиденная ошибка\nmain.content_user\nerror: {str(err)}")
            logger.error(f"Ошибка отправки сообщения \n error: {str(err)}")
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
                if message.content_type == "text":
                    msg = bot.send_message(userID, f"администратор {adminNAME} пишет:\n{message.text}")
                    msgDB = Messages(AppMessage(message.message_thread_id, message, message, message.from_user.id))
                    msgDB.add()
                    msgDB.exit()
                else:
                    bot.copy_message(userID, GROUP_ID, message.message_id)
            except Exception as err:
                if "bot was blocked by the user" in str(err):
                    bot.reply_to(message, "Пользователь заблокировал бота.\nМожете удалять тикет.")
                    bot.close_forum_topic(GROUP_ID, message.message_thread_id)
                elif "user is deactivated" in str(err):
                    bot.reply_to(message, "Аккаунт пользователя был заблокирован, помянем.\nМожете удалять тикет.")
                    bot.close_forum_topic(GROUP_ID, message.message_thread_id)
                else:
                    bot.reply_to(message, "Ошибка при отправке контента пользователю.")
                    bot.send_message(
                        DEV,
                        f"У администратора @{message.from_user.username} произошла непредвиденная ошибка\n"
                        f"main.content_user\n"
                        f"error: {str(err)}"
                    )
                    logger.error(f"Ошибка отправки сообщения \n error: {str(err)}")
        else:
            bot.reply_to(
                message,
                "userID для этого топика не найден."
            )
            #bot.close_forum_topic(message.chat.id, message.message_thread_id)
        userD.exit()

@bot.message_handler(content_types="forum_topic_closed")
def delete_topic_remote(message: Message):
    try:
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
                        reply_markup=rate_support(adminID)
                    )
                    bot.delete_forum_topic(GROUP_ID, message.message_thread_id)
                except Exception as err:
                    bot.reply_to(message, "Ошибка при отправке диалога оценки.")
                    logger.error(f"Ошибка отправки диалога оценки \n error: {str(err)}")
            else:
                bot.reply_to(message, "userID для этого топика не найден.")
            userD.exit()
    except Exception as err:
        bot.delete_forum_topic(GROUP_ID, message.message_thread_id)
        logger.error(f"close_topic_error-topic deleted: {str(err)}")

@bot.message_handler(content_types=content_type_service)
def sys_message_clean(message: Message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass



content_type_services = [
    'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo',
    'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'message_auto_delete_timer_changed',
    'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message', 'users_shared', 'chat_shared',
    'write_access_allowed', 'proximity_alert_triggered', 'forum_topic_created', 'forum_topic_edited',
    'forum_topic_closed', 'forum_topic_reopened', 'general_forum_topic_hidden', 'general_forum_topic_unhidden',
    'giveaway_created', 'giveaway', 'giveaway_winners', 'giveaway_completed', 'video_chat_scheduled',
    'video_chat_started', 'video_chat_ended', 'video_chat_participants_invited',
]