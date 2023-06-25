"""
Classe Nodo mantiene tutte le info principali del dispositivo
"""
import DirectoryManager
import DirectoryClass


class Nodo:
    """Questo viene creato dal main come nuovo nodo o caricato da un file config"""

    def __init__(self, nome: str, idn: int, sbpath: str = "/", dirlist: list = None, nodi: list = None):
        self.nome = nome
        self.idNodo = idn
        self.safeBinPath = sbpath
        self.directoryList = DirectoryManager.loadDirList(dirlist)
        self.nodiList = nodi

    def toDict(self) -> dict:
        dirList = []
        for x in self.directoryList:
            if isinstance(x, DirectoryClass.Directory):
                dirList.append(x.getPath())
        return {
            'nome': self.nome,
            'idNodo': self.idNodo,
            'safeBinPath': self.safeBinPath,
            'dirList': dirList,  # lista con obj directory va trasformata in lista come "dirList" con solo i path
            'nodiList': self.nodiList
        }

    def isValid(self):
        """ True = oggetto valido, False instead"""
        pass
