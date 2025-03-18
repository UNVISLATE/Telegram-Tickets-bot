import datetime
import sqlite3
from ..Logers import LoggingConfigurations
from ..config import APP_PATHS as PATH

logger = LoggingConfigurations.db

class AdminRateForUpdate:
    def __init__(self, adminID: int, user_id: str = None):
        """
        Инициализация класса AdminRate.
        :param adminID: ID администратора.
        :param user_id: ID пользователя (опционально).
        """
        self.db_path = f"{PATH["data"]}database.db"
        self.adminID = adminID
        self.uid = user_id

    def _execute_query(self, query: str, params: tuple = None):
        """
        Выполняет SQL-запрос с использованием контекстного менеджера.
        :param query: SQL-запрос.
        :param params: Параметры для запроса.
        :return: Результат выполнения запроса.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                result = cursor.fetchall()
                conn.commit()
                return result
        except Exception as err:
            logger.error(f"Ошибка при выполнении запроса: {query}\nОшибка: {str(err)}")
            raise

    def get_rate(self):
        """
        Получает все оценки для указанного администратора.
        :return: Список кортежей с данными или None, если записей нет.
        """
        query = "SELECT * FROM AdminRate WHERE id = ?"
        result = self._execute_query(query, (self.adminID,))
        return result if result else None

    def new_rate(self, rate: int):
        """
        Добавляет новую оценку для администратора.
        :param rate: Оценка (целое число).
        """
        if not isinstance(rate, int):
            raise ValueError("Оценка должна быть целым числом.")

        date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        query = "INSERT INTO AdminRate (id, rate, date, uid) VALUES (?, ?, ?, ?)"
        self._execute_query(query, (self.adminID, rate, date, self.uid))

    def clean_all_rates(self):
        """
        Удаляет все записи из таблицы AdminRate.
        """
        query = "DELETE FROM AdminRate"
        self._execute_query(query)

    def clean_rates_by_id(self, admin_id: int):
        """
        Удаляет записи по ID администратора.
        :param admin_id: ID администратора.
        """
        query = "DELETE FROM AdminRate WHERE id = ?"
        self._execute_query(query, (admin_id,))

    def replace_rates_by_id(self, rate: int, admin_id: int):
        """
        Обновляет оценку для указанного администратора.
        :param rate: Новая оценка.
        :param admin_id: ID администратора.
        """
        if not isinstance(rate, int):
            raise ValueError("Оценка должна быть целым числом.")

        query = "UPDATE AdminRate SET rate = ? WHERE id = ?"
        self._execute_query(query, (rate, admin_id))

    def __del__(self):
        """
        Закрывает соединение с базой данных при удалении объекта.
        """
        try:
            if hasattr(self, "connection"):
                self.connection.close()
        except Exception as err:
            logger.error(f"Ошибка при закрытии соединения: {str(err)}")

    def exit(self):
        self.__del__()


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