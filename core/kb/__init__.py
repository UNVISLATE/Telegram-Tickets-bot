from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from core import SUBSCRIBE_CHAT_IDS

def hello_kb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            "💭ArayasCheats CHAT💭",
            url="https://t.me/arayas1337cheats"
        )
    ).add(
        InlineKeyboardButton(
            "📰ArayasCheats NEWS📰",
            url="https://t.me/arayascheats"
        )
    )
    return kb

def rate_support(admin_id):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            "1 ⭐️",
            callback_data=f"{admin_id}|1"
        ),
        InlineKeyboardButton(
            "2 ⭐️⭐️",
            callback_data=f"{admin_id}|2"
        )
    ).add(
        InlineKeyboardButton(
            "3 ⭐️⭐️⭐️",
            callback_data=f"{admin_id}|3"
        ),
        InlineKeyboardButton(
            "4 ⭐️⭐️⭐️⭐️",
            callback_data=f"{admin_id}|4"
        ),
        InlineKeyboardButton(
            "5 ⭐️⭐️⭐️⭐️⭐️",
            callback_data=f"{admin_id}|5"
        )
    )
    return kb