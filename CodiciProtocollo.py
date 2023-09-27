from enum import Enum


class Codice(Enum):
    """Richiesta completata -> stesso codice inviato AS codice risposta"""
    REQUEST_BANNER = 10,  # x il sistema
    REQUEST_LIST_DIRS = 12,  # config
    REQUEST_DIR = 14,  # config
    REQUEST_FILE = 16,  # config
    GET_FILE = 20,  # FILE EFFETTIVO
    PUSH_UPDATE = 22,
    FORCE_UPDATE = 25,
    ERR_UNKNOWN = 30,  # IDK
    ERR_PERMISSION = 32,  # non ho i permessi per darti questo file
    ERR_404 = 34,  # file non trovato
    ERR_BUSY = 36,  # file occupato, retry
    WET_PAPER = 99  # PROTOCOLLO CARTA BAGNATA - CHIUDERE LA LIBRERIA
