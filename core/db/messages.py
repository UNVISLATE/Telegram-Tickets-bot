import datetime
import sqlite3
from dataclasses import dataclass
from uuid import uuid4
import statistics
from telebot.types import Message, MessageID
from ..Logers import LoggingConfigurations
from ..types import AppMessage
from ..config import APP_PATHS as PATH

logger = LoggingConfigurations.db

class Messages:
    def __init__(self, message:AppMessage=None):
        self.connection = sqlite3.connect(f"{PATH["data"]}database.db")
        self.message = message

    def add(self):
        if self.message is not None:
            try:
                message = self.message.Message
                user_id = self.message.MessageFromID
                ticket_id = self.message.TicketID
                msg_id = self.message.TicketMessageID

                cursor = self.connection.cursor()
                cursor.execute(
                    "INSERT INTO Messages (ID, ticketID, content, date, uid) VALUES (?,?,?,?,?)",
                    (
                        msg_id.message_id,
                        ticket_id,
                        message.text if message.content_type == "text" else message.content_type,
                        message.date.real,
                        user_id
                    )
                )
                self.connection.commit()
                cursor.close()
            except Exception as err:
                logger.error(f"Ошибка добавления информации о сообщении\nerror: {str(err)}")
        else:
            logger.warning(f"Попытка добавить сообщение без информации.")

    def exit(self):
        self.connection.close()
