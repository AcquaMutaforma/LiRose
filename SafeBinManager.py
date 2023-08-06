"""
giorni scadenza = da 7 a 60. Default 20g
MaxSide = 100 MB a X. Default 10GB
"""
import FileManager

cartella_safebin = 'safeBin'


def getDefaultSafeBinPath() -> str:
    return str(__file__).replace('SafeBinManager.py', cartella_safebin)


class SafeBin:
    def __init__(self, path: str = getDefaultSafeBinPath(), maxday: int = 20, maxsize: int = 1e+9):
        """
        :param maxday: numero di giorni da aspettare prima di cancellare i files nella SafeBin. Default 20g
        :param maxsize: Grandezza massima in Byte per la rimozione anticipata. Default 10GB
        """
        self.__percorso = path
        self.__giorniScadenza = maxday
        self.__grandezzaMax = maxsize
        self.verificaFiles()

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
            self.__grandezzaMax = maxbyte
            return True
        return False

    def verificaScandenzaFiles(self):
        pass  # todo


def getSafeBinFromConfig(sbpath: dict) -> SafeBin | None:
    path = sbpath.get('percorso')
    gg = sbpath.get('giorniScadenza')
    maxbyte = sbpath.get('grandezzaMax')
    if path is None or gg is None or maxbyte is None:
        return SafeBin()
    return SafeBin(path=path, maxday=gg, maxsize=maxbyte)

