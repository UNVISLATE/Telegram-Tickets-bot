from telebot.types import CallbackQuery

from core import *
from core.Logers import LoggingConfigurations
from core.db import AdminRate
from main import bot

logger = LoggingConfigurations.main

@bot.callback_query_handler(func=lambda call: True)
def rate_callback(call: CallbackQuery):
    bot.delete_message(call.from_user.id, call.message.message_id)
    data = str(call.data)
    data = data.split('|')
    admin_id = data[0]
    rate = int(data[1])
    rate_mark = "⭐️" * rate
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