import LogManager
import json
import subprocess  # per creare files invisibili in windows :<
import os

log = LogManager.setName(__name__)

cartellaConfig = str(__file__).replace('ConfigManager.py', 'configFiles')
confNodo = cartellaConfig + '/nodo.conf'
confFile = '/files.conf'
confSafe = '/safe.conf'
safebinlist = '/sblist.conf'
# NOTAA: i files configurazione viene usato per fare il confronto con altri nodi, non gli frega se in locale hai
# fatto delle modifiche o meno


cartella_configFiles = 'configFiles'
# cartella_keys = 'keys'


def creaCartella(percorso: str) -> bool:
    try:
        os.mkdir(path=percorso)
        return True
    except PermissionError as e:
        log.error(f"Creazione cartella [{percorso}] Fallita - {e}")
    except FileExistsError as e:
        log.warning(f"Creazione cartella [{percorso}] Fallita - {e}")
    return False


def verificaComponentiAvvio():
    percorsoBase = str(__file__).removesuffix('FileManager.py')
    cartelle = [
        percorsoBase + cartella_configFiles,
        #percorsoBase + cartella_keys,
        percorsoBase + LogManager.cartella_logs,
        #percorsoBase + SafeBinManager.cartella_safebin,
        #safebinObj.getPath()
    ]
    for x in cartelle:
        if not os.path.isdir(x):
            # se non esiste provo a crearla, se non ci riesce allora c'e' un problema :((
            happy = creaCartella(x)
            if not happy:
                log.critical(f"Permessi negati per la creazione di cartella [{x}] - EXIT Q_Q")
                exit(0)


def leggiConfigFile(dirpath: str) -> list[dict]:
    """Una volta letto il file, tramite JSON ritorno una lista di dict"""
    percorso = dirpath + '/' + confFile
    toret = leggiConfig(percorsoCompleto=percorso)
    if toret is not None:
        return json.loads(toret)
    else:
        return []


def leggiConfigNodo() -> dict:
    """Una volta letto il file, tramite JSON ritorno una lista di dict"""
    toret = leggiConfig(percorsoCompleto=confNodo)
    if toret is not None:
        return json.loads(toret)
    return {}


def aggiornaConfigFile(dirpath: str, contenuto: list[dict]) -> bool:
    percorso = dirpath + "/" + confFile
    cont = json.dumps(obj=contenuto)
    return scriviConfig(percorsoCompleto=percorso, contenuto=cont, hidden=True)


def aggiornaConfigNodo(contenuto: dict) -> bool:
    cont = json.dumps(obj=contenuto)
    return scriviConfig(percorsoCompleto=confNodo, contenuto=cont)


def leggiSafeBinList(path: str) -> list[dict]:
    percorso = path + safebinlist
    toret = leggiConfig(percorsoCompleto=percorso)
    if toret is not None:
        return json.loads(toret)
    else:
        return []


def aggiornaSafeBinList(path: str, contenuto: list[dict]) -> bool:
    cont = json.dumps(obj=contenuto)
    percorso = path + safebinlist
    return scriviConfig(percorsoCompleto=percorso, contenuto=cont)


def leggiConfigSafeBin() -> dict:
    """Una volta letto il file, tramite JSON ritorno una lista di dict"""
    toret = leggiConfig(percorsoCompleto=confSafe)
    if toret is not None:
        return json.loads(toret)
    else:
        return {}


def aggiornaConfigSafeBin(contenuto: dict) -> bool:
    cont = json.dumps(obj=contenuto)
    # todo: se il percorso è diverso, va cancellata la vecchia config ?
    return scriviConfig(percorsoCompleto=contenuto.get('percorso') + confSafe, contenuto=cont)


def scriviConfig(percorsoCompleto: str, contenuto: str, hidden: bool = False) -> bool:
    try:
        fp = open(percorsoCompleto, 'w')
        fp.write(contenuto)
        fp.close()
        if hidden and os.name == 'nt':
            try:
                subprocess.check_call(["attrib", "+H", percorsoCompleto])
            except Exception as e:
                log.warning(f"Occultamento file config {percorsoCompleto} fallito - {e}")
        return True
    except PermissionError as e:
        log.error(f"Errore scrittura file [{percorsoCompleto}] - {e}")
        return False


def leggiConfig(percorsoCompleto: str) -> str | None:
    try:
        f = open(percorsoCompleto, 'r')
        toret = f.read()
        f.close()
        return toret
    except PermissionError as e:
        log.error(f"Impossibile aprire il file config - permesso negato - {e}")
    except FileNotFoundError:
        log.debug(f"File configurazione non trovato in {percorsoCompleto}")
    return None


