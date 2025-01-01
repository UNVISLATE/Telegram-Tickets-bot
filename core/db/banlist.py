import sqlite3
from ..Logers import LoggingConfigurations
from ..types import UserData
from ..config import APP_PATHS as PATH

logger = LoggingConfigurations.db

class BanList:
    def __init__(self):
        self.connection = sqlite3.connect(f"{PATH["data"]}database.db")