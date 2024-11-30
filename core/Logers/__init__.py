from dataclasses import dataclass
import logging
import uuid

def _logger_setup(filename:str, level=logging.INFO):
    filename = f"/data/logs/{filename}"
    filename = filename if filename.endswith(".log") else f"{filename}.log"
    loger = logging.getLogger(str(uuid.uuid4()))
    formatter = logging.Formatter("%(asctime)s | %(levelname)s - %(message)s")
    fileHandler = logging.FileHandler(filename, mode='a')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    loger.setLevel(level)
    loger.addHandler(fileHandler)
    loger.addHandler(streamHandler)
    return loger

@dataclass
class LoggingConfigurations:
    main = _logger_setup("main", level=logging.INFO)
    db = _logger_setup("db", level=logging.INFO)
