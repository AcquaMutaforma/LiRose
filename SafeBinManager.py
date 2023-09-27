"""
giorni scadenza = da 7 a 60. Default 20g
MaxSide = 100 MB a X. Default 10GB
"""
import ConfigManager
import datetime

dateFormat = "%d/%m/%Y %H:%M:%S"


class BackupElem:
    def __init__(self, filename: str, oldpath: str, data: str = None):
        self.filename = filename
        self.oldpath = oldpath
        if data is None:
            self.dataInserimento = datetime.datetime.today().strftime(dateFormat)
        else:
            self.dataInserimento = data

    def toDict(self) -> dict:
        return {
            'filename': self.filename,
            'oldpath': self.oldpath,
            'dataInserimento': self.dataInserimento
        }


class SafeBin:
    def __init__(self, path: str, maxday: int = 20, maxsize: int = 1e+9):
        if path is None or len(path) < 4:
            self.__percorso = str(__file__).replace('SafeBinManager.py', ConfigManager.confSafe)
        else:
            self.__percorso = path
        """
        :param maxday: numero di giorni da aspettare prima di cancellare i files nella SafeBin. Default 20g
        :param maxsize: Grandezza massima in Byte per la rimozione anticipata. Default 10GB
        """
        self.__giorniScadenza = maxday
        self.__grandezzaMax = maxsize
        self.verificaScadenzeSafeBin()

    def getPath(self):
        return self.__percorso

    def getGiorniScadenza(self):
        return self.__giorniScadenza

    def getGrandezzaMax(self):
        return self.__grandezzaMax

    def toDict(self):
        return {
            'percorso': self.getPath(),
            'giorniScadenza': self.getGiorniScadenza(),
            'grandezzaMax': self.getGrandezzaMax()
        }

    def modificaPercorso(self, path: str) -> bool:
        self.__percorso = path
        return ConfigManager.aggiornaConfigSafeBin(contenuto=self.toDict())

    def modificaGiorniScadenza(self, gg: int) -> bool:
        if 7 <= gg <= 60:
            self.__giorniScadenza = gg
            ConfigManager.aggiornaConfigSafeBin(contenuto=self.toDict())
            return True
        return False

    def modificaGrandezzaMax(self, maxbyte: int) -> bool:
        if maxbyte > 1e+7:
            self.__grandezzaMax = maxbyte
            ConfigManager.aggiornaConfigSafeBin(contenuto=self.toDict())
            return True
        return False

    def verificaScadenzeSafeBin(self) -> list:
        """Viene chiamato alla creazione, non serve avviarlo nuovamente."""
        elementi = creaListaBackupElemFromConfig()
        oggi = datetime.datetime.today()
        toremove = []
        for x in elementi:
            dataIns = datetime.datetime.strptime(x.dataInserimento, dateFormat)
            # se il file e' nella "safe bin" da piu giorni di quelli consentiti, procedo alla rimozione
            if (dataIns + datetime.timedelta(days=self.getGiorniScadenza())) > oggi:
                toremove.append(x.filename)
                # FileManager.eliminaFile(percorso=self.getPath(), nome=x.filename)
        ConfigManager.aggiornaSafeBinList(path=self.getPath(), contenuto=listaBackupElemToDict(elementi))
        return toremove

    def aggiungiFile(self, fn: str, oldp: str):
        new = BackupElem(filename=fn, oldpath=oldp)
        elem = creaListaBackupElemFromConfig()
        elem.append(new)
        toret = listaBackupElemToDict(elem)
        ConfigManager.aggiornaSafeBinList(path=self.getPath(), contenuto=toret)


def getSafeBinFromConfig() -> SafeBin:
    sb = ConfigManager.leggiConfigSafeBin()
    path = sb.get('percorso')
    gg = sb.get('giorniScadenza')
    maxbyte = sb.get('grandezzaMax')
    if path is None or gg is None or maxbyte is None:
        return SafeBin()
    else:
        return SafeBin(path=path, maxday=gg, maxsize=maxbyte)


GlobalSafeBin = SafeBin


def creaListaBackupElemFromConfig() -> list[BackupElem]:
    toret: list[BackupElem] = []
    path = GlobalSafeBin.getPath()
    configSB = ConfigManager.leggiSafeBinList(path)
    for x in configSB:
        fn = x.get('filename')
        data = x.get('dataInserimento')
        oldpath = x.get('oldpath')
        if fn is None or data is None or oldpath is None:
            continue
        else:
            toret.append(BackupElem(filename=fn, oldpath=oldpath, data=data))
    return toret


def listaBackupElemToDict(lista: list[BackupElem]) -> list[dict]:
    toret: list[dict] = []
    for x in lista:
        toret.append(x.toDict())
    return toret

