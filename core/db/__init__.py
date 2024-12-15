import datetime
import sqlite3
from dataclasses import dataclass
from uuid import uuid4
import statistics
from ..Logers import LoggingConfigurations

loger = LoggingConfigurations.db

@dataclass
class UserData:
    id:int
    username:str
    ticketID:int
    language:str

class User:
    def __init__(self, uid:int=None, username:str=None, ticketID:int=None, full_data=None):
        self.connection = sqlite3.connect("data/database.db")
        self.uid = uid
        self.username = username
        self.ticket_id = ticketID
        self.userdata = None
        self.full_data = full_data
        if self.uid is not None:
            self._get_by_uid()
        elif self.ticket_id is not None:
            self._get_by_ticket()
        else:
            loger.error('core.db.User.__init__ | A minimum of 1 parameter was expected but 0 is given')

    def _get_by_uid(self) -> UserData:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE id = ?", (self.uid, ))
        result = cursor.fetchone()
        cursor.close()
        if result:
            self.userdata = UserData(result[0], result[1], result[2], result[3])
            print(self.userdata)
        else:
            self.create()

    def _get_by_ticket(self) -> UserData:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE ticketID = ?", (int(self.ticket_id), ))
        result = cursor.fetchone()
        cursor.close()
        if result:
            self.userdata = UserData(result[0], result[1], result[2], result[3])
        else:
            self.userdata = None

    def create(self) -> UserData:
        try:
            if self.full_data is not None:
                loger.info(f"{str(self.full_data)}\n\n")
        except:
            loger.error(f"full_data log error for id: {self.uid} | username: {self.username}")
        try:
            if self.username is None:
                self.username = "NONE_USER"
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Users (ID, username, ticketID, language) VALUES (?,?,?,?)", (self.uid, self.username, -99999, "en"))
            self.connection.commit()
            cursor.close()
            self.userdata = UserData(self.uid, self.username, 0, "Not selected")
        except Exception as err:
            loger.error(f"core.db.User.create | Ошибка при создании пользователя\nerror: {str(err)}")
        return self.userdata

    def set_language(self, lang:str) -> UserData:
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE Users SET language = ? WHERE ID = ?", (lang, self.uid))
            self.connection.commit()
            cursor.close()
            self.userdata.language = lang
            return self.userdata
        except Exception as err:
            loger.error(f"core.db.User.set_language | Ошибка установки языка пользователя\nerror: {str(err)}")
            self.userdata.language = None
        return None

    def set_ticket(self, ticketID:int):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE Users SET ticketID = ? WHERE ID = ?", (ticketID, self.uid))
        self.connection.commit()
        cursor.close()

    def exit(self):
        self.connection.close()

class AdminRate:
    def __init__(self, adminID:int, user_id:str=None):
        self.connection = sqlite3.connect("data/database.db")
        self.adminID = adminID
        self.uid = user_id

    def get_rate(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM AdminRate WHERE id = ?", (self.adminID,))
            result = cursor.fetchall()
            cursor.close()
            if result:
                return result
            else:
                return None
        except Exception as err:
            loger.error(f"core.db.AdminRate.get_rates | Ошибка при получении оценок\nerror: {str(err)}")

    def new_rate(self, rate:int):
        try:
            date = datetime.datetime.now()
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO AdminRate (id, rate, date, uid) VALUES (?,?,?,?)",
                (self.adminID, rate, f"{date.day}-{date.month}-{date.year} {date.hour}:{date.minute}", self.uid)
            )
            self.connection.commit()
            cursor.close()
        except Exception as err:
            loger.error(f"core.db.AdminRate.new_rate | Ошибка при создании оценки\nerror: {str(err)}")

    def exit(self):
        self.connection.close()
