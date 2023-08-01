import subprocess  # per creare files invisibili in windows :<
import LogManager
import os
import SafeBinManager

log = LogManager.setName(__name__)

cartella_configFiles = 'configFiles'
cartella_keys = 'keys'
cartella_logs = 'logs'
cartella_safebin = 'safeBin'


def verificaComponentiAvvio():
    percorsoBase = str(__file__).removesuffix('FileManager.py')
    cartelle = [cartella_configFiles, cartella_keys, cartella_logs, cartella_safebin]
    for x in cartelle:
        if not verificaDir(percorsoBase+x):
            happy = creaCartella(percorsoBase, x)
            if not happy:
                log.critical(f"Permessi negati per la creazione di cartella [{x}] in [{percorsoBase}] - EXIT Q_Q")
                exit(0)


def creaFile(percorso: str, nomefile: str, contenuto: str) -> bool:
    percorsoCompleto = percorso + '/' + nomefile
    try:
        fp = open(percorsoCompleto, 'r')
        fp.close()
        return False
    except FileNotFoundError:
        return __scriviSuFile(percorsoCompleto=percorso, contenuto=contenuto)


def creaCartella(percorso: str, nomedir: str) -> bool:
    try:
        os.mkdir(path=percorso+nomedir)
        return True
    except PermissionError as e:
        log.error(f"Creazione cartella [{percorso+nomedir}] Fallita - {e}")
    except FileExistsError as e:
        log.error(f"Creazione cartella [{percorso+nomedir}] Fallita - {e}")
    return False


def __scriviSuFile(percorsoCompleto: str, contenuto: str) -> bool:
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
        return None
    except FileNotFoundError:
        return ''


def sovrascriviFile(percorso: str, nomefile: str, contenuto: str) -> bool:
    percorsoCompleto = percorso + '/' + nomefile
    if gotoSafeBin(percorsoCompleto=percorsoCompleto, nomefile=nomefile):
        return __scriviSuFile(percorsoCompleto=percorsoCompleto, contenuto=contenuto)
    else:
        return False


def eliminaFile(percorso: str, nome: str) -> bool:
    return gotoSafeBin(percorsoCompleto=percorso, nomefile=nome)


def gotoSafeBin(percorsoCompleto: str, nomefile: str) -> bool:
    return spostaFiles(src=percorsoCompleto + nomefile, dst=SafeBinManager.getDefaultSafeBinPath() + nomefile)


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


def sincronizzaFiles() -> list:  # lista di elementi da copiare
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


def fileScaduto(percorso: str) -> bool:
    pass
