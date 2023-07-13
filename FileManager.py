"""
Questo modulo fa da supporto per la gestione della configurazione dei files in una cartella.

Cosa fa:
- Crea la configurazione con i files presenti (usato per aggiornare il file configurazione) la funzione ritorna
la stringa da scrivere in files.conf
- Tramite una lista di oggetti per rappresentare files e cartelle, valuta le differenze con un file configurazione che
proviene da una fonte <X> e crea un oggetto esito. (Aiuta l'utente a capire quali files hanno differenze)

"""
import LogManager
from LogManager import logger as log
import ConfigManager
import datetime
import os
import hashlib

dateFormat = "%d/%m/%Y %H:%M:%S"
LogManager.setName(__name__)


# NOTAA: le classi qui sotto prendono spunto dal design pattern "composite"

class Elemento:
    def toDict(self) -> dict:
        return self.__dict__


class File(Elemento):
    """Questa classe rappresenta i files presenti all'interno di una certa cartella.
    Lo scopo principale è fornire supporto per scrittura, lettura, valutazioni di sostituzione e verifica di
    cambiamenti nei files all'interno della cartella."""

    def __init__(self, filename: str, hashCode: str, lastUpdate: str):
        """Non controllo i valori, li faccio controllare alle 2 funzioni sopra che si occupano di caricare e creare"""
        self.__filename = filename
        self.__hashCode = hashCode
        self.__lastUpdate = datetime.datetime.strptime(lastUpdate, dateFormat)
        log.debug(f"Creato oggetto 'File' : {self.getFilename()}, {self.getHashcode()}, {self.getLastUpdate()}")

    def toDict(self) -> dict:
        return {
            'filename': self.getFilename(),
            'hashCode': self.getHashcode(),
            'lastUpdate': self.getLastUpdate()
        }

    def getFilename(self):
        return self.__filename

    def getHashcode(self):
        return self.__hashCode

    def getLastUpdate(self) -> str:
        return self.__lastUpdate.strftime(dateFormat)


class Dir(Elemento):
    def __init__(self, dirname: str):
        self.__dirname = dirname
        self.__contenuto: list[Elemento] = []

    def aggiungiElemento(self, oggetto: Elemento):
        if isinstance(oggetto, Elemento):  # e' corretto, ho controllato
            self.__contenuto.append(oggetto)

    def getDirname(self):
        return self.__dirname

    def toDict(self) -> dict:
        cont = []
        for x in self.__contenuto:
            cont.append(x.toDict())
        return {
            'dirname': self.getDirname(),
            'contenuto': cont  # todo: controllare se ha senso
        }


def getConfigurazione(dirpath: str) -> list[dict]:
    """
    Chiama il metodo per creare la List <Elemento> poi in ricorsione trasforma tutto in formato dict per essere
    scritto da Json nel file configurazione
    """
    toret = []
    listaElementi: list[Elemento] = creaLista(dirpath)
    for a in listaElementi:
        toret.append(a.toDict())
    return toret


def creaLista(dirpath: str) -> list[Elemento]:
    """
    Metodo per creare una lista di oggetti in base ai files e cartelle presenti nel percorso specificato.
    Smonta il JSON e in maniera ricorsiva(nelle dir) va a creare i vari oggetti
    """
    toret: list[Elemento] = []
    listaFilesPresenti = os.scandir(dirpath)
    for i in listaFilesPresenti:
        try:
            nomeOggetto = i.name
            if ConfigManager.confFile in nomeOggetto:
                continue
            if i.is_file():
                f = creaElementoFile(nomeOggetto, dirpath)
                if f is not None:
                    toret.append(f)
                    log.debug(f"Aggiunto File(Elemento): {f.toDict()} alla lista ")
            elif i.is_dir():
                tmp = creaElementoDir(nomeOggetto)
                if tmp is None:
                    log.error(f"DIR {nomeOggetto} in {dirpath} e' None ?!")
                    continue
                try:
                    contenutoTmp = creaLista(dirpath + '/' + nomeOggetto)
                    for j in contenutoTmp:
                        tmp.aggiungiElemento(j)
                    toret.append(tmp)
                    log.debug(f"Aggiunto Dir(Elemento): {tmp.getDirname()} con {len(contenutoTmp)} elementi alla lista")
                except Exception as e:
                    log.error(f'Errore creazione elemento DIR - {tmp.toDict()} - {e}')
        except PermissionError as e:
            log.error(f"Accesso ad un file in {dirpath} negato - {e}")
    return toret


def confrontaConfigEsterna() -> [list[Elemento], list[Elemento]]:  # todo: decidere chi lo chiama e come
    return [], []

# NOTA: nella valutazione, se l'hash è uguale, skippo

"""def test() -> [list, list]:
    a = ['a','1']
    b = ['b', '2']
    return a, b


t, _ = test()
print(f"t = {t}")"""


def creaElementoFile(filename: str, dirpath: str) -> File | None:
    """Prende dal file le info, calcola l'hash, crea un oggetto 'File' e lo ritorna"""
    log.debug(f"Creazione File Object per {filename} da {dirpath}")
    percorsoCompleto = dirpath + '/' + filename
    try:
        datafile = datetime.datetime.fromtimestamp(os.path.getmtime(percorsoCompleto))
        log.debug(f"Data file {datafile}")
        nuovoHash = __calcolaHashCode(percorsoCompleto)
        log.debug(f"Hash del file {nuovoHash}")
        if nuovoHash is None:
            return None
        f = File(filename=filename, hashCode=nuovoHash, lastUpdate=datafile.strftime(dateFormat))
        return f
    except FileNotFoundError as e:
        log.error(f"{__name__} - File:{filename} in Cartella:{dirpath} non trovato {e} - WTF")
        return None


def creaElementoDir(dirname: str) -> Dir | None:
    log.debug(f"Creazione Dir Object per {dirname} ")
    try:
        d = Dir(dirname=dirname)
        log.debug(f"{d.toDict()}")
        return d
    except FileNotFoundError as e:
        log.error(f"{__name__} - Dir:{dirname} non trovato {e} - WTF")
        return None


def __calcolaHashCode(filepath: str) -> str | None:
    try:
        fp = open(filepath, "rb")
        toret = hashlib.file_digest(fp, "sha256").hexdigest()
        fp.close()
        return toret
    except PermissionError as e:
        log.error(f"Permessi lettura negati per [{filepath}] - {e}")
    except Exception as e:
        log.error(f"Calcolo hash fallito per [{filepath}] - {e}")
    return None
