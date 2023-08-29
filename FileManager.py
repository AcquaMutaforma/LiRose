import subprocess  # per creare files invisibili in windows :<
import LogManager
import os
from SafeBinManager import SafeBin
import SafeBinManager

log = LogManager.setName(__name__)

cartella_configFiles = 'configFiles'
cartella_keys = 'keys'


def verificaComponentiAvvio(safebinObj: SafeBin):
    percorsoBase = str(__file__).removesuffix('FileManager.py')
    cartelle = [percorsoBase + cartella_configFiles,
                percorsoBase + cartella_keys,
                percorsoBase + LogManager.cartella_logs,
                percorsoBase + SafeBinManager.cartella_safebin,
                safebinObj.getPath()]
    for x in cartelle:
        if not verificaDir(x):
            happy = creaCartella(x)
            if not happy:
                log.critical(f"Permessi negati per la creazione di cartella [{x}] - EXIT Q_Q")
                exit(0)


# TODO: credo non serva a nessuno
def creaFile(percorso: str, nomefile: str, contenuto: str) -> bool:
    percorsoCompleto = percorso + '/' + nomefile
    try:
        fp = open(percorsoCompleto, 'r')
        fp.close()
        return False
    except FileNotFoundError:
        return scriviSuFile(percorsoCompleto=percorso, contenuto=contenuto)


def creaCartella(percorso: str) -> bool:
    try:
        os.mkdir(path=percorso)
        return True
    except PermissionError as e:
        log.error(f"Creazione cartella [{percorso}] Fallita - {e}")
    except FileExistsError as e:
        log.warning(f"Creazione cartella [{percorso}] Fallita - {e}")
    return False


def scriviSuFile(percorsoCompleto: str, contenuto: str) -> bool:
    try:
        fp = open(percorsoCompleto, 'w')
        fp.write(contenuto)
        fp.close()
        return True
    except PermissionError as e:
        log.error(f"Errore scrittura file [{percorsoCompleto}] - {e}")
        return False


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


def aggiornaFile(percorso: str, nomefile: str, contenuto: str, safebin: SafeBin) -> bool:
    percorsoCompleto = percorso + '/' + nomefile
    if gotoSafeBin(percorsoCompleto=percorsoCompleto, nomefile=nomefile, safebin=safebin):
        return scriviSuFile(percorsoCompleto=percorsoCompleto, contenuto=contenuto)
    else:
        return False


def eliminaFile(percorso: str, nome: str) -> bool:
    pass  # todo z_z


def gotoSafeBin(percorsoCompleto: str, nomefile: str, safebin: SafeBin) -> bool:
    # todo: safe bin deve aggiungere il "record" dell'oggetto nella config safe
    return spostaFiles(src=percorsoCompleto + nomefile, dst=safebin.getPath()+'/'+nomefile)


def spostaFiles(src: str, dst: str) -> bool:
    try:
        os.replace(src=src, dst=dst)
        return True
    except FileNotFoundError as e:
        log.error(f'Sovrascrittura files non eseguita - {e}')
    except PermissionError as e:
        log.error(f'Sovrascrittura files non eseguita - {e}')
    return False


def verificaDir(percorso: str):
    return os.path.isdir(percorso)


def sincronizzaFiles():  # lista di elementi da copiare
    pass  # todo


# per le ridondanze
def copiaFile(src: str, dst: str):
    # todo
    '''
    files = os.listdir(src_dir)
    for x in files:
        shutils.copy2(os.path.join(path,x), dst_dir)
    '''
    pass
