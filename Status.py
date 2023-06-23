from enum import Enum


class Stato(Enum):
    OK = 1
    ADDED_FILE = 2
    REMOVED_FILE = 3
    Conf_404 = 4
    ERR_CONFIG = 5
