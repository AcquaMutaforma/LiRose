from LogManager import logger as log
import json
import Nodo
import os
import subprocess  # per creare files invisibili in windows :<

cartella = 'configFile/'
confNodo = cartella + 'nodo.conf'
confDir = '/dir.conf'
confFile = '/files.conf'
# NOTAA: il file configurazione viene usato per fare il confronto con altri nodi, non gli frega se in locale hai
# fatto delle modifiche o meno


def getNodo() -> Nodo.Nodo | None:
    try:
        f = open(confNodo, 'r')
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


def leggiConfigFile(dirpath: str) -> list | None:
    """Una volta letto il file, tramite JSON ritorno una lista di dict"""
    try:
        f = open(dirpath + confFile, 'r')
        return json.load(f)
    except PermissionError as e:
        log.error(f"Impossibile aprire il file config - permesso negato - {e}")
        return None
    except FileNotFoundError:
        return []


# todo: questo puo essere chiamato fuori o e' troppo rischioso?
def __scriviFileConfig(filename: str, dati: str) -> bool:
    json.dump()  # TODO: cambiare dati: str -> dict, cosi uso json per scrivere direttamente sul file, da fixare
    try:
        fp = open(filename, 'w')
        fp.write(dati)
        return True
    except PermissionError as e:
        log.error(f"Errore scrittura config '{filename}' - Permessi - {e}")
    except Exception as e:
        log.error(f"Errore scrittura config '{filename}' - {e}")
    # Se e' windows, cerco di nascondere i file config aggiungendo l'attributo "hidden"
    # Per ora se uso Linux li vedo, quelli skillati possono fare quello che vogliono u.u
    if os.name == 'nt':
        try:
            subprocess.check_call(["attrib", "+H", filename])
            return True
        except Exception as e:
            log.warning(f"Occultamento file config {filename} fallito - {e}")
    return True
