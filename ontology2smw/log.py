import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime


def log(_dir, filename):
    """
    Simple logger object.
    Logs Installation loop.py actions
    """
    logger = logging.getLogger('Ontology 2 SMW import script')
    log_format = logging.Formatter('%(asctime)-15s %(message)s')
    log_path = _dir + filename  # prepend "/" to filename
    log_handler = RotatingFileHandler(filename=log_path,
                                      maxBytes=2000000,
                                      backupCount=4)  # 2Mb log file
    log_handler.setFormatter(log_format)
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)
    return logger


logs_dir_str = 'logs/'
_dir = Path(logs_dir_str)  # os.path.dirname(os.path.abspath(__file__))
if not _dir.is_dir():
    os.mkdir(path=logs_dir_str, mode=0o777)
now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
logger = log(_dir=logs_dir_str,
             filename=f"ontology2smw_{now}.log")
