import LogManager
import json
import FileManager

log = LogManager.setName(__name__)

cartella = str(__file__).replace('ConfigManager.py', 'configFiles')
confNodo = cartella + '/nodo_Config.conf'
confDir = '/dir_Config.conf'
confFile = '/file_Config.conf'
confSafe = cartella + '/safe.conf'
safebinlist = '/sblist.conf'
# NOTAA: il file configurazione viene usato per fare il confronto con altri nodi, non gli frega se in locale hai
# fatto delle modifiche o meno


def leggiConfigFile(dirpath: str) -> list[dict]:
    """Una volta letto il file, tramite JSON ritorno una lista di dict"""
    percorso = dirpath + '/' + confFile
    toret = FileManager.leggiConfig(percorsoCompleto=percorso)
    if toret is not None:
        return json.loads(toret)
    else:
        return []


def leggiConfigDirs() -> list[dict]:
    """Una volta letto il file, tramite JSON ritorno una lista di dict"""
    toret = FileManager.leggiConfig(percorsoCompleto=confDir)
    if toret is not None:
        return json.loads(toret)
    return []


def leggiConfigNodo() -> dict:
    """Una volta letto il file, tramite JSON ritorno una lista di dict"""
    toret = FileManager.leggiConfig(percorsoCompleto=confNodo)
    if toret is not None:
        return json.loads(toret)
    return {}


def aggiornaConfigFile(dirpath: str, contenuto: list[dict]) -> bool:
    percorso = dirpath + "/" + confFile
    cont = json.dumps(obj=contenuto)
    return FileManager.scriviConfig(percorsoCompleto=percorso, contenuto=cont, hidden=True)


def aggiornaConfigDir(contenuto: list[dict]) -> bool:
    cont = json.dumps(obj=contenuto)
    return FileManager.scriviConfig(percorsoCompleto=confDir, contenuto=cont)


def aggiornaConfigNodo(contenuto: dict) -> bool:
    cont = json.dumps(obj=contenuto)
    return FileManager.scriviConfig(percorsoCompleto=confNodo, contenuto=cont)


def leggiSafeBinList(path: str) -> list[dict]:
    percorso = path + safebinlist
    toret = FileManager.leggiConfig(percorsoCompleto=percorso)
    if toret is not None:
        return json.loads(toret)
    else:
        return []


def aggiornaSafeBinList(path: str, contenuto: list[dict]) -> bool:
    cont = json.dumps(obj=contenuto)
    percorso = path + safebinlist
    return FileManager.scriviConfig(percorsoCompleto=percorso, contenuto=cont)


def leggiConfigSafeBin() -> dict:
    """Una volta letto il file, tramite JSON ritorno una lista di dict"""
    toret = FileManager.leggiConfig(percorsoCompleto=confSafe)
    if toret is not None:
        return json.loads(toret)
    else:
        return {}


def aggiornaConfigSafeBin(contenuto: dict) -> bool:
    cont = json.dumps(obj=contenuto)
    return FileManager.scriviConfig(percorsoCompleto=confSafe, contenuto=cont)

