from LogManager import logger as log
import json
import Nodo


def getNodo() -> Nodo.Nodo | None:
    try:
        f = open('configFile/nodo.conf', 'r')
        tmp = json.load(f)
        if isinstance(tmp, list):
            log.error("File config Nodo e' una lista e non un dict! -" + str(type(tmp)))
        # todo: verifica validità dell'oggetto json prima di andare a prendere queste info
        a = Nodo.Nodo(nome=tmp.nome, idn=tmp.idNodo, sbpath=tmp.safeBinPath, dirlist=tmp.dirList,
                         nodi=tmp.nodiList)
        if a.isValid() is False:
            log.error("Errore caricamento Nodo da file config - invalid obj")
            return None
        # todo: verifica che l'oggetto venga creato bene prima di ritornare, altrimenti do un errore o None o altro
        return a
    except Exception as e:
        log.warning(f'Errore apertura file config nodo - {e}')


def leggiConfigDirFiles(dirpath) -> list:
    """Una volta letto il file, tramite JSON ritorno una lista di dict"""
    return []

