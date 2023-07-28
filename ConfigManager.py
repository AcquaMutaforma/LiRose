import LogManager
import json
import FileManager

log = LogManager.setName(__name__)

cartella = str(__file__).replace('ConfigManager.py', 'configFiles')
confNodo = '/nodo_Config.conf'
confDir = '/dir_Config.conf'
confFile = '/file_Config.conf'
# NOTAA: il file configurazione viene usato per fare il confronto con altri nodi, non gli frega se in locale hai
# fatto delle modifiche o meno


def leggiConfigFile(dirpath: str) -> list[dict] | None:
    """Una volta letto il file, tramite JSON ritorno una lista di dict"""
    percorso = dirpath + confFile
    toret = FileManager.leggiConfig(percorsoCompleto=percorso)
    if toret is not None:
        return json.loads(toret)
    else:
        return None


def leggiConfigDirs() -> list[dict] | None:
    """Una volta letto il file, tramite JSON ritorno una lista di dict"""
    toret = FileManager.leggiConfig(percorsoCompleto=confDir)
    if toret is not None:
        return json.loads(toret)
    return None


def leggiConfigNodo() -> dict | None:
    """Una volta letto il file, tramite JSON ritorno una lista di dict"""
    toret = FileManager.leggiConfig(percorsoCompleto=confNodo)
    if toret is not None:
        return json.loads(toret)
    return None


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
