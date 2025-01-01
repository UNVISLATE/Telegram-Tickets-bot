import datetime
import sqlite3
from ..Logers import LoggingConfigurations
from ..config import APP_PATHS as PATH

logger = LoggingConfigurations.db

class AdminRate:
    def __init__(self, adminID:int, user_id:str=None):
        self.connection = sqlite3.connect(f"{PATH["data"]}database.db")
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
            logger.error(f"core.db.AdminRate.get_rates | Ошибка при получении оценок\nerror: {str(err)}")

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
            logger.error(f"core.db.AdminRate.new_rate | Ошибка при создании оценки\nerror: {str(err)}")

    def clean_all_rates(self):
        try:
            date = datetime.datetime.now()
            cursor = self.connection.cursor()
            cursor.execute(
                "DELETE FROM AdminRate"
            )
            self.connection.commit()
            cursor.close()
        except Exception as err:
            logger.error(f"core.db.AdminRate.new_rate | Ошибка при создании оценки\nerror: {str(err)}")

    def clean_rates_by_id(self, id):
        try:
            date = datetime.datetime.now()
            cursor = self.connection.cursor()
            cursor.execute(
                "DELETE FROM AdminRate WHERE id = ?", (id, )
            )
            self.connection.commit()
            cursor.close()
        except Exception as err:
            logger.error(f"core.db.AdminRate.new_rate | Ошибка при создании оценки\nerror: {str(err)}")

    def replace_rates_by_id(self, rate, id):
        try:
            date = datetime.datetime.now()
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE AdminRate SET rate = ? WHERE id = ?", (rate, id)
            )
            self.connection.commit()
            cursor.close()
        except Exception as err:
            logger.error(f"core.db.AdminRate.new_rate | Ошибка при создании оценки\nerror: {str(err)}")

    def exit(self):
        self.connection.close()