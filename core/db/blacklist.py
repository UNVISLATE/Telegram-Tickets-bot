import sqlite3
from ..Logers import LoggingConfigurations
from ..types import UserData
from ..config import APP_PATHS as PATH

logger = LoggingConfigurations.db

import sqlite3

class BlackList:
    def __init__(self):
        """
        Инициализация менеджера черного списка.
        """
        self.db_path = f"{PATH["data"]}database.db"

    def is_blacklisted(self, user_id):
        """
        Проверяет, находится ли пользователь в черном списке.
        :param user_id: ID пользователя.
        :return: True, если пользователь в черном списке, иначе False.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM BlackList WHERE ID = ?", (user_id,))
            return cursor.fetchone() is not None

    def get_blacklist_entry(self, user_id):
        """
        Получает запись из черного списка.
        :param user_id: ID пользователя.
        :return: Кортеж (AddedBy, Reason), если пользователь найден, иначе None.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT AddedBy, Reason FROM BlackList WHERE ID = ?", (user_id,))
            return cursor.fetchone()

    def add_to_blacklist(self, user_id, added_by, reason):
        """
        Добавляет пользователя в черный список.
        :param user_id: ID пользователя.
        :param added_by: ID администратора, который добавил пользователя.
        :param reason: Причина блокировки.
        :return: True, если пользователь успешно добавлен, иначе False.
        """
        if self.is_blacklisted(user_id):
            print(f"Пользователь с ID {user_id} уже в черном списке.")
            return False

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO BlackList (ID, AddedBy, Reason) VALUES (?, ?, ?)", (user_id, added_by, reason))
            conn.commit()
            print(f"Пользователь с ID {user_id} добавлен в черный список.")
            return True

    def remove_from_blacklist(self, user_id):
        """
        Удаляет пользователя из черного списка.
        :param user_id: ID пользователя.
        :return: True, если пользователь успешно удален, иначе False.
        """
        if not self.is_blacklisted(user_id):
            print(f"Пользователь с ID {user_id} не найден в черном списке.")
            return False

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM BlackList WHERE ID = ?", (user_id,))
            conn.commit()
            print(f"Пользователь с ID {user_id} удален из черного списка.")
            return True

    def list_all_blacklisted_users(self):
        """
        Возвращает список всех пользователей в черном списке.
        :return: Список кортежей (ID, AddedBy, Reason).
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ID, AddedBy, Reason FROM BlackList")
            return cursor.fetchall()

