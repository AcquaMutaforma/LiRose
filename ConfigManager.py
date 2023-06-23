from LogManager import logger as log
import json
import Nodo


def getNodo() -> Nodo.Nodo:
    try:
        f = open('configFile/nodo.conf', 'r')
        tmp = json.load(f)
        return Nodo.Nodo(tmp.nome, tmp.idNodo, tmp.safeBinPath, tmp.dirList)
    except Exception as e:
        log.warning(f'Errore apertura file config nodo - {e}')
