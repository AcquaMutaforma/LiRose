"""
giorni scadenza = da 7 a 60. Default 20g
MaxSide = 100 MB a X. Default 10GB
"""
import FileManager


def getDefaultSafeBinPath() -> str:
    return str(__file__).replace('SafeBinManager.py', FileManager.cartella_safebin)


class SafeBin:
    def __init__(self, path: str = getDefaultSafeBinPath(), maxday: int = 20, maxsize: int = 1e+9):
        """
        :param maxday: numero di giorni da aspettare prima di cancellare i files nella SafeBin. Default 20g
        :param maxsize: Grandezza massima in Byte per la rimozione anticipata. Default 10GB
        """
        self.__percorso = path
        self.__giorniScadenza = maxday
        self.__grandezzaMassima = maxsize
        self.verificaFiles()

    def toDict(self):
        return {
            'percorso': self.__percorso,
            'giorniScadenza': self.__giorniScadenza,
            'grandezzaMax': self.__grandezzaMassima
        }

    # todo: metodo per verifica e applicazione di cancellazioni, etc etc
    def verificaFiles(self):
        pass

    def modificaPercorso(self, path: str) -> bool:
        if FileManager.verificaDir(path):
            self.__percorso = path
            return True
        return False

    def modificaGiorniScadenza(self, gg: int) -> bool:
        if 7 <= gg <= 60:
            self.__giorniScadenza = gg
            return True
        return False

    def modificaGrandezzaMax(self, maxbyte: int) -> bool:
        if maxbyte > 1e+7:
            self.__grandezzaMassima = maxbyte
            return True
        return False


def getSafeBinFromConfig(sbpath: dict) -> SafeBin | None:
    path = sbpath.get('percorso')
    gg = sbpath.get('giorniScadenza')
    maxbyte = sbpath.get('grandezzaMax')
    if path is None or gg is None or maxbyte is None:
        return None
    return SafeBin(path=path, maxday=gg, maxsize=maxbyte)


def verificaScandenzaFile():
    pass  # todo



# Qua devo inserire anche i metodi per verificare le date, fare controlli, gestire il file
# config che contiene le scadenze dei vari files etc.. etc..
