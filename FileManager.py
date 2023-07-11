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
        self.__contenuto: list[Elemento] = []  # todo: controllare se e' corretto

    def aggiungiElemento(self, oggetto: Elemento):
        if isinstance(oggetto, Elemento):  # e' corretto, ho controllato
            self.__contenuto.append(oggetto)

    def getDirname(self):
        return self.__dirname

    def toDict(self) -> dict:
        cont = {}
        for x in self.__contenuto:
            cont.update(x.toDict())
        return {
            'dirname': self.getDirname(),
            'contenuto': cont  # todo: controllare se ha senso
        }


def getConfigurazione(dirpath: str) -> dict:
    """
    Chiama il metodo per creare la List <Elemento> poi in ricorsione trasforma tutto in formato dict per essere
    scritto da Json nel file configurazione
    """
    return {}


def creaLista(dirpath: str) -> list[Elemento]:
    """
    Metodo per creare una lista di oggetti in base ai files e cartelle presenti nel percorso specificato.
    Usa configManager per recuperare il file in formato JSON
    Smonta il JSON e in maniera ricorsiva(nelle dir) va a creare i vari oggetti
    """
    toret: list[Elemento] = []

    # todo

    return toret


def confrontaConfigEsterna() -> [list[Elemento], list[Elemento]]:  # todo: decidere chi lo chiama e come
    return [], []


"""def test() -> [list, list]:
    a = ['a','1']
    b = ['b', '2']
    return a, b


t, _ = test()
print(f"t = {t}")"""
