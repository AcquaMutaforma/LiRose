from LogManager import logger as log
import ConfigManager
import datetime
import os
import hashlib
import time

dateFormat = "%d/%m/%Y %H:%M"


def verificaCorrettezzaFileInConfig(y, dirpath: str) -> bool:
    """L'oggetto File viene messo a confronto con il file nella cartella, se sono differenti ritorno False."""
    filename = y.getFilename()
    percorsoCompleto = dirpath + '/' + filename
    datafile = datetime.datetime.strptime(time.ctime(os.path.getmtime(percorsoCompleto)), dateFormat)
    if datafile != y.getLastUpdate():
        log.debug(f"File e config non hanno data uguale: {filename} conf:{y.getLastUpdate()} file: {datafile}")
        return False
    hashfile = __calcolaHashCode(percorsoCompleto)
    if y.getHashcode() != hashfile:
        log.debug(f"File e config non hanno hashcode uguale: {filename} conf:{y.getHashcode()} file: {hashfile}")
        return False
    return True


def loadFiles(dirpath) -> (list, int, int, int):
    """Carica il file configurazione presente nella cartella e ritorna una lista di oggetti "file".
    Creo gli oggetti dal formato JSON
    Leggo i files all'interno della cartella e controllo le differenze
    Calcolo e valuto anche gli hash dei files che sembrano gli stessi
    Ritorno la lista di obj File e un elemento per rappresentare l'esito."""

    listaFileObj = []
    listaJsonObjs = ConfigManager.leggiConfigFile(dirpath)  # lista di dizionari
    if listaJsonObjs is None:
        return []
    if len(listaJsonObjs) > 0:
        for x in listaJsonObjs:
            try:
                f = File(filename=x.filename, hashCode=x.hashCode, lastUpdate=x.lastUpdate)
                listaFileObj.append(f)
            except Exception as e:
                log.warning(f'Errore JSON to "File" - {e}')

    listaFilesAttuali = os.listdir(dirpath)  # + '/' ???
    filesRimossi = 0
    filesAggiunti = 0
    filesErrati = 0
    listaFileToAdd = []  # listaFileToAdd.append(createNewFile())
    if len(listaFileObj) > 0:
        '''Per ogni elemento nella lista di oggett, vado a verificare le info e rimuovo il nome
            dalla lista dei files attuali. Nel caso di modifiche vado ad alterare le info dell'oggetto nella lista.
            I nomi rimanenti sono file nuovi '''
        for y in listaFileObj:
            """Controllo gli elementi dalla config se vanno tolti o aggiornati"""
            if '.conf' in y:
                continue
            yFileName = y.getFilename()
            if yFileName in listaFilesAttuali:
                log.debug(f"Trovata corrispondenza tra config e file nella cartella - {yFileName}")
                if not verificaCorrettezzaFileInConfig(y, dirpath):
                    # Se e' differente dal file presente lo rimuovo dalle 2 liste e lo crearo da zero, meno codice
                    listaFilesAttuali.remove(yFileName)
                    listaFileObj.remove(y)
                    listaFileToAdd.append(creaNuovoFileObj(yFileName, dirpath))
                    filesErrati += 1
            else:
                listaFileObj.remove(y)
                filesRimossi += 1
    '''Aggiungo i files nuovi o comunque non presenti nel file configurazione'''
    for z in listaFilesAttuali:
        tmp = creaNuovoFileObj(z, dirpath)
        filesAggiunti += 1
        listaFileToAdd.append(tmp)
    listaFileObj += listaFileToAdd  # todo: vedere se il risultato e' corretto
    return listaFileObj, filesAggiunti, filesRimossi, filesErrati


class File:
    """Questa classe rappresenta i files presenti all'interno di una certa cartella.
    Lo scopo principale è fornire supporto per scrittura, lettura, valutazioni di sostituzione e verifica di
    cambiamenti nei files all'interno della cartella."""

    def __init__(self, filename: str, hashCode: str, lastUpdate: str):
        """Non controllo i valori, li faccio controllare alle 2 funzioni sopra che si occupano di caricare e creare"""
        self.__filename = filename
        self.__hashCode = hashCode
        self.__lastUpdate = datetime.datetime.strptime(lastUpdate, dateFormat)
        log.debug(f"Creato oggetto 'File' : {self.getFilename()}, {self.getHashcode()}, {self.getLastUpdate()}")

    def toDict(self):
        return {
            'filename': self.getFilename(),
            'hashCode': self.getHashcode(),
            'lastUpdate': self.getLastUpdate().__str__()
        }

    def getFilename(self):
        return self.__filename

    def getHashcode(self):
        return self.__hashCode

    def getLastUpdate(self) -> datetime.date:
        return self.__lastUpdate


# TODO: NOTAAAAAA la scrittura in file se ne occupa chi utilizza gli obj "File",
#  qua fornisco solo "toDict" da chiamare per ogni elemento da trasformare in JSON


def creaNuovoFileObj(filename: str, dirpath: str) -> File | None:
    """Prende dal file le info, calcola l'hash, crea un oggetto 'File' e lo ritorna"""
    percorsoCompleto = dirpath + '/' + filename
    try:
        datafile = time.ctime(os.path.getmtime(percorsoCompleto))
        nuovoHash = __calcolaHashCode(percorsoCompleto)
        if nuovoHash is None:
            return None
        return File(filename=filename, hashCode=nuovoHash, lastUpdate=datafile)
    except FileNotFoundError as e:
        log.error(f"File:{filename} in Cartella:{dirpath} non trovato {e} - WTF")
        return None


def __calcolaHashCode(filepath: str) -> str | None:
    try:
        fp = open(filepath, "rb")
        return hashlib.file_digest(fp, "sha256").hexdigest()
    except PermissionError as e:
        log.error(f"Permessi lettura negati per [{filepath}] - {e}")
    except Exception as e:
        log.error(f"Calcolo hash fallito per [{filepath}] - {e}")
    return None
