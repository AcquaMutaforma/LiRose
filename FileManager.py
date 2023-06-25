import ConfigManager


def loadFiles(dirpath) -> list:
    """Carica il file configurazione presente nella cartella e ritorna una lista di oggetti "file"."""
    dati = ConfigManager.leggiConfigDirFiles(dirpath)  # ritorna una lista di dizionari, quindi foreach devo creare un
    # oggetto e aggiungerlo alla nuova lista da usare come return

    '''
    Creo gli oggetti dal formato JSON
    Leggo i files all'interno della cartella e controllo le differenze (è da cercare un modo veloce per farlo)
    Calcolo e valuto anche gli hash dei files che sembrano gli stessi
    Ritorno la lista di obj File e un elemento per rappresentare l'esito.'''

    # todo: add "ricalcolo" hash per assicurarsi che il file non sia stato sostituito manualmente,
    #   in quel caso viene aggiornato l'hash del file presente.

    # todo: va aggiunto un valore per specificare se i files sono gli stessi, sono di più, di meno o alterati, Enum/int?
    return []


class File:
    """Questa classe rappresenta i files presenti all'interno di una certa cartella.
    Lo scopo principale è fornire supporto per scrittura, lettura, valutazioni di sostituzione e verifica di
    cambiamenti nei files all'interno della cartella."""

    def __init__(self, filename: str, hashCode: str, lastUpdate: str):
        self.__filename = filename
        self.__hashCode = hashCode
        self.__lastUpdate = lastUpdate
        self.__verificaInfo()
        # todo: add verifica informazioni

    def toDict(self):
        return {
            'filename': self.__filename,
            'hashCode': self.__hashCode,
            'lastUpdate': self.__lastUpdate
        }

    def __verificaInfo(self):
        """Verifica che le informazioni appartenenti al file siano corrette"""
        pass

    def getFilename(self):
        return self.__filename

    def getHashcode(self):
        return self.__hashCode

    def getLastUpdate(self):
        return self.__lastUpdate

# TODO: NOTAAAAAA la scrittura in file se ne occupa chi utilizza gli obj "File",
#  qua fornisco solo "toDict" da chiamare per ogni elemento da trasformare in JSON
