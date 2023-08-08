"""
Questo modulo fa da supporto per la gestione della configurazione dei files in una cartella.

Cosa fa:
- Crea la configurazione con i files presenti (usato per aggiornare il file configurazione) la funzione ritorna
la stringa da scrivere in files.conf
- Tramite una lista di oggetti per rappresentare files e cartelle, valuta le differenze con un file configurazione che
proviene da una fonte <X> e crea un oggetto esito. (Aiuta l'utente a capire quali files hanno differenze)

"""

import LogManager
import ConfigManager
import datetime
import os
import hashlib

dateFormat = "%d/%m/%Y %H:%M:%S"
log = LogManager.setName(__name__)


# le classi qui sotto prendono spunto dal design pattern "composite"


class Elemento:
    def toDict(self) -> dict:
        return self.__dict__


class File(Elemento):
    """Questa classe rappresenta i files presenti all'interno di una certa cartella.
    Lo scopo principale è fornire supporto per scrittura, lettura, valutazioni di sostituzione e verifica di
    cambiamenti nei files all'interno della cartella."""

    def __init__(self, filename: str, hashCode: str, lastUpdate: str, filesize: int):
        """Non controllo i valori, li faccio controllare alle 2 funzioni sopra che si occupano di caricare e creare"""
        self.__filename = filename
        self.__hashCode = hashCode
        self.__lastUpdate = datetime.datetime.strptime(lastUpdate, dateFormat)
        self.__size = filesize
        log.debug(f"Creato oggetto 'File' : {self.getFilename()}, {self.getHashcode()},"
                  f"{self.getLastUpdate()}, {self.__size}")

    def toDict(self) -> dict:
        return {
            'filename': self.getFilename(),
            'hashCode': self.getHashcode(),
            'lastUpdate': self.getLastUpdate(),
            'size': self.getSize()
        }

    def getFilename(self) -> str:
        return self.__filename

    def getHashcode(self) -> str:
        return self.__hashCode

    def getLastUpdate(self) -> str:
        return self.__lastUpdate.strftime(dateFormat)

    def getSize(self) -> int:
        return self.__size

    def __eq__(self, other):
        if not isinstance(other, File):
            return False
        if self.getFilename() != other.getFilename():
            return False
        if self.getHashcode() != other.getHashcode():
            return False
        return True


class Dir(Elemento):
    def __init__(self, dirname: str, c: list[Elemento] = None):
        self.__dirname = dirname
        if c is None:  # TODO: Nuovo elemento, prima non c'era, controlla se servono fix in basso
            self.__contenuto: list[Elemento] = []
        else:
            self.__contenuto: list[Elemento] = c

    def aggiungiElemento(self, oggetto: Elemento):
        if isinstance(oggetto, Elemento):  # e' corretto, ho controllato
            self.__contenuto.append(oggetto)

    def getDirname(self):
        return self.__dirname

    def getContenuto(self):
        return self.__contenuto

    def toDict(self) -> dict:
        cont: list[dict] = []
        for x in self.getContenuto():
            cont.append(x.toDict())
        return {
            'dirname': self.getDirname(),
            'contenuto': cont
        }

    def __eq__(self, other):
        if not isinstance(other, Dir):
            return False
        if self.getDirname() != other.getDirname():
            return False
        return True


def aggiornaConfigFile(dirpath: str) -> bool:
    """
    Chiama il metodo per creare la List <Elemento> poi in ricorsione trasforma tutto in formato dict per essere
    scritto da Json nel file configurazione
    """
    toret = []
    listaElementi: list[Elemento] = getListaElementiLocali(dirpath)
    for a in listaElementi:
        toret.append(a.toDict())
    return ConfigManager.aggiornaConfigFile(dirpath=dirpath, contenuto=toret)


def getListaElementiLocali(dirpath: str) -> list[Elemento]:
    """Metodo per creare una lista di oggetti in base ai files e cartelle presenti nel percorso specificato.
    In maniera ricorsiva(nelle dir) va a creare i vari oggetti Elemento"""
    toret: list[Elemento] = []
    listaFilesPresenti = os.scandir(dirpath)
    for i in listaFilesPresenti:
        try:
            nomeOggetto = i.name
            if ConfigManager.confFile in nomeOggetto:
                continue
            if i.is_file():
                f = __creaElementoFile(filename=nomeOggetto, dirpath=dirpath)
                if f is not None:
                    toret.append(f)
                    log.debug(f"Aggiunto File(Elemento): [{f.toDict()}] alla lista ")
            elif i.is_dir():
                tmp = __creaElementoDir(dirname=nomeOggetto, dirpath=dirpath)
                if tmp is None:
                    log.error(f"DIR {nomeOggetto} in {dirpath} e' None ?!")
                    continue
                try:
                    contenutoTmp = getListaElementiLocali(dirpath + '/' + nomeOggetto)
                    for j in contenutoTmp:
                        tmp.aggiungiElemento(j)
                    toret.append(tmp)
                    log.debug(f"Aggiunto Dir(Elemento): [{tmp.getDirname()}] con [{len(contenutoTmp)}] elementi alla lista")
                except Exception as e:
                    log.error(f'Errore creazione elemento DIR - {tmp.toDict()} - {e}')
        except PermissionError as e:
            log.error(f"Accesso ad un file in [{dirpath}] negato - {e}")
    return toret


def creaListaElementiFromConf(configurazione: list[dict]) -> list[Elemento]:
    if len(configurazione) < 1:
        log.warning("Lunghezza della config fornita e' '<1'")
        return []
    toret: list[Elemento] = []
    for x in configurazione:
        if x.get('dirname') is None:
            a = File(filename=x.get('filename'), hashCode=x.get('hashCode'),
                     lastUpdate=x.get('lastUpdate'), filesize=x.get('size'))
            if a is not None:
                toret.append(a)
        else:
            b = Dir(dirname=x.get('dirname'))
            if b is None:
                log.warning(f"Nella configurazione [x.dirname] != da None --> dovrebbe essere una cartella "
                            f"--> creazione fallita con valore [{x}]")
                continue
            listaContenuto = (creaListaElementiFromConf(x.get('contenuto')))
            for y in listaContenuto:
                b.aggiungiElemento(y)
            toret.append(b)
    return toret


def __creaElementoFile(filename: str, dirpath: str) -> File | None:
    """Prende dal file le info, calcola l'hash, crea un oggetto 'File' e lo ritorna"""
    log.debug(f"Creazione File Object per {filename} da {dirpath}")
    percorsoCompleto = dirpath + '/' + filename
    try:
        datafile = datetime.datetime.fromtimestamp(os.path.getmtime(percorsoCompleto))
        log.debug(f"Data file {datafile}")
        nuovoHash = __calcolaHashCode(percorsoCompleto)
        log.debug(f"Hash del file {nuovoHash}")
        size = os.path.getsize(percorsoCompleto)
        log.debug(f"grandezza file {size}")
        if nuovoHash is None:
            return None
        f = File(filename=filename, hashCode=nuovoHash, lastUpdate=datafile.strftime(dateFormat), filesize=size)
        return f
    except FileNotFoundError as e:
        log.error(f"File:[{filename}] in Cartella:[{dirpath}] non trovato {e} - WTF")
        return None


def __creaElementoDir(dirname: str, dirpath: str) -> Dir | None:
    log.debug(f"Creazione Dir Object per {dirname} nella cartella {dirpath}")
    percorsoCompleto = dirpath + '/' + dirname
    if os.path.isdir(percorsoCompleto):
        d = Dir(dirname=dirname)
        log.debug(f"{d.toDict()}")
        return d
    else:
        log.error(f"Dir: [{dirname}] in Cartella: [{dirpath}] non trovato - WTF")
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
