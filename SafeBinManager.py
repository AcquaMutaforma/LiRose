"""
giorni scadenza = da 7 a 60. Default 20g
MaxSide = 100 MB a X. Default 10GB
"""
import FileManager
import ConfigManager
import datetime

dateFormat = "%d/%m/%Y %H:%M:%S"

cartella_safebin = 'safeBin'


def getDefaultSafeBinPath() -> str:
    return str(__file__).replace('SafeBinManager.py', cartella_safebin)


class BackupElem:
    def __init__(self, filename:str, oldpath: str, data: str = None):
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
    def __init__(self, path: str = getDefaultSafeBinPath(), maxday: int = 20, maxsize: int = 1e+9):
        """
        :param maxday: numero di giorni da aspettare prima di cancellare i files nella SafeBin. Default 20g
        :param maxsize: Grandezza massima in Byte per la rimozione anticipata. Default 10GB
        """
        self.__percorso = path
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
        if FileManager.verificaDir(path):
            self.__percorso = path
            ConfigManager.aggiornaConfigSafeBin(path=path, contenuto=self.toDict())
            return True
        return False

    def modificaGiorniScadenza(self, gg: int) -> bool:
        if 7 <= gg <= 60:
            self.__giorniScadenza = gg
            ConfigManager.aggiornaConfigSafeBin(path=self.getPath(), contenuto=self.toDict())
            return True
        return False

    def modificaGrandezzaMax(self, maxbyte: int) -> bool:
        if maxbyte > 1e+7:
            self.__grandezzaMax = maxbyte
            ConfigManager.aggiornaConfigSafeBin(path=self.getPath(), contenuto=self.toDict())
            return True
        return False

    def verificaScadenzeSafeBin(self):
        """Viene chiamato alla creazione, non serve avviarlo nuovamente."""
        elementi = creaListaBackupElemFromConfig(self)
        oggi = datetime.datetime.today()
        for x in elementi:
            dataIns = datetime.datetime.strptime(x.dataInserimento, dateFormat)
            if (dataIns + datetime.timedelta(days=self.getGiorniScadenza())) > oggi:
                FileManager.eliminaFile(percorso=self.getPath(), nome=x.filename)
                elementi.remove(x)
        ConfigManager.aggiornaSafeBinList(path=self.getPath(), contenuto=listaBackupElemToDict(elementi))

    def aggiungiFile(self, fn: str, oldp: str):
        new = BackupElem(filename=fn, oldpath=oldp)
        elem = creaListaBackupElemFromConfig(self)
        elem.append(new)
        toret = listaBackupElemToDict(elem)
        ConfigManager.aggiornaSafeBinList(path=self.getPath(), contenuto=toret)


def getSafeBinFromConfig(path: str = None) -> SafeBin | None:
    if path is None:
        p = getDefaultSafeBinPath()
    else:
        p = path
    sb = ConfigManager.leggiConfigSafeBin(p)
    if sb is None:
        return SafeBin()
    path = sb.get('percorso')
    gg = sb.get('giorniScadenza')
    maxbyte = sb.get('grandezzaMax')
    if path is None or gg is None or maxbyte is None:
        return SafeBin()
    return SafeBin(path=path, maxday=gg, maxsize=maxbyte)


def creaListaBackupElemFromConfig(sb: SafeBin) -> list[BackupElem]:
    toret: list[BackupElem] = []
    path = sb.getPath()
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


globalSafeBin = getSafeBinFromConfig()
