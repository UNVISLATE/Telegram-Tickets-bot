import sqlite3
from dataclasses import dataclass
from ..Logers import LoggingConfigurations

loger = LoggingConfigurations.db

@dataclass
class UserData:
    id:int
    username:str
    ticketID:int
    language:str

class User:
    def __init__(self, uid:int=None, username:str=None, ticketID:int=None):
        self.connection = sqlite3.connect("/data/database.db")
        self.uid = uid
        self.username = username
        self.ticket_id = ticketID
        self.userdata = None
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