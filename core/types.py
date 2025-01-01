from dataclasses import dataclass
from telebot.types import MessageID, Message

@dataclass
class UserData:
    id:int
    username:str
    ticketID:int
    language:str

@dataclass
class AppMessage:
    TicketID:int
    Message:Message
    TicketMessageID:MessageID
    MessageFromID:int