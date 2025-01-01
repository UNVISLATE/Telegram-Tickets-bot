import sqlite3
from ..config import APP_PATHS as PATH
from ..Logers import LoggingConfigurations
from ..exceptions import SetupError

logger = LoggingConfigurations.critical

def setup_database():
    try:
        with sqlite3.connect(f"{PATH["data"]}database.db") as connection:
            with open(f"{PATH["data"]}setup.sql") as sqlfile:
                script = sqlfile.read()
            connection.executescript(script)
            connection.commit()
    except sqlite3.DatabaseError as err:
        logger.critical(f"DatabaseError: {str(err)}", exc_info=err)
        raise SetupError("DatabaseSetup Error check tracback for details | saved (critical.log)") from err
    except Exception as err:
        logger.critical(f"Exception: {str(err)}", exc_info=err)
        raise SetupError("DatabaseSetup Error check tracback for details | saved (critical.log)") from err

